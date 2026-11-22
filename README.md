# Unfinished Business

Every project you and Claude have going, and where each one stands: **In progress**, **Complete** or **Abandoned**,
plus a "Waiting on you" list of anything blocked on your answer.

## Three ways to open it

| Where | How |
| --- | --- |
| **Phone app** (iPhone / Android) | Open the GitHub Pages URL in Safari or Chrome → Share → **Add to Home Screen**. It opens full screen like a normal app and works offline. |
| **Desktop app** (Mac / Windows) | Open the same URL in Chrome or Edge → click the install icon in the address bar (or Safari → File → **Add to Dock**). |
| **Inside the Claude app** | Open https://claude.ai/artifact/WvkEFL5j4uzG19Q17JkpCU. Works on any phone or computer signed in to Claude, no install needed. |

GitHub Pages URL (after setup): `https://chud575.github.io/ClaudesUnfinishedBusiness/`

### One-time setup for the app

1. The files have to be on the `main` branch.
2. GitHub → this repo → **Settings → Pages** → Source: *Deploy from a branch* → Branch: `main`, folder `/docs` → Save.

## Changing things

- **Ask Claude:** in a Claude Code session on this repo, say "update my dashboard" or "move Red Baron to Complete".
  `CLAUDE.md` tells Claude how.
- **From the app:** Settings → paste a fine-grained GitHub token limited to this repo with *Contents: Read and write*.
  Then you can move projects between columns, edit notes and add projects. The token stays on that device.
- **Copy resume prompt:** every project has a button that copies a "here's where we left off" message to paste into a new Claude chat.

## Files

- `data/projects.json` is the project list (the only thing that needs editing).
- `src/app.html` is the UI, shared by both builds.
- `node build.mjs` rebuilds `docs/` (the app) and `artifact/index.html` (the Claude app view).
