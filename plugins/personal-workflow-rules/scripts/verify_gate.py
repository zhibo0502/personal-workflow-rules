#!/usr/bin/env python3
"""Claude Code PreToolUse hook: commit gate for "did this session run a verify skill?"

Modes (env VERIFY_GATE_MODE): off | observe (default) | enforce
- observe: never blocks; logs commits made without verification to ~/.claude/verify-gate.log
- enforce: blocks `git commit` until a verify skill has run in this session;
           after 2 blocks in the same session the 3rd attempt is allowed (escape hatch).
Detection is heuristic: looks in the session transcript for a Skill call whose name contains "verify".
"""
import json, os, sys, time
from pathlib import Path

MODE = os.environ.get("VERIFY_GATE_MODE", "observe")
STATE_DIR = Path.home() / ".claude" / "verify-gate"
LOG = Path.home() / ".claude" / "verify-gate.log"
MAX_BLOCKS = 2


def ran_verify(transcript_path):
    try:
        with open(transcript_path, encoding="utf-8") as f:
            for line in f:
                if '"Skill"' in line and "verify" in line:
                    return True
    except OSError:
        pass
    return False


def main():
    if MODE == "off":
        return 0
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    if data.get("tool_name") != "Bash":
        return 0
    cmd = (data.get("tool_input") or {}).get("command", "")
    if "git commit" not in cmd:
        return 0
    if ran_verify(data.get("transcript_path", "")):
        return 0

    session = data.get("session_id", "unknown")
    cwd = data.get("cwd", "")
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')}\t{MODE}\t{session}\t{cwd}\tcommit-without-verify\n")

    if MODE != "enforce":
        return 0

    STATE_DIR.mkdir(parents=True, exist_ok=True)
    counter = STATE_DIR / f"{session}.count"
    n = int(counter.read_text()) if counter.exists() else 0
    if n >= MAX_BLOCKS:
        return 0  # escape hatch: don't let Claude get stuck
    counter.write_text(str(n + 1))
    print(
        "提交被拦下：这个会话还没有运行 verify skill。请先运行项目的 verify skill，"
        "确实无法验证的话，在提交说明里写 'Verified: none' 并说明原因。"
        f"（第 {n + 1}/{MAX_BLOCKS} 次拦截）",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
