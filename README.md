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

## Currently running

The top of the dashboard shows what's running right now on the **MacBook Pro**, the **M4 Mini** and in the **cloud**.

One-time setup:
1. On the server, add `SB_RUNNING_KEY=<random>` to `/etc/shakybets-auth.env` (make one with `openssl rand -hex 32`),
   then `systemctl restart shakybets-auth`.
2. On each Mac, clone this repo and run `reporter/install.sh macbook "MacBook Pro"` (or `reporter/install.sh mini "M4 Mini"`
   on the Mini). Paste the same key when asked.

The installer adds three Claude Code hooks to `~/.claude/settings.json` (backed up first) and a launchd job that reports every minute.
It shows Claude Code sessions that are mid-task, plus any process using 50%+ CPU for 10+ minutes (e.g. solver training).
To give a job a friendly name, add it to `"watch"` in `~/.unfinished-business/config.json`, e.g.
`{"name": "Stud High training", "pattern": "studhi"}`. Remove everything with `reporter/uninstall.sh`.
Machines and jobs show live on the ShakyBets page only. Cloud sessions are live in the Claude app view and appear
on the ShakyBets page as of the last sync.

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
