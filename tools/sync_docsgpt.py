#!/usr/bin/env python3
"""把仓库 docs/ 同步进自托管 DocsGPT / Sync this repo's docs/ into the self-hosted DocsGPT.

DocsGPT 侧的源是 local 快照（type=local，没有 connection_id、没有 remote_data），
它自己不会去拉上游：只有把新的 docs/ 打包 POST 给 manage_source_files 的 sync，
索引才会更新。定时任务 sync_worker 即便把 sync_frequency 设成 daily 也会跳过这类
源（它要求先从 remote_data 解析出可同步的地址），所以这一步必须由 CI 或人来做。

同步是**按文件增量**的：每个文件在 sources.directory_structure 里存了 sha256，只有
内容变了的文件才重新解析和嵌入；实测 2 个文件变更 → 171 块 / 约 14 秒，全量重灌
1646 块 → 89 秒。

⚠️ sync 的语义是「整源替换」： DocsGPT 会先落新文件，再把源目录里**不在本次 zip 里**
的文件删掉。所以绝不能只打包改动的那几个文件，也不能在 docs/ 缺失的分支上跑。
本脚本因此内置了护栏：文件数下限、路径前缀与扩展名校验，不通过就直接退出而不上传。

用法：
    DOCSGPT_TOKEN=dgpt_pat_xxx python3 tools/sync_docsgpt.py            # CI 用法
    DOCSGPT_TOKEN=$(...) python3 tools/sync_docsgpt.py --check          # 失败即退出码 1
    python3 tools/sync_docsgpt.py --dry-run                            # 只体检，不上传

鉴权（CI 里用前者）：
  DOCSGPT_SYNC_TOKEN  随机同步令牌。只作为 X-DocsGPT-Sync 头送出，由云端 Caddy 在
                      manage_source_files / task_status 这两个端点上换成 DocsGPT 内部
                      凭据。因为本部署是 AUTH_TYPE=simple_jwt，DocsGPT 发不出 PAT
                      （auth_type_supports_pats 只允许默认/oidc 模式），所以不能直接
                      用 scope 令牌；也不要把 JWT_SECRET_KEY 交给 CI —— 拿到它等于能
                      伪造该实例的任意身份。
  DOCSGPT_TOKEN       DocsGPT 主机上用：现签的 JWT（或 PAT，若哪天换了鉴权模式）。
服务地址默认取 _config.yaml 的 docsgpt.api_host，可用 DOCSGPT_API_HOST 覆盖。
"""

from __future__ import annotations

import argparse
import io
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
import uuid
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CONFIG = REPO_ROOT / "_config.yaml"

#: 与仓库当前文档规模一致的下限；低于此值说明 checkout 不完整或分支没有 docs/
MIN_FILES = 120
#: sync 会按 sha256 跳过未变文件，没有变化时也应很快返回
DEFAULT_TIMEOUT = 900


def api_host_from_config():
    """_config.yaml 里 docsgpt.api_host 那一个标量，不引入 YAML 依赖。"""
    if not CONFIG.is_file():
        return ""
    in_block = False
    for line in CONFIG.read_text(encoding="utf-8").splitlines():
        if line.startswith("docsgpt:"):
            in_block = True
            continue
        if in_block and line and not line[0].isspace():
            break
        if in_block:
            found = re.search(r'api_host:\s*"?([^"\s]+)"?', line)
            if found:
                return found.group(1).rstrip("/")
    return ""


def build_zip(docs_dir: Path):
    """把 docs/ 打成 zip（条目形如 docs/reference/xxx.md），返回 (字节, 条数, 异常)。"""
    if not docs_dir.is_dir():
        return b"", 0, ["docs/ 目录不存在"]
    entries = []
    problems = []
    for path in sorted(docs_dir.rglob("*")):
        if path.is_dir():
            continue
        rel = path.relative_to(docs_dir.parent).as_posix()
        if path.suffix.lower() != ".md":
            problems.append(f"非 markdown 文件被跳过：{rel}")
            continue
        if not rel.startswith("docs/"):
            return b"", 0, [f"内部错误，路径前缀异常：{rel}"]
        entries.append((rel, path))
    if len(entries) < MIN_FILES:
        problems.append(f"markdown 文件只有 {len(entries)} 个，低于下限 {MIN_FILES}，拒绝上传")
        return b"", len(entries), problems
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for rel, path in entries:
            zf.writestr(rel, path.read_bytes())
    return buf.getvalue(), len(entries), problems


def post_multipart(url, auth, fields, filename, payload, timeout):
    """multipart/form-data POST，返回 (status, 解析后的 body 或原始文本片段)。"""
    boundary = "----sync" + uuid.uuid4().hex
    body = io.BytesIO()
    for key, value in fields.items():
        body.write(f"--{boundary}\r\n".encode())
        body.write(f'Content-Disposition: form-data; name="{key}"\r\n\r\n'.encode())
        body.write(str(value).encode() + b"\r\n")
    body.write(f"--{boundary}\r\n".encode())
    body.write(
        f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
        f"Content-Type: application/zip\r\n\r\n".encode()
    )
    body.write(payload + b"\r\n")
    body.write(f"--{boundary}--\r\n".encode())
    req = urllib.request.Request(
        url,
        data=body.getvalue(),
        headers={
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            **auth,
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, json.loads(resp.read().decode() or "{}")
    except urllib.error.HTTPError as err:
        raw = err.read().decode("utf-8", "replace")
        try:
            return err.code, json.loads(raw)
        except json.JSONDecodeError:
            return err.code, {"raw": raw[:300]}


def get_json(url, auth, timeout):
    req = urllib.request.Request(url, headers=auth)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, json.loads(resp.read().decode() or "{}")
    except urllib.error.HTTPError as err:
        raw = err.read().decode("utf-8", "replace")
        try:
            return err.code, json.loads(raw)
        except json.JSONDecodeError:
            return err.code, {"raw": raw[:300]}


def wait_for_task(host, auth, task_id, timeout):
    """轮询 reingest 任务；DocsGPT 在 sync 响应里把它叫 reingest_task_id。"""
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        status, body = get_json(f"{host}/api/task_status?task_id={task_id}", auth, 60)
        state = str(body.get("status") or body.get("task_status") or "")
        if state in {"SUCCESS", "FAILURE", "REVOKED"}:
            return state, body
        time.sleep(3)
    return "TIMEOUT", {}


def main():
    parser = argparse.ArgumentParser(description="把 docs/ 同步进 DocsGPT")
    parser.add_argument("--source-id", default="085202e8-aa20-4ca7-9ea9-de0cf52de557",
                        help="DocsGPT 知识库 source id（默认 Fourier-GRX-M4）")
    parser.add_argument("--docs-dir", default=str(REPO_ROOT / "docs"), help="文档目录")
    parser.add_argument("--dry-run", action="store_true", help="只体检并打印将要上传的内容")
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT, help="等待重嵌入的秒数上限")
    parser.add_argument("--check", action="store_true", help="失败时退出码 1（CI 用）")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    host = os.environ.get("DOCSGPT_API_HOST", "").strip() or api_host_from_config()

    payload, count, problems = build_zip(Path(args.docs_dir))
    if problems:
        for problem in problems:
            print(f"⚠️  {problem}")
    if not payload:
        print("没有可上传的文档，放弃同步（DocsGPT 侧不会被改动）")
        return 1
    print(f"待上传：{count} 个 markdown，{len(payload) / 1024:.0f} KiB ← {args.docs_dir}")

    if args.dry_run:
        print("dry-run：未上传，DocsGPT 未改动")
        return 0

    if not host:
        print("找不到服务地址：_config.yaml 里没有 docsgpt.api_host，也没设 DOCSGPT_API_HOST")
        return 2

    # 两种凭据，按部署形态择一：
    #   DOCSGPT_SYNC_TOKEN  CI 用。只作为 X-DocsGPT-Sync 头送给 Caddy，由它换取内部
    #                       凭据，且仅对 manage_source_files 这一个端点有效。
    #   DOCSGPT_TOKEN       DocsGPT 主机上用，直接当 Bearer（PAT 或现签 JWT）。
    sync_token = os.environ.get("DOCSGPT_SYNC_TOKEN", "").strip()
    bearer = os.environ.get("DOCSGPT_TOKEN", "").strip()
    if sync_token:
        auth = {"X-DocsGPT-Sync": sync_token}
        print(f"提交到 {host}/api/manage_source_files （source_id={args.source_id}，同步令牌）")
    elif bearer:
        auth = {"Authorization": f"Bearer {bearer}"}
        print(f"提交到 {host}/api/manage_source_files （source_id={args.source_id}，Bearer）")
    else:
        print("缺少凭据：请设置 DOCSGPT_SYNC_TOKEN（CI）或 DOCSGPT_TOKEN（主机上）")
        return 2

    status, body = post_multipart(
        f"{host}/api/manage_source_files", auth,
        {"source_id": args.source_id, "operation": "sync"},
        "docs.zip", payload, 180,
    )
    # 源正被其它改动占用时返回 409 source_busy；CI 里等一会重试即可
    for attempt in range(3):
        if status == 409 and "busy" in json.dumps(body, ensure_ascii=False).lower():
            print(f"源正忙，{10 * (attempt + 1)} 秒后重试")
            time.sleep(10 * (attempt + 1))
            status, body = post_multipart(
                f"{host}/api/manage_source_files", auth,
                {"source_id": args.source_id, "operation": "sync"},
                "docs.zip", payload, 180,
            )
            continue
        break

    if status != 200 or not body.get("success"):
        print(f"提交失败：HTTP {status} {json.dumps(body, ensure_ascii=False)[:400]}")
        return 1

    files = body.get("files") or []
    removed = body.get("removed_files") or []
    print(f"已接收 {len(files)} 个文件；移除 {len(removed)} 个" + (f"：{removed}" if removed else ""))
    if args.verbose:
        print("  " + "\n  ".join(files))

    task_id = body.get("reingest_task_id") or body.get("task_id")
    if not task_id:
        print("响应里没有 reingest_task_id，无法确认重嵌入结果")
        return 1
    state, detail = wait_for_task(host, auth, task_id, args.timeout)
    if state != "SUCCESS":
        print(f"重嵌入未成功：{state} {json.dumps(detail, ensure_ascii=False)[:300]}")
        return 1
    result = detail.get("result")
    if isinstance(result, (dict, list)):
        print("重嵌入结果：" + json.dumps(result, ensure_ascii=False)[:400])
    print("同步完成 ✅")
    return 0


if __name__ == "__main__":
    sys.exit(main())
