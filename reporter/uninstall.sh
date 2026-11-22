#!/usr/bin/env bash
# Removes the reporter: stops launchd, removes the Claude Code hooks, deletes ~/.unfinished-business.
set -euo pipefail
PLIST="$HOME/Library/LaunchAgents/com.unfinishedbusiness.reporter.plist"
launchctl bootout "gui/$(id -u)" "$PLIST" 2>/dev/null || true
rm -f "$PLIST"
SETTINGS="$HOME/.claude/settings.json"
if [ -f "$SETTINGS" ]; then
  python3 - "$SETTINGS" <<'EOF'
import json, sys
path = sys.argv[1]; s = json.load(open(path))
for event, groups in list(s.get("hooks", {}).items()):
    groups[:] = [g for g in groups if not any("unfinished-business/hook.py" in h.get("command", "") for h in g.get("hooks", []))]
    if not groups:
        del s["hooks"][event]
json.dump(s, open(path, "w"), indent=2)
EOF
fi
rm -rf "$HOME/.unfinished-business"
echo "Reporter removed."
