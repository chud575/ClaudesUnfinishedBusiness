#!/usr/bin/env bash
# Installs the "Currently running" reporter on a Mac (run once on the MacBook and once on the M4 Mini).
#   ./install.sh macbook "MacBook Pro"
#   ./install.sh mini "M4 Mini"
# Asks for the reporter key (SB_RUNNING_KEY from the server's /etc/shakybets-auth.env) the first time.
# Safe to re-run: it updates the scripts and keeps your config.
set -euo pipefail
MACHINE="${1:?usage: ./install.sh <macbook|mini> \"Label\"}"
LABEL="${2:-$MACHINE}"
SRC="$(cd "$(dirname "$0")" && pwd)"
DEST="$HOME/.unfinished-business"
PLIST="$HOME/Library/LaunchAgents/com.unfinishedbusiness.reporter.plist"
PY="$(command -v python3)"

mkdir -p "$DEST/sessions" "$HOME/Library/LaunchAgents"
cp "$SRC/hook.py" "$SRC/report.py" "$DEST/"
chmod +x "$DEST/hook.py" "$DEST/report.py"

# 1. config (kept on re-runs)
if [ ! -f "$DEST/config.json" ]; then
  read -rsp "Reporter key (SB_RUNNING_KEY): " KEY; echo
  MACHINE="$MACHINE" LABEL="$LABEL" KEY="$KEY" "$PY" - "$DEST/config.json" <<'EOF'
import json, os, sys
cfg = {
  "machine": os.environ["MACHINE"], "label": os.environ["LABEL"], "key": os.environ["KEY"],
  "url": "https://shakybetspokertools.com/auth/running/report",
  "heavy_cpu": 50, "heavy_minutes": 10,
  "watch": [
    {"name": "Example: Stud High training", "pattern": "EXAMPLE_studhi_train"}
  ]
}
json.dump(cfg, open(sys.argv[1], "w"), indent=2)
EOF
  chmod 600 "$DEST/config.json"
  echo "Wrote $DEST/config.json (edit \"watch\" to name specific jobs)"
fi

# 2. Claude Code hooks in ~/.claude/settings.json (backed up first; existing hooks are kept)
mkdir -p "$HOME/.claude"
SETTINGS="$HOME/.claude/settings.json"
[ -f "$SETTINGS" ] && cp "$SETTINGS" "$SETTINGS.bak-unfinished-business"
HOOK_CMD="$PY $DEST/hook.py" "$PY" - "$SETTINGS" <<'EOF'
import json, os, sys
path, cmd = sys.argv[1], os.environ["HOOK_CMD"]
try:
    s = json.load(open(path))
except FileNotFoundError:
    s = {}
hooks = s.setdefault("hooks", {})
for event in ("UserPromptSubmit", "Stop", "SessionEnd"):
    groups = hooks.setdefault(event, [])
    if not any("unfinished-business/hook.py" in h.get("command", "") for g in groups for h in g.get("hooks", [])):
        groups.append({"hooks": [{"type": "command", "command": cmd, "timeout": 5}]})
json.dump(s, open(path, "w"), indent=2)
EOF
echo "Claude Code hooks added to $SETTINGS (backup: $SETTINGS.bak-unfinished-business)"

# 3. launchd: run every minute while logged in
cat > "$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
  <key>Label</key><string>com.unfinishedbusiness.reporter</string>
  <key>ProgramArguments</key><array><string>$PY</string><string>$DEST/report.py</string></array>
  <key>StartInterval</key><integer>60</integer>
  <key>RunAtLoad</key><true/>
  <key>StandardErrorPath</key><string>$DEST/report.log</string>
</dict></plist>
EOF
launchctl bootout "gui/$(id -u)" "$PLIST" 2>/dev/null || true
launchctl bootstrap "gui/$(id -u)" "$PLIST"

echo "Reporter running every minute. Test it:"
"$PY" "$DEST/report.py" --verbose && echo "Report accepted by the server."
