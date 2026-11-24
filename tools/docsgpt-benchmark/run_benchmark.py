#!/usr/bin/env python3
"""DocsGPT 问答基准跑分器 / DocsGPT benchmark runner.

读取同目录 cases.yaml，把每条问题打到线上 DocsGPT，按“检索证据 + 回答正文”两级
判分。用于升级 DocsGPT、更换 embedding / 检索器 / 分块参数、或重新同步文档之后，
确认问答链路没有悄悄退化。

两种模式：

  answer    走站点 widget 用的同一条链路（/stream + 已发布 Agent 的公开 key），
            判“回答正文是否含有文档事实、是否引用了对的文件、该拒答时有没有拒答”。
            慢（每条几秒到几十秒），但这是用户真正得到的东西。
  retrieve  走 DocsGPT 的检索试跑端点（/api/sources/<id>/search），只跑检索不生成
            答案，秒级完成、可全量跑。需要 DocsGPT 主机上的 JWT 密钥，因此只能在
            那台机器上跑（或显式给出 DOCSGPT_JWT_SECRET）。
  both      先 retrieve 快速定位“是检索没召回还是模型没用上”，再 answer 判最终质量。

用法：
    python3 tools/docsgpt-benchmark/run_benchmark.py                    # 全量 answer 模式
    python3 tools/docsgpt-benchmark/run_benchmark.py --mode both        # 检索 + 回答
    python3 tools/docsgpt-benchmark/run_benchmark.py --category cli     # 只跑一类
    python3 tools/docsgpt-benchmark/run_benchmark.py --id rel-4486 -v   # 只看一条
    python3 tools/docsgpt-benchmark/run_benchmark.py --mode retrieve --check
    python3 tools/docsgpt-benchmark/run_benchmark.py --list             # 列分类与条数

密钥：Agent key 取自仓库 _config.yaml 的 docsgpt.api_key（公开 key），可用
DOCSGPT_API_KEY 覆盖；JWT 只从 DOCSGPT_JWT_SECRET 或本机 /opt/docsgpt/.env 读取，
仓库里不存。退出码：--check 下有 FAIL 即 1，适合挂 CI。
"""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import os
import re
import ssl
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("需要 PyYAML：pip install pyyaml")

HERE = Path(__file__).resolve().parent
CASES_FILE = HERE / "cases.yaml"
REPO_ROOT = HERE.parent.parent

GREEN, RED, YELLOW, DIM, RESET = "\033[32m", "\033[31m", "\033[33m", "\033[2m", "\033[0m"


# ────────────────────────────── 配置与密钥 ──────────────────────────────


def load_cases():
    data = yaml.safe_load(CASES_FILE.read_text(encoding="utf-8"))
    return data["target"], data.get("grading", {}), data["cases"]


def agent_key(target):
    """已发布 Agent 的公开 key：环境变量优先，其次仓库站点配置。"""
    key = os.environ.get("DOCSGPT_API_KEY", "").strip()
    if key:
        return key
    rel = target.get("agent_key_from_config") or "_config.yaml"
    conf = yaml.safe_load((REPO_ROOT / rel).read_text(encoding="utf-8"))
    return ((conf or {}).get("docsgpt") or {}).get("api_key") or ""


def jwt_token():
    """给 retrieve 模式现签一个本机 JWT；拿不到就返回 None。"""
    secret = os.environ.get("DOCSGPT_JWT_SECRET", "").strip()
    if not secret:
        env_file = Path("/opt/docsgpt/.env")
        if env_file.is_file():
            for line in env_file.read_text(encoding="utf-8").splitlines():
                if line.startswith("JWT_SECRET_KEY="):
                    secret = line.split("=", 1)[1].strip()
    if not secret:
        return None
    try:
        import jwt
    except ImportError:
        return None
    return jwt.encode({"sub": "local"}, secret, algorithm="HS256")


def http(url, body=None, headers=None, timeout=300, stream=False):
    """一次性请求，返回 (status, text)。"""
    req = urllib.request.Request(url, data=body, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ssl.create_default_context()) as r:
            if not stream:
                return r.status, r.read().decode("utf-8", "replace")
            out = []
            for raw in r:
                out.append(raw.decode("utf-8", "replace"))
            return r.status, "".join(out)
    except urllib.error.HTTPError as err:
        return err.code, err.read().decode("utf-8", "replace")[:2000]
    except Exception as err:  # 超时、断连都算这条用例失败，而不是整个基准崩掉
        return 0, f"{type(err).__name__}: {err}"


# ────────────────────────────── 两种取数方式 ──────────────────────────────


def ask_answer(host, key, question, timeout):
    """走 /stream，收集回答正文与引用文件。"""
    payload = json.dumps(
        {"api_key": key, "question": question, "history": "[]", "stream": True}
    ).encode()
    status, raw = http(
        f"{host.rstrip('/')}/stream",
        body=payload,
        headers={"Content-Type": "application/json", "Accept": "text/event-stream"},
        timeout=timeout,
        stream=True,
    )
    if status != 200:
        return {"error": f"HTTP {status}: {raw[:200]}"}
    answer, sources, error = [], [], None
    for line in raw.splitlines():
        if not line.startswith("data:"):
            continue
        chunk = line[5:].strip()
        if not chunk or chunk == "[DONE]":
            continue
        try:
            event = json.loads(chunk)
        except json.JSONDecodeError:
            continue
        if not isinstance(event, dict):
            continue
        etype = event.get("type")
        if etype == "answer" and isinstance(event.get("answer"), str):
            answer.append(event["answer"])
        elif etype == "source":
            for src in event.get("source") or []:
                if isinstance(src, dict):
                    sources.append({"source": src.get("source") or src.get("filename") or "", "text": src.get("text", "")})
        elif etype == "error":
            error = event.get("error")
    if error:
        return {"error": str(error)}
    if not answer:
        return {"error": "没有拿到回答内容"}
    return {"text": "".join(answer), "sources": sources}


def ask_retrieve(host, token, source_id, question, timeout):
    """走检索试跑端点，只拿召回结果。"""
    payload = json.dumps({"query": question}).encode()
    status, raw = http(
        f"{host.rstrip('/')}/api/sources/{source_id}/search",
        body=payload,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"},
        timeout=timeout,
    )
    if status != 200:
        return {"error": f"HTTP {status}: {raw[:200]}"}
    try:
        body = json.loads(raw)
    except json.JSONDecodeError:
        return {"error": f"响应不是 JSON: {raw[:200]}"}
    if not body.get("success"):
        return {"error": body.get("message", "检索失败")}
    return {
        "sources": [
            {"source": c.get("source") or c.get("filename") or "", "text": c.get("text", "")}
            for c in body.get("chunks", [])
        ],
        "latency_ms": body.get("latency_ms"),
    }


# ────────────────────────────── 判分 ──────────────────────────────


def _norm(text):
    """判分前的归一化：小写 + 折叠空白，避免排版差异造成误判。"""
    return re.sub(r"\s+", " ", (text or "").casefold())


def check_case(case, grading, picked, answer_text=None):
    """返回 (ok, 失败原因列表)。picked 是引用/召回的文件列表，answer_text 为 None
    时（retrieve 模式）文字判定改在召回正文里做。"""
    top_k = grading.get("cite_top_k", 20)
    cited = [item["source"] for item in picked[:top_k]]
    corpus = _norm(answer_text if answer_text is not None else " \n ".join(i["text"] for i in picked))
    reasons = []

    for want in case.get("cite") or []:
        if not any(c.startswith(want) or c.endswith(want) or want in c for c in cited):
            reasons.append(f"未引用 {want}（前 {top_k} 条：{sorted(set(cited))[:4]}）")

    cite_any = case.get("cite_any") or []
    if cite_any and not any(
        any(c.startswith(w) or w in c for c in cited) for w in cite_any
    ):
        reasons.append(f"引用里没有一个候选文件：{cite_any}")

    for want in case.get("all_of") or []:
        if _norm(want) not in corpus:
            reasons.append(f"缺少内容锚点 {want!r}")

    for group in case.get("any_of") or []:
        group = group if isinstance(group, list) else [group]
        if not any(_norm(g) in corpus for g in group):
            reasons.append(f"以下都没出现：{group}")

    for bad in case.get("none_of") or []:
        if _norm(bad) in corpus:
            reasons.append(f"不该出现 {bad!r}")

    if case.get("absent"):
        markers = [_norm(m) for m in grading.get("refusal_markers", [])]
        if not any(m in corpus for m in markers):
            reasons.append("文档里没有这条信息，但回答没有说明查不到（疑似编造）")

    return (not reasons), reasons


def run_one(case, target, grading, mode, host, key, token, source_id, timeout):
    started = time.monotonic()
    question = case["question"]
    result = {
        "id": case["id"],
        "category": case.get("category", "-"),
        "question": question,
        "status": "PASS",
        "reasons": [],
    }

    retrieved = None
    if mode in ("retrieve", "both"):
        if mode == "retrieve" and case.get("absent"):
            # 拒答与否取决于生成环节，纯检索模式判不了，明确跳过而不是蒙一个结果
            result.update(status="SKIP", reasons=["absent 用例只能在 answer / both 模式判定"])
            result["elapsed"] = round(time.monotonic() - started, 1)
            return result
        retrieved = ask_retrieve(host, token, source_id, question, timeout)
        if "error" in retrieved:
            result.update(status="ERROR", reasons=[f"retrieve: {retrieved['error']}"])
            result["elapsed"] = round(time.monotonic() - started, 1)
            return result
        ok, reasons = check_case(case, grading, retrieved["sources"])
        if mode == "retrieve":
            result.update(status="PASS" if ok else "FAIL", reasons=reasons)
            result["cited"] = sorted({i["source"] for i in retrieved["sources"]})[:6]
            result["elapsed"] = round(time.monotonic() - started, 1)
            return result
        if not ok:
            # both 模式：检索这一步已经不干净了，先记下来，继续看最终回答
            result["retrieve_reasons"] = reasons

    answer = ask_answer(host, key, question, timeout)
    if "error" in answer:
        result.update(status="ERROR", reasons=[f"answer: {answer['error']}"])
        result["elapsed"] = round(time.monotonic() - started, 1)
        return result

    ok, reasons = check_case(case, grading, answer["sources"], answer["text"])
    result.update(status="PASS" if ok else "FAIL", reasons=reasons)
    result["cited"] = sorted({i["source"] for i in answer["sources"]})[:6]
    result["answer_excerpt"] = re.sub(r"\s+", " ", answer["text"])[:300]
    if mode == "both":
        retrieve_only = result.pop("retrieve_reasons", None)
        if retrieve_only:
            same = set(reasons) & set(retrieve_only)
            if ok:
                # 回答本身是对的，但检索窗口里没有这条证据：通常是模型从别处
                # 拿到了同样结论，或者证据排在窗口之外，值得单独提示
                result["note"] = "回答通过，但检索阶段有告警：" + "；".join(retrieve_only)
            else:
                result["reasons"] = [f"[检索也没召回] {r}" for r in sorted(same)] + [
                    r for r in reasons if r not in same
                ]
    result["elapsed"] = round(time.monotonic() - started, 1)
    return result


# ────────────────────────────── 入口 ──────────────────────────────


def main():
    parser = argparse.ArgumentParser(description="DocsGPT 问答基准跑分器")
    parser.add_argument("--mode", choices=["answer", "retrieve", "both"], default="answer")
    parser.add_argument("--category", help="只跑这个分类（可逗号分隔多个）")
    parser.add_argument("--id", dest="only_id", help="只跑这个用例 id")
    parser.add_argument("--limit", type=int, help="最多跑前 N 条")
    parser.add_argument("--concurrency", type=int, default=3, help="并发数，默认 3")
    parser.add_argument("--timeout", type=float, default=300, help="单条超时秒数")
    parser.add_argument("--host", help="覆盖 DocsGPT 地址")
    parser.add_argument("--source-id", help="覆盖知识库 source id（retrieve 模式）")
    parser.add_argument("--json", dest="json_out", help="把明细写成 JSON 报告")
    parser.add_argument("--check", action="store_true", help="有 FAIL 则退出码 1（CI 用）")
    parser.add_argument("--fail-under", type=float, help="通过率低于该百分比则退出码 1")
    parser.add_argument("--list", action="store_true", help="列出分类与条数")
    parser.add_argument(
        "--audit-anchors",
        action="store_true",
        help="只做静态检查：找出模型复述问题就能满足的锚点",
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="打印失败用例的回答摘录")
    args = parser.parse_args()

    target, grading, cases = load_cases()

    if args.list:
        by_cat = {}
        for case in cases:
            by_cat[case.get("category", "-")] = by_cat.get(case.get("category", "-"), 0) + 1
        for cat in sorted(by_cat):
            print(f"{by_cat[cat]:>4}  {cat}")
        print(f"{len(cases):>4}  合计")
        return 0

    wanted = {c.strip() for c in args.category.split(",")} if args.category else None
    selected = [
        c
        for c in cases
        if (wanted is None or c.get("category") in wanted)
        and (not args.only_id or c["id"] == args.only_id)
    ]
    if args.limit:
        selected = selected[: args.limit]
    if not selected:
        print("没有匹配的用例")
        return 1

    if args.audit_anchors:
        # 锚点只要出现在问句里，模型复述一遍问题就能满足；这类锚点没有判别力，
        # 用例是否还成立取决于它有没有别的非回声锚点或 cite 要求。
        echoed_total, useless = 0, []
        for case in cases:
            question = _norm(case["question"])
            anchors = list(case.get("all_of") or [])
            anchors += [g for group in (case.get("any_of") or []) for g in (group if isinstance(group, list) else [group])]
            echoed = [a for a in anchors if _norm(a) in question]
            if not echoed:
                continue
            echoed_total += 1
            # 只要还剩下任何一个非回声锚点，或存在 cite 要求，用例就仍然有效
            discriminating = (
                any(_norm(a) not in question for a in anchors)
                or bool(case.get("cite") or case.get("cite_any"))
            )
            if not discriminating:
                useless.append(case["id"])
            print(f"  {case['id']:<26} 可被复述满足：{echoed}")
        print(f"\n{echoed_total}/{len(cases)} 条用例含有回声锚点")
        if useless:
            print(f"其中 {len(useless)} 条没有任何判别力，需要补锚点或补 cite：{', '.join(useless)}")
        return 1 if (args.check and useless) else 0

    host = args.host or os.environ.get("DOCSGPT_API_HOST") or target["api_host"]
    source_id = args.source_id or target.get("source_id")
    key = agent_key(target) if args.mode in ("answer", "both") else ""
    token = jwt_token() if args.mode in ("retrieve", "both") else None

    if args.mode in ("answer", "both") and not key:
        print("拿不到 Agent key：设置 DOCSGPT_API_KEY 或确认仓库 _config.yaml 里有 docsgpt.api_key")
        return 2
    if args.mode in ("retrieve", "both") and not token:
        print(
            "retrieve 模式需要 DocsGPT 主机上的 JWT 密钥：设置 DOCSGPT_JWT_SECRET，"
            "或在 DocsGPT 所在机器上运行（会自动读 /opt/docsgpt/.env）。改用 --mode answer 也可以跑。"
        )
        return 2

    print(f"{len(selected)} 条用例 · mode={args.mode} · {host} · 并发 {args.concurrency}")
    print(f"{'状态':<6}{'分类':<16}{'用例':<26}耗时   说明")
    print("─" * 100)

    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, args.concurrency)) as pool:
        futures = {
            pool.submit(run_one, case, target, grading, args.mode, host, key, token, source_id, args.timeout): case
            for case in selected
        }
        for future in concurrent.futures.as_completed(futures):
            res = future.result()
            results.append(res)
            color = {"PASS": GREEN, "FAIL": RED, "ERROR": YELLOW, "SKIP": DIM}.get(res["status"], RESET)
            note = ""
            if res["status"] == "PASS" and res.get("note"):
                note = f" {YELLOW}{res['note'][:70]}{RESET}"
            elif res["status"] != "PASS":
                note = f" {DIM}{'; '.join(res['reasons'])[:78]}{RESET}"
            print(
                f"{color}{res['status']:<6}{RESET}{res['category']:<16}"
                f"{res['id']:<26}{res['elapsed']:>5.1f}s{note}"
            )
            if res["status"] != "PASS" and args.verbose and res.get("answer_excerpt"):
                print(f"      {DIM}回答摘录：{res['answer_excerpt'][:200]}{RESET}")

    results.sort(key=lambda r: (r["category"], r["id"]))
    graded = [r for r in results if r["status"] != "SKIP"]
    skipped = [r for r in results if r["status"] == "SKIP"]
    passed = sum(1 for r in graded if r["status"] == "PASS")
    failed = [r for r in graded if r["status"] == "FAIL"]
    errored = [r for r in graded if r["status"] == "ERROR"]
    rate = 100.0 * passed / len(graded) if graded else 0.0

    print("─" * 100)
    by_cat = {}
    for res in results:
        bucket = by_cat.setdefault(res["category"], [0, 0])
        if res["status"] == "SKIP":
            continue
        bucket[1] += 1
        bucket[0] += 1 if res["status"] == "PASS" else 0
    for cat in sorted(by_cat):
        ok, total = by_cat[cat]
        flag = "" if ok == total else f"  {RED}← {total - ok} 条未过{RESET}"
        share = f"{ok:>3}/{total:<3} {round(100 * ok / total)}%" if total else f"{'—':>9}"
        print(f"  {cat:<18} {share}{flag}")
    tail = f"，{len(errored)} 条请求出错" if errored else ""
    skip_note = f"（另有 {len(skipped)} 条在当前模式下跳过）" if skipped else ""
    print(f"\n通过率 {passed}/{len(graded)} = {rate:.1f}%{tail}{skip_note}")

    if failed:
        print("\n失败明细：")
        for res in failed:
            print(f"  {res['id']}（{res['category']}）：{'；'.join(res['reasons'])}")
    if errored:
        print("\n错误明细：")
        for res in errored:
            print(f"  {res['id']}：{'；'.join(res['reasons'])}")

    if args.json_out:
        Path(args.json_out).write_text(
            json.dumps(
                {
                    "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
                    "mode": args.mode,
                    "host": host,
                    "passed": passed,
                    "total": len(results),
                    "pass_rate": round(rate, 2),
                    "results": results,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        print(f"\n明细已写入 {args.json_out}")

    if args.fail_under is not None and rate < args.fail_under:
        return 1
    if args.check and (failed or errored):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
