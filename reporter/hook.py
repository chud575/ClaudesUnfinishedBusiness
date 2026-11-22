#!/usr/bin/env python3
"""Claude Code hook: marks a session as "running" while Claude is working on a prompt.

UserPromptSubmit writes ~/.unfinished-business/sessions/<session_id>.json; Stop and SessionEnd remove it.
report.py reads that folder. Prints nothing (UserPromptSubmit output would be added to Claude's context)
and never fails the hook.
"""
import json
import os
import subprocess
import sys
import time

DIR = os.path.expanduser("~/.unfinished-business/sessions")


def parent_of(pid):
    try:
        return int(subprocess.run(["ps", "-o", "ppid=", "-p", str(pid)], capture_output=True, text=True, timeout=2).stdout.strip())
    except Exception:
        return None


def main():
    try:
        d = json.load(sys.stdin)
    except Exception:
        return
    sid = "".join(c for c in str(d.get("session_id", "")) if c.isalnum() or c in "-_")[:80]
    if not sid:
        return
    path = os.path.join(DIR, sid + ".json")
    event = d.get("hook_event_name", "")
    if event == "UserPromptSubmit":
        prompt = " ".join(str(d.get("prompt", "")).split())
        ppid = os.getppid()
        state = {
            "cwd": d.get("cwd") or os.getcwd(),
            "title": prompt[:140] + ("…" if len(prompt) > 140 else ""),
            "since": int(time.time()),
            "pids": [p for p in (ppid, parent_of(ppid)) if p and p > 1],
        }
        os.makedirs(DIR, exist_ok=True)
        tmp = path + ".tmp"
        with open(tmp, "w") as f:
            json.dump(state, f)
        os.replace(tmp, path)
    elif event in ("Stop", "SessionEnd"):
        try:
            os.remove(path)
        except FileNotFoundError:
            pass


try:
    main()
except Exception:
    pass
sys.exit(0)
