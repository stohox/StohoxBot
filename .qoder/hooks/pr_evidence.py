#!/usr/bin/env python
"""PreToolUse 门禁：拦截 `gh pr create`，强制 PR 描述含三段证据。

约定：PR 正文必须先写入 `.qoder/pr-body.md`，再用 `--body-file` 引用。
本脚本校验该文件的段落完整性，缺段或段落过薄即 exit 2 阻断。
"""

import json
import pathlib
import re
import sys

# 段落名 -> 该段正文最少字符数（去空白后）
SECTIONS = [
    ("行为变更", 15),
    ("验证证据", 15),
    ("剩余限制", 8),
]

HEAD = re.compile(r"^\s*#{1,6}\s*(.+?)\s*#*\s*$")


def deny(msg: str):
    sys.stderr.write(msg + "\n")
    sys.exit(2)


def main():
    raw = sys.stdin.read()
    try:
        data = json.loads(raw)
    except Exception:
        sys.exit(0)

    if data.get("tool_name") != "Bash":
        sys.exit(0)
    cmd = (data.get("tool_input") or {}).get("command") or ""
    if not isinstance(cmd, str) or "gh pr create" not in cmd:
        sys.exit(0)

    m = re.search(r"--body-file\s+\"?([^\s\"]+)", cmd)
    if not m:
        deny(
            "PR 门禁拦截：`gh pr create` 必须使用 `--body-file .qoder/pr-body.md`。\n"
            "请先把 PR 正文写入 .qoder/pr-body.md（含「行为变更 / 验证证据 / 剩余限制」三段），再重新提交。"
        )

    body_path = pathlib.Path(m.group(1))
    if not body_path.exists():
        deny(f"PR 门禁拦截：正文文件不存在: {body_path}")

    text = body_path.read_text(encoding="utf-8", errors="replace")

    blocks = {}
    current = None
    for line in text.splitlines():
        h = HEAD.match(line)
        if h:
            current = h.group(1)
            blocks.setdefault(current, [])
            continue
        if current is not None:
            blocks[current].append(line)

    problems = []
    for name, min_len in SECTIONS:
        found = next((k for k in blocks if name in k), None)
        if found is None:
            problems.append(f"缺少「{name}」段（需要二级标题，如 `## {name}`）")
            continue
        body = "".join(blocks[found]).strip()
        if len(body) < min_len:
            problems.append(
                f"「{name}」段正文过薄（{len(body)} 字符，至少 {min_len}）。"
                "空话、占位符或仅写「无」不予通过。"
            )

    if problems:
        deny("PR 门禁拦截，证据不足：\n- " + "\n- ".join(problems))

    sys.exit(0)


if __name__ == "__main__":
    main()
