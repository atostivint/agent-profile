#!/usr/bin/env python3
"""Build the agent-profile site from a single source of truth: index.md.

Steps:
  1. stamp the "last updated" line from the last git commit touching index.md
     (falls back to today when the repo has no history yet);
  2. regenerate llms.txt and AGENTS.md as byte-identical copies of index.md,
     so an agent that looks for either convention gets the same facts;
  3. render index.html from index.md (no client-side JS, no CDN dependency).

Usage: python3 scripts/build.py [--date YYYY-MM-DD]
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import subprocess
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "index.md"

# Change this after a custom domain is wired up (CNAME + DNS).
SITE_URL = "https://atostivint.github.io/agent-profile"
CANONICAL = f"{SITE_URL}/index.md"

STAMP_RE = re.compile(
    r"(<!-- last-modified:start -->\n)(.*?)(\n<!-- last-modified:end -->)", re.S
)


def last_commit_date() -> str | None:
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%cs", "--", "index.md"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError:
        return None
    value = out.stdout.strip()
    return value or None


def stamp(text: str, date: str) -> str:
    line = f"*Last updated: {date} · Canonical Markdown: <{CANONICAL}>*"
    new, count = STAMP_RE.subn(lambda m: m.group(1) + line + m.group(3), text)
    if count != 1:
        raise SystemExit("expected exactly one last-modified block in index.md")
    return new


PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Alexandre Tostivint — Senior Cloud Architect</title>
<meta name="description" content="Senior Cloud Architect. 10+ years in IT, 8+ years in cloud, 300+ customer environments across AWS, Azure and GCP." />
<link rel="canonical" href="__SITE_URL__/" />
<link rel="alternate" type="text/markdown" href="/index.md" title="Agent-readable profile" />
<link rel="alternate" type="application/pdf" href="https://cv.alexandre.tostivint.bzh/resume.pdf" title="CV" />
<style>
  :root {
    --ink: #1b1a17;
    --ink-soft: #4a463d;
    --muted: #6f6a5f;
    --paper: #f5f1e8;
    --paper-2: #fbf8f2;
    --rule: #d9d2c3;
    --accent: #7a4a1d;
  }
  * { box-sizing: border-box; }
  html { -webkit-text-size-adjust: 100%; }
  body {
    margin: 0;
    background: var(--paper);
    color: var(--ink);
    font: 400 17px/1.62 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    text-rendering: optimizeLegibility;
  }
  .shell { max-width: 60rem; margin: 0 auto; padding: 0 24px; }
  header.top {
    border-bottom: 1px solid var(--rule);
    background: linear-gradient(180deg, var(--paper-2), var(--paper));
  }
  header.top .shell {
    display: flex; flex-wrap: wrap; gap: 12px 24px;
    align-items: baseline; justify-content: space-between;
    padding-top: 26px; padding-bottom: 20px;
  }
  .who { font: 600 15px/1.3 ui-monospace, SFMono-Regular, Menlo, monospace;
         letter-spacing: .02em; }
  .who span { color: var(--muted); font-weight: 400; }
  .agent-link { font: 400 14px/1.4 ui-monospace, SFMono-Regular, Menlo, monospace;
                color: var(--accent); text-decoration: none;
                border: 1px solid var(--rule); border-radius: 999px; padding: 6px 14px;
                background: #fff; white-space: nowrap; }
  .agent-link:hover { border-color: var(--accent); }
  main { display: grid; grid-template-columns: minmax(0, 1fr) 16.5rem; gap: 56px;
         padding: 44px 0 72px; align-items: start; }
  .doc { min-width: 0; }
  .doc h1 { font: 500 2.6rem/1.1 "Iowan Old Style", "Palatino Linotype", Palatino, Georgia, serif;
            margin: 0 0 .5rem; letter-spacing: -.01em; }
  .doc h2 { font: 500 1.42rem/1.25 "Iowan Old Style", "Palatino Linotype", Palatino, Georgia, serif;
            margin: 2.6rem 0 .7rem; padding-top: 1.1rem; border-top: 1px solid var(--rule); }
  .doc h3 { font: 600 1.06rem/1.35 inherit; margin: 1.9rem 0 .5rem; letter-spacing: .01em; }
  .doc p, .doc li { color: var(--ink-soft); }
  .doc blockquote { margin: 0 0 1.2rem; padding: 0 0 0 18px; border-left: 3px solid var(--accent); }
  .doc blockquote p { font-size: 1.1rem; color: var(--ink); margin: 0; }
  .doc em { font-style: italic; }
  .doc a { color: var(--accent); text-decoration-thickness: 1px; text-underline-offset: 2px; }
  .doc ul, .doc ol { padding-left: 1.15rem; }
  .doc li { margin: .32rem 0; }
  .doc table { width: 100%; border-collapse: collapse; margin: 1rem 0; font-size: .95rem; }
  .doc th { text-align: left; font-weight: 600; color: var(--ink);
            border-bottom: 1px solid var(--ink); padding: 6px 10px 6px 0; }
  .doc td { border-bottom: 1px solid var(--rule); padding: 7px 10px 7px 0;
            color: var(--ink-soft); vertical-align: top; }
  .doc code { font: 400 .9em/1.4 ui-monospace, SFMono-Regular, Menlo, monospace;
              background: #ece6d9; padding: .1em .35em; border-radius: 3px; }
  .doc hr { border: 0; border-top: 1px solid var(--rule); margin: 2rem 0; }
  aside { position: sticky; top: 28px; font-size: .92rem; }
  aside .card { border: 1px solid var(--rule); border-radius: 12px; background: var(--paper-2);
                padding: 18px 18px 16px; margin-bottom: 18px; }
  aside .card h4 { margin: 0 0 .55rem; font: 600 .74rem/1.3 ui-monospace, SFMono-Regular, Menlo, monospace;
                   letter-spacing: .1em; text-transform: uppercase; color: var(--muted); }
  aside .card p { margin: 0 0 .6rem; color: var(--ink-soft); }
  aside .card p:last-child { margin-bottom: 0; }
  aside .card a { color: var(--accent); }
  aside code { font: 400 .84rem/1.5 ui-monospace, SFMono-Regular, Menlo, monospace;
               background: #ece6d9; padding: .12em .35em; border-radius: 3px; word-break: break-all; }
  .stack li { list-style: none; margin: 0 0 .45rem; }
  .stack { padding: 0; }
  footer.bottom { border-top: 1px solid var(--rule); padding: 22px 0 44px;
                  font: 400 .82rem/1.6 ui-monospace, SFMono-Regular, Menlo, monospace;
                  color: var(--muted); }
  footer.bottom a { color: var(--accent); }
  @media (max-width: 860px) {
    main { grid-template-columns: 1fr; gap: 36px; padding-top: 30px; }
    aside { position: static; }
    .doc h1 { font-size: 2.1rem; }
  }
  @media (prefers-color-scheme: dark) {
    :root {
      --ink: #f2ede2; --ink-soft: #cfc8ba; --muted: #9c9486;
      --paper: #16150f; --paper-2: #1d1b14; --rule: #332f26; --accent: #d9a86a;
    }
    .agent-link { background: #1d1b14; }
    .doc code, aside code { background: #262319; }
  }
</style>
</head>
<body>
<header class="top"><div class="shell">
  <div class="who">alexandre.tostivint <span>— senior cloud architect, Rennes</span></div>
  <a class="agent-link" href="/index.md">read this as .md →</a>
</div></header>

<div class="shell">
<main>
  <article class="doc">
__CONTENT__
  </article>

  <aside>
    <div class="card">
      <h4>This page is also a file</h4>
      <p>Agents and crawlers should read the Markdown, not this HTML:</p>
      <p><code>/index.md</code></p>
      <p>Conventions honoured: <code>/llms.txt</code>, <code>/AGENTS.md</code>. Same
      facts, one source.</p>
    </div>
    <div class="card">
      <h4>For humans</h4>
      <ul class="stack">
        <li><a href="https://cv.alexandre.tostivint.bzh/resume.pdf">CV (PDF)</a><br><span style="color:var(--muted)">the authority on detail</span></li>
        <li><a href="https://www.linkedin.com/in/alexandretostivint/">LinkedIn</a></li>
        <li><a href="https://github.com/atostivint">GitHub</a></li>
        <li><a href="https://ask.alexandre.tostivint.bzh">Ask a question</a></li>
        <li><a href="mailto:alexandre@tostivint.bzh">alexandre@tostivint.bzh</a></li>
      </ul>
    </div>
    <div class="card">
      <h4>Why this exists</h4>
      <p>An agent reading my CV PDF has to guess. This file states what I do, what I
      do not do, and what an agent must never invent about me.</p>
    </div>
  </aside>
</main>
</div>

<footer class="bottom"><div class="shell">
  __STAMP__ · Source: <a href="https://github.com/atostivint/agent-profile">atostivint/agent-profile</a>
</div></footer>
</body>
</html>
"""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", help="override the last-updated date (YYYY-MM-DD)")
    args = ap.parse_args()

    date = args.date or last_commit_date() or dt.date.today().isoformat()

    text = SOURCE.read_text(encoding="utf-8")
    text = stamp(text, date)
    SOURCE.write_text(text, encoding="utf-8")

    for twin in ("llms.txt", "AGENTS.md"):
        (ROOT / twin).write_text(text, encoding="utf-8")

    html_body = markdown.markdown(
        text,
        extensions=["tables", "attr_list", "fenced_code", "toc"],
        output_format="html5",
    )
    page = (
        PAGE.replace("__CONTENT__", html_body)
        .replace("__STAMP__", f"Last updated {date}")
        .replace("__SITE_URL__", SITE_URL)
    )
    (ROOT / "index.html").write_text(page, encoding="utf-8")

    print(f"stamped {date}")
    print("wrote llms.txt, AGENTS.md, index.html")
    print(f"site: {SITE_URL}/")


if __name__ == "__main__":
    main()
