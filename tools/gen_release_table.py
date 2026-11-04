#!/usr/bin/env python3
"""固件版本表生成器 / Generate the firmware version table from the release index.

数据源（口径只在这里定义一次）：

  1. 发布索引 manifest.json —— COS 上的公开对象，由 fourier-grx 仓库的
     scripts/release_meta.py 维护，列出每个变体已发布的版本与发布渠道
  2. 正式发布台账 channels.json —— fourier-grx 仓库 release/channels.json，
     只有登记在内的版本算正式版本（长期支持）。本仓库带一份副本
     tools/channels.json；若能看到同级的 fourier-grx 工作副本则优先用它，
     避免两份台账长期漂移

行为：只重写两张发布页里被标记的表格区域，**行只增不删**。

  - 每行的「发布性质 / 支持状态」两列按数据源刷新（版本号加粗规则随之统一）
  - 索引里有、表里没有的版本作为新行插入到正确位置
  - 已下架（安装包已从下载服务器移除）的行原样保留：索引里没有对象不等于该行该消失
  - 表里有、索引里没有的行只告警，不改写下载链接

用法：
    python3 tools/gen_release_table.py --check          # 只检查漂移（CI 用，有漂移则退出码 1）
    python3 tools/gen_release_table.py --write          # 就地重写表格区域
    python3 tools/gen_release_table.py --print-latest   # 打印索引里的渠道最新版本
    python3 tools/gen_release_table.py --manifest /tmp/manifest.json --check
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = {
    "zh": ROOT / "docs" / "release" / "fourier-grx.md",
    "en": ROOT / "docs" / "en" / "release" / "fourier-grx.md",
}
MANIFEST_URL = "https://fourier-grx-1302548221.cos.ap-shanghai.myqcloud.com/grx/manifest.json"
LEDGER_CANDIDATES = [
    ROOT.parent / "fourier-grx" / "release" / "channels.json",
    ROOT / "tools" / "channels.json",
]
DOC_VARIANT = "linux-arm64-cpu-m4l-blaze"

BEGIN = "<!-- BEGIN GENERATED version-table —— 由 tools/gen_release_table.py 维护，请勿手改 -->"
END = "<!-- END GENERATED version-table -->"
HEADER_RE = re.compile(r"^\| (发布日期|Release Date) \|")

CELLS = {
    "zh": {
        "official_kind": "**正式发布**",
        "official_sup": "✅ 长期支持",
        "beta_kind": "内测构建",
        "beta_sup": "❌ 不再支持",
        "other_kind": {"prerelease": "预发布", "test": "内部验证构建"},
        "detail": "[详情](#{anchor})",
        "detail_todo": "待补",
        "download": "[⬇ 下载]({url})",
        "delisted": "已下架",
    },
    "en": {
        "official_kind": "**Official**",
        "official_sup": "✅ Long-term support",
        "beta_kind": "Internal build",
        "beta_sup": "❌ No longer supported",
        "other_kind": {"prerelease": "Pre-release", "test": "Internal test build"},
        "detail": "[Details](#{anchor})",
        "detail_todo": "TBD",
        "download": "[⬇ Download]({url})",
        "delisted": "Delisted",
    },
}


def version_key(version: str) -> tuple:
    m = re.match(r"^(\d+)\.(\d+)\.(\d+)(.*)$", version)
    if not m:
        return (-1, -1, -1, version)
    return (int(m.group(1)), int(m.group(2)), int(m.group(3)), m.group(4))


def load_manifest(source: str) -> dict:
    if source == MANIFEST_URL:
        with urllib.request.urlopen(source, timeout=30) as resp:  # noqa: S310 - 固定的 https 源
            return json.loads(resp.read().decode("utf-8"))
    path = pathlib.Path(source)
    if not path.is_file():
        raise SystemExit(f"ERROR: 索引文件不存在: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def load_ledger(explicit: str | None) -> tuple[dict, pathlib.Path | None]:
    for path in [pathlib.Path(explicit)] if explicit else LEDGER_CANDIDATES:
        if path.is_file():
            return json.loads(path.read_text(encoding="utf-8")), path
    if explicit:
        raise SystemExit(f"ERROR: 台账文件不存在: {explicit}")
    return {"releases": {}}, None


def releases_from_manifest(manifest: dict) -> dict[str, dict]:
    """version -> {channel, lts, url, date, variants}。

    只取文档所讲的这条线（linux-arm64-cpu-m4l-blaze）：只发过预发布渠道的版本
    不进这张表（页面另有「预发布渠道」一节），只存在于 c1 变体的版本同理。
    """
    out: dict[str, dict] = {}
    for row in manifest.get("index") or []:
        version = str(row.get("v") or "")
        variant = str(row.get("variant") or "")
        if not version or variant != DOC_VARIANT:
            continue
        out[version] = {
            "channel": row.get("channel") or "beta",
            "lts": bool(row.get("lts")),
            "url": row.get("url"),
            "date": (row.get("uploaded_at") or row.get("published_at") or row.get("build_time") or "")[:10] or None,
            "variants": [variant],
        }
    return out


def other_channel_versions(manifest: dict, shown: dict[str, dict]) -> dict[str, list[str]]:
    """这条线之外的版本（只在预发布 / c1 渠道出现），用于提示而不是静默丢弃。"""
    others: dict[str, set[str]] = {}
    for row in manifest.get("index") or []:
        version = str(row.get("v") or "")
        variant = str(row.get("variant") or "")
        if version and version not in shown and variant != DOC_VARIANT:
            others.setdefault(variant, set()).add(version)
    return {k: sorted(v, key=version_key) for k, v in sorted(others.items())}


def classify(version: str, entry: dict | None, ledger: dict, lang: str) -> tuple[str, str, bool, str]:
    """返回 (发布性质单元格, 支持状态单元格, 版本号是否加粗, 渠道)。台账优先。"""
    c = CELLS[lang]
    official = ((ledger.get("releases") or {}).get(version) or {}).get("channel") == "stable"
    channel = (entry or {}).get("channel", "beta")
    if official or channel == "stable":
        return c["official_kind"], c["official_sup"], True, "stable"
    if channel in c["other_kind"]:
        return c["other_kind"][channel], c["beta_sup"], False, channel
    return c["beta_kind"], c["beta_sup"], False, channel


def parse_rows(lines: list[str]) -> list[list[str]]:
    rows = []
    for line in lines:
        if not line.startswith("|") or HEADER_RE.match(line) or set(line) <= set("|- "):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 6:
            raise SystemExit(f"ERROR: 表格行列数不是 6：{line[:70]}")
        rows.append(cells)
    return rows


def locate_table(lines: list[str]) -> tuple[int, int]:
    for i, line in enumerate(lines):
        if HEADER_RE.match(line):
            last = i
            while last + 1 < len(lines) and lines[last + 1].startswith("|"):
                last += 1
            return i, last
    raise SystemExit("ERROR: 找不到版本表表头")


def region_of(lines: list[str]) -> tuple[list[str], list[str], list[str], bool]:
    """返回 (前缀, 表格区域, 后缀, 是否需要补标记)。"""
    begin = next((i for i, l in enumerate(lines) if l.strip() == BEGIN), None)
    end = next((i for i, l in enumerate(lines) if l.strip() == END), None)
    if begin is not None and end is not None and end > begin:
        return lines[: begin + 1], lines[begin + 1:end], lines[end:], False
    first, last = locate_table(lines)
    return lines[:first], lines[first:last + 1], lines[last + 1:], True


def render(lang: str, text: str, data: dict[str, dict], ledger: dict, page: pathlib.Path) -> tuple[str, list[str]]:
    notes: list[str] = []
    lines = text.split("\n")
    pre, region, post, need_markers = region_of(lines)
    if need_markers:
        notes.append("该页还没有 BEGIN/END 标记，本次写入会补上")

    header_line = next(l for l in region if HEADER_RE.match(l))
    sep_line = region[region.index(header_line) + 1]

    detail_heads = set(re.findall(r"^### (\d+\.\d+\.\d+)$", text, re.M))
    missing_in_index: list[str] = []
    merged: dict[str, list[str]] = {}
    for cells in parse_rows(region):
        version = cells[1].strip().strip("*").strip()
        kind, sup, bold, channel = classify(version, data.get(version), ledger, lang)
        entry = data.get(version)
        if entry is None:
            missing_in_index.append(version)
        elif channel == "stable" and ((ledger.get("releases") or {}).get(version) or {}).get("channel") != "stable":
            notes.append(f"{version}: 索引标为 stable，但台账未登记，按正式版本渲染——请补台账")
        ver_cell = f"**{version}**" if bold else version
        anchor = "#" + version.replace(".", "")
        if f"({anchor})" in cells[3] and version not in detail_heads:
            notes.append(f"{version}: 详情链接指向的小节不存在")
        if version in merged:
            notes.append(f"{version}: 表格里有重复行，只保留第一条")
            continue
        merged[version] = [cells[0], ver_cell, cells[2], cells[3], kind, sup]

    if missing_in_index:
        shown = sorted(missing_in_index, key=version_key)
        head = ", ".join(shown[:6]) + (" …" if len(shown) > 6 else "")
        notes.append(f"{len(shown)} 行在索引里没有对应对象（{head}），按已下架历史行原样保留")

    for version, entry in sorted(data.items(), key=lambda kv: version_key(kv[0])):
        if version in merged:
            continue
        kind, sup, bold, _channel = classify(version, entry, ledger, lang)
        if _channel == "stable" and ((ledger.get("releases") or {}).get(version) or {}).get("channel") != "stable":
            notes.append(f"{version}: 索引标为 stable，但台账未登记——发布时要用 scripts/release.sh --channel stable 才会写台账")
        anchor = version.replace(".", "")
        has_detail = version in detail_heads
        detail = CELLS[lang]["detail"].format(anchor=anchor) if has_detail else CELLS[lang]["detail_todo"]
        if not has_detail:
            notes.append(f"{version}: 新增行，但页面还没有对应的小节，需要人工补写")
        download = CELLS[lang]["download"].format(url=entry["url"]) if entry.get("url") else CELLS[lang]["delisted"]
        merged[version] = [entry.get("date") or "", f"**{version}**" if bold else version, download, detail, kind, sup]

    order = sorted(merged.items(), key=lambda kv: version_key(kv[0]), reverse=True)
    body = [header_line, sep_line] + ["| " + " | ".join(cells) + " |" for _v, cells in order]
    if need_markers:
        return "\n".join(pre + [BEGIN] + body + [END] + post), notes
    return "\n".join(pre + body + post), notes


def check_prose(text: str, ledger: dict, page: pathlib.Path) -> list[str]:
    """页面顶部关于正式版本的叙述必须和台账一致。"""
    notes: list[str] = []
    want = sorted((v for v, e in (ledger.get("releases") or {}).items() if e.get("channel") == "stable"), key=version_key)
    if not want:
        return notes
    latest = max(want, key=version_key)
    for line in text.splitlines():
        if not line.startswith(">"):
            continue
        for found in re.findall(r"\*\*(\d+\.\d+\.\d+)\*\*", line):
            if "正式版本" in line or "official release" in line.lower():
                if "当前" in line or "current" in line.lower():
                    if found != latest:
                        notes.append(f"叙述里的当前正式版本 {found} 与台账 {latest} 不一致")
        listed = set(re.findall(r"\d+\.\d+\.\d+", line))
        if listed and ("真正的正式发布" in line or "genuine official" in line.lower()):
            if listed != set(want):
                notes.append(f"叙述列举的正式版本 {sorted(listed)} 与台账 {want} 不一致")
    return notes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--manifest", default=MANIFEST_URL, help="索引 URL 或本地文件")
    parser.add_argument("--ledger", help="台账路径，默认找 fourier-grx 工作副本，再退回 tools/channels.json")
    parser.add_argument("--write", action="store_true", help="就地重写表格")
    parser.add_argument("--check", action="store_true", help="只检查是否有漂移")
    parser.add_argument("--print-latest", action="store_true", help="打印索引里各渠道最新版本后退出")
    args = parser.parse_args()

    manifest = load_manifest(args.manifest)
    ledger, ledger_path = load_ledger(args.ledger)

    if args.print_latest:
        print(json.dumps(manifest.get("latest"), ensure_ascii=False, indent=2))
        return 0

    drift = False
    data = releases_from_manifest(manifest)
    official = sorted((v for v, e in (ledger.get("releases") or {}).items() if e.get("channel") == "stable"), key=version_key)
    print(f"索引收录 {len(manifest.get('index') or [])} 个产物 / 本表涵盖版本 {len(data)} 个")
    print(f"台账：{ledger_path or '（未找到，全部按内测构建处理）'}  正式版本：{', '.join(official) or '无'}")
    # 文档仓的台账副本只是 fourier-grx 工作副本不可用时的后备，两份不一致要发声
    mirror = ROOT / "tools" / "channels.json"
    if ledger_path is not None and ledger_path != mirror and mirror.is_file():
        try:
            same = json.loads(mirror.read_text(encoding="utf-8")).get("releases") == ledger.get("releases")
        except json.JSONDecodeError:
            same = False
        if not same:
            print("  ! tools/channels.json 与 fourier-grx/release/channels.json 不一致，请同步这份镜像")
            drift = True
    for variant, vers in other_channel_versions(manifest, data).items():
        tail = " …" if len(vers) > 5 else ""
        print(f"  仅存在于 {variant}：{', '.join(vers[:5])}{tail}（不进本表）")

    for lang, page in PAGES.items():
        if not page.is_file():
            print(f"ERROR: 页面不存在 {page}", file=sys.stderr)
            return 1
        text = page.read_text(encoding="utf-8")
        new_text, notes = render(lang, text, data, ledger, page)
        prose_notes = check_prose(text, ledger, page)
        changed = new_text != text
        print(f"  {page.relative_to(ROOT)}  {'需要更新' if changed else '已一致'}（{len(notes)} 条提示）")
        for note in notes:
            print(f"      · {note}")
        for note in prose_notes:
            print(f"      ! {note}")
        if changed or prose_notes:
            drift = True
        if args.write and changed:
            page.write_text(new_text, encoding="utf-8")
            print(f"      已写入 {page.relative_to(ROOT)}")

    if args.check:
        if drift:
            print("结论：文档与发布索引/台账存在漂移，请运行 python3 tools/gen_release_table.py --write")
            return 1
        print("结论：文档与发布索引/台账一致")
    return 0


if __name__ == "__main__":
    sys.exit(main())
