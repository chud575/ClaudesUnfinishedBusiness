# Unfinished Business

Every project you and Claude have going, and where each one stands: **In progress**, **Complete** or **Abandoned**,
plus a "Waiting on you" list of anything blocked on your answer.

## Where to open it

| Where | How |
| --- | --- |
| **shakybetspokertools.com** (main home, admins only) | Sign in, open the admin portal (`/admin`), click **Claude's project dashboard**. Direct address: `shakybetspokertools.com/ClaudesProjectDashboard.html`. Nothing public links to it, and non-admins are sent back to the home page. On a phone: open it, then Share → **Add to Home Screen**. |
| **Inside the Claude app** | Open https://claude.ai/artifact/WvkEFL5j4uzG19Q17JkpCU. Works on any phone or computer signed in to Claude, no install needed. |
| GitHub Pages (optional, public) | Not turned on. If you ever want it: Settings → Pages → `main`, folder `/docs`. |

The ShakyBets page reads `data/projects.json` live from this repo, so updates show up there without redeploying the site.
To change the page's *code*, run `node build.mjs`, copy `site/ClaudesProjectDashboard.html` into the ShakyBets-Site repo's `auth/` folder,
and run `./deploy.sh auth` from that repo.

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
