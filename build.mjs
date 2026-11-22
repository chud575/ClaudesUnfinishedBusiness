// Builds the two copies of the dashboard from src/app.html + data/projects.json:
//   docs/index.html      installable web app (GitHub Pages), reads the list live from GitHub
//   artifact/index.html  claude.ai Artifact (Claude app view), list embedded at build time
//   site/ClaudesProjectDashboard.html  admin-only page on shakybetspokertools.com, reads the list live from GitHub
// Run: node build.mjs
import { readFileSync, writeFileSync, mkdirSync, copyFileSync } from "node:fs";

const app = readFileSync("src/app.html", "utf8");
const data = readFileSync("data/projects.json", "utf8");
JSON.parse(data); // fail loudly on bad JSON

const pwaHead = `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#eceff3" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0e1319" media="(prefers-color-scheme: dark)">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Unfinished">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="icon-180.png">
<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}[hidden]{display:none!important}</style>
</head>
<body>
`;

mkdirSync("docs", { recursive: true });
writeFileSync("docs/index.html", pwaHead + app.replace("<!--CUB:CONFIG-->", `<script>window.CUB={mode:"pwa"}</script>`) + "\n</body>\n</html>\n");
copyFileSync("data/projects.json", "docs/projects.json");

// shakybetspokertools.com/ClaudesProjectDashboard.html (admins only, served by the accounts service)
mkdirSync("site", { recursive: true });
writeFileSync("site/ClaudesProjectDashboard.html", `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="robots" content="noindex,nofollow">
<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}[hidden]{display:none!important}</style>
</head>
<body>
` + app.replace("<!--CUB:CONFIG-->", `<script>window.CUB={mode:"site"}</script>`) + "\n</body>\n</html>\n");

const seed = JSON.stringify(JSON.parse(data)).replace(/</g, "\\u003c");
mkdirSync("artifact", { recursive: true });
writeFileSync("artifact/index.html", app.replace("<!--CUB:CONFIG-->", `<script>window.CUB={mode:"artifact"}</script>\n<script type="application/json" id="cub-seed">${seed}</script>`));

console.log("Built docs/index.html, artifact/index.html and site/ClaudesProjectDashboard.html");
