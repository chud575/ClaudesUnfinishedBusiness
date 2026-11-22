#!/usr/bin/env python3
"""Sends this machine's "currently running" list to shakybetspokertools.com. launchd runs it every minute.

Reports:
  sessions  Claude Code sessions that are mid-task (written by hook.py)
  jobs      processes matching a pattern in config.json "watch", plus any heavy process
            (>= heavy_cpu % CPU for >= heavy_minutes) such as solver training

Config: ~/.unfinished-business/config.json (made by install.sh). Run by hand with --dry-run to see the report.
"""
import json
import os
import re
import subprocess
import sys
import time
import urllib.request

HOME = os.path.expanduser("~/.unfinished-business")
SESSIONS = os.path.join(HOME, "sessions")
MAX_SESSION_AGE = 6 * 3600  # a turn that never sent Stop (e.g. interrupted) drops off after this

# never counted as a "heavy job"
SKIP = re.compile(r"(^|/)(claude|Claude|WindowServer|kernel_task|mds\w*|mdworker\w*|backupd|photoanalysisd|"
                  r"Google Chrome|Safari|Finder|Dock|softwareupdated|com\.apple\.\S+|Spotlight|cloudd|bird|"
                  r"Code Helper\b.*|Electron|Slack|zoom\.us)\b")
SKIP_PATHS = ("/System/", "/usr/libexec/", "/usr/sbin/", "/Library/Apple/", "/Applications/")


def alive(pid):
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True


def sessions(now):
    out = []
    for name in sorted(os.listdir(SESSIONS)) if os.path.isdir(SESSIONS) else []:
        path = os.path.join(SESSIONS, name)
        if not name.endswith(".json"):
            continue
        try:
            s = json.load(open(path))
        except Exception:
            os.remove(path)
            continue
        if now - s.get("since", 0) > MAX_SESSION_AGE or not any(alive(p) for p in s.get("pids", [])):
            os.remove(path)
            continue
        out.append({"title": s.get("title") or "Working", "folder": os.path.basename(s.get("cwd", "").rstrip("/")),
                    "since": s.get("since")})
    return out


def etime_seconds(t):
    # [[dd-]hh:]mm:ss
    days, _, rest = t.rpartition("-")
    parts = [int(x) for x in rest.split(":")]
    while len(parts) < 3:
        parts.insert(0, 0)
    return (int(days) if days else 0) * 86400 + parts[0] * 3600 + parts[1] * 60 + parts[2]


def short_command(args):
    """'python3 /Users/x/HORSE/train_studhi.py --games 6' -> 'train_studhi.py'. Never sends the full arguments."""
    words = args.split()
    if not words:
        return "process"
    prog = os.path.basename(words[0])
    for w in words[1:]:
        if w.startswith("-"):
            continue
        base = os.path.basename(w)
        if re.search(r"\.(py|sh|js|ts|rb|jl|pl)$", base) or prog.startswith(("python", "node", "bash", "zsh", "sh")):
            return base[:80]
        break
    return prog[:80]


def jobs(cfg, now):
    try:
        ps = subprocess.run(["ps", "-Ao", "pid=,etime=,pcpu=,args="], capture_output=True, text=True, timeout=10).stdout
    except Exception:
        return []
    me = os.getpid()
    watch = [(w["name"], re.compile(w["pattern"])) for w in cfg.get("watch", []) if w.get("name") and w.get("pattern")]
    heavy_cpu, heavy_secs = float(cfg.get("heavy_cpu", 50)), 60 * float(cfg.get("heavy_minutes", 10))
    out, seen = [], set()
    for line in ps.splitlines():
        m = re.match(r"\s*(\d+)\s+(\S+)\s+([\d.]+)\s+(.*)", line)
        if not m:
            continue
        pid, secs, cpu, args = int(m[1]), etime_seconds(m[2]), float(m[3]), m[4].strip()
        if pid == me or "report.py" in args:
            continue
        named = next((n for n, rx in watch if rx.search(args)), None)
        heavy = cpu >= heavy_cpu and secs >= heavy_secs and not SKIP.search(args) and not args.startswith(SKIP_PATHS)
        if not (named or heavy):
            continue
        cmd = short_command(args)
        key = named or cmd
        if key in seen:
            continue
        seen.add(key)
        out.append({"title": named or cmd, "detail": f"{cmd} · {cpu:.0f}% CPU", "since": now - secs})
    return out


def main():
    cfg = json.load(open(os.path.join(HOME, "config.json")))
    now = int(time.time())
    report = {"machine": cfg["machine"], "label": cfg.get("label", cfg["machine"]),
              "sessions": sessions(now), "jobs": jobs(cfg, now)}
    if "--dry-run" in sys.argv:
        print(json.dumps(report, indent=2))
        return
    req = urllib.request.Request(cfg.get("url", "https://shakybetspokertools.com/auth/running/report"),
                                 data=json.dumps(report).encode(), method="POST",
                                 headers={"Content-Type": "application/json", "X-Report-Key": cfg["key"],
                                          "User-Agent": "unfinished-business-reporter"})
    with urllib.request.urlopen(req, timeout=20) as r:
        if "--verbose" in sys.argv:
            print(r.status, r.read().decode()[:200])


if __name__ == "__main__":
    main()
