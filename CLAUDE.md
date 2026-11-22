# Unfinished Business

A dashboard of every project the user works on with Claude. Each project is
In progress, Complete or Abandoned.

## Layout

- `data/projects.json` is the **only source of truth**. Edit this file, never the built copies.
- `src/app.html` is the shared UI.
- `node build.mjs` writes:
  - `docs/` holds the installable web app served by GitHub Pages. It reads `data/projects.json` live from the `main` branch.
  - `artifact/index.html` is the claude.ai Artifact (the view inside the Claude app), with the list embedded.
  - `site/ClaudesProjectDashboard.html` is the admin-only page at shakybetspokertools.com/ClaudesProjectDashboard.html.
    It reads `data/projects.json` live from `main`, so data updates need no deploy. Only a UI change needs copying into
    the ShakyBets-Site repo (`auth/ClaudesProjectDashboard.html`) and `./deploy.sh auth` from the owner's Mac.
- Claude app view (Artifact): see `ARTIFACT_URL` below.

ARTIFACT_URL: https://claude.ai/artifact/WvkEFL5j4uzG19Q17JkpCU

## Project record

```json
{
  "id": "kebab-case-unique",
  "name": "Display name",
  "area": "Poker | Games | Health | Other",
  "category": "in_progress | complete | abandoned",
  "summary": "One line: what the project is",
  "status": "Where we're at, in plain words",
  "next": "The next concrete step",
  "waiting": "What the user has to do or answer. Empty string if nothing.",
  "updated": "YYYY-MM-DD of the last real activity",
  "repos": ["RepoName"],
  "links": [{ "label": "Play", "url": "https://..." }],
  "sessions": [{ "title": "Session title", "id": "session_..." }],
  "unsure": true
}
```

`unsure: true` marks details Claude guessed. Remove it once the user confirms them.

## When the user asks to update the dashboard

1. Edit `data/projects.json`: move the category, rewrite `status`/`next`/`waiting`, bump `updated`, and set the top-level `synced` to today.
2. Run `node build.mjs`.
3. Commit and push.
4. Republish the Artifact: Artifact tool, `url` = ARTIFACT_URL, `file_path` = `artifact/index.html` (read it first if this session hasn't).

## Syncing from Claude sessions

Use `list_sessions` (mine: true) and `list_repos` from the claude-code-remote tools. For each session updated since `synced`:
- Match it to an existing project by repo or by title. Otherwise add a new project with `unsure: true`.
- Rewrite `status`, `next` and `waiting` from the session's `post_turn_summary` (`needs_action` goes into `waiting`).
- Never move a project the user filed as Complete or Abandoned back to In progress unless there is new activity on it.
- Keep it non-sensitive: no IP addresses, wallet details, passwords or personal data. This repo is public.
