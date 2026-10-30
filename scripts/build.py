#!/usr/bin/env python3
"""Build the agent-profile site from a single source of truth: index.md.

Steps:
  1. stamp the "last updated" line from the last git commit touching index.md
     (falls back to today when the repo has no history yet);
  2. regenerate llms.txt and AGENTS.md as byte-identical copies of index.md,
     so an agent that looks for either convention gets the same facts;
  3. render index.html from index.md — no CDN, fonts self-hosted in
     assets/fonts, one inline scroll-spy script.

The page follows the operating-system colour scheme: dark by default, light
when the system asks for it. Both palettes come from the same CSS variables.

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

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<meta name="color-scheme" content="dark light" />
<title>Alexandre Tostivint — Senior Cloud Architect</title>
<meta name="description" content="Senior Cloud Architect. 10+ years in IT, 8+ years in cloud, 300+ customer environments across AWS, Azure and GCP." />
<link rel="canonical" href="__SITE_URL__/" />
<link rel="alternate" type="text/markdown" href="/index.md" title="Agent-readable profile" />
<link rel="alternate" type="application/pdf" href="https://cv.alexandre.tostivint.bzh/resume.pdf" title="CV" />
<link rel="stylesheet" href="assets/fonts/fonts.css" />
<style>
  /* ---- palettes ---------------------------------------------------------
     Dark is the operator view (hard-edged, green prompt, amber headings).
     Light borrows the greys and the blue accent of the spec-sheet sketch on
     plain white, so it reads like a technical document rather than a
     washed-out terminal. Both are driven by the same variables.            */
  :root {
    --bg:#0a0c0f; --rail:#0d1117; --panel:#11151a; --chrome:#0e1216;
    --line:#232a33; --ink:#d6dee7; --head:#ffffff; --dim:#8f98a4;
    --accent:#79c0ff; --prompt:#7ee787; --subhead:#f0b429; --mark:#7d8794;
    --quote:#0d1216; --code:#161c22; --shadow:0 24px 60px rgba(0,0,0,.45);
    --rule-dot:#1c232b; --tint:rgba(214,222,231,.07);
  }
  @media (prefers-color-scheme: light) {
    :root {
      --bg:#ffffff; --rail:#f7f8fa; --panel:#ffffff; --chrome:#f3f5f8;
      --line:#e6e8eb; --ink:#333a43; --head:#14181d; --dim:#5b6470;
      --accent:#1f4fd8; --prompt:#0f7b3f; --subhead:#334155; --mark:#7b8492;
      --quote:#f8f9fb; --code:#f3f5f8; --shadow:0 18px 44px rgba(15,23,42,.08);
      --rule-dot:#e6e8eb; --tint:rgba(20,24,29,.07);
    }
  }

  * { box-sizing: border-box; }
  html { -webkit-text-size-adjust: 100%; }
  body {
    margin: 0;
    background: var(--bg);
    color: var(--ink);
    font: 400 15.5px/1.68 "IBM Plex Mono", ui-monospace, SFMono-Regular, Menlo, monospace;
    letter-spacing: -.004em;
  }
  a { color: var(--accent); text-decoration: none; border-bottom: 1px dotted var(--dim); }
  a:hover { border-bottom-style: solid; border-bottom-color: var(--accent); }
  :focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; border-radius: 2px; }

  /* ---- shell: rail + terminal window ----------------------------------- */
  .shell { display: grid; grid-template-columns: 16.5rem minmax(0, 1fr); max-width: 84rem; margin: 0 auto; }

  .rail {
    position: sticky; top: 0; align-self: start; height: 100vh;
    display: flex; flex-direction: column;
    background: var(--rail); border-right: 1px solid var(--line);
    padding: 24px 16px 18px;
  }
  .rail .nm { font-weight: 600; font-size: 13.5px; color: var(--head); }
  .rail .rl { font-size: 10.5px; text-transform: uppercase; letter-spacing: .13em; color: var(--dim); margin-top: 4px; }
  .rail .id { padding: 0 8px; margin-bottom: 22px; }
  .rail nav { display: flex; flex-direction: column; overflow: auto; }
  .rail nav a {
    color: var(--dim); font-size: 13px; line-height: 1.4; padding: 6px 8px 6px 12px;
    border: 0; border-left: 2px solid transparent;
  }
  .rail nav a:hover { color: var(--ink); background: var(--tint); }
  .rail nav a.active { color: var(--head); border-left-color: var(--prompt); background: var(--tint); font-weight: 600; }
  .rail .util { border-top: 1px solid var(--line); padding-top: 12px; margin-top: auto; }
  .rail .util a { display: flex; justify-content: space-between; gap: 10px; color: var(--ink); font-size: 12.5px; padding: 5px 8px; border: 0; }
  .rail .util a em { color: var(--dim); font-style: normal; }
  .rail .util a:hover { color: var(--accent); }
  .rail .mdlink { margin-top: 10px; padding: 0 8px; font-size: 10.5px; color: var(--dim); }
  .rail .mdlink a { border: 0; }

  main { min-width: 0; padding: 0 26px; }
  .win {
    max-width: 47rem; margin: 26px auto 40px;
    background: var(--panel); border: 1px solid var(--line); border-radius: 10px;
    overflow: hidden; box-shadow: var(--shadow);
  }
  .bar { display: flex; align-items: center; gap: 8px; padding: 11px 14px; background: var(--chrome); border-bottom: 1px solid var(--line); }
  .dot { width: 11px; height: 11px; border-radius: 50%; }
  .dot.r { background: #ff5f57; } .dot.y { background: #febc2e; } .dot.g { background: #28c840; }
  .bar .title { margin-left: 10px; color: var(--dim); font-size: 12px; letter-spacing: .01em; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .win .body { padding: 30px 34px 34px; counter-reset: work; }
  .win .body > :first-child { margin-top: 0; }

  /* ---- document -------------------------------------------------------- */
  h1 { font-size: 1.75rem; line-height: 1.25; margin: 0 0 .5rem; color: var(--head); letter-spacing: -.015em; }
  h1::before { content: "\\276F whois "; color: var(--prompt); font-weight: 400; }
  h2 {
    font-size: .88rem; text-transform: uppercase; letter-spacing: .1em; color: var(--subhead);
    margin: 2.4rem 0 .7rem; padding-bottom: .45rem; border-bottom: 1px solid var(--line);
    scroll-margin-top: 18px;
  }
  h2::before { content: "## "; color: var(--mark); }
  /* work entries: a numbered block with a hairline boundary above it, so six
     entries stop reading as one continuous list */
  h3 {
    counter-increment: work;
    font-size: 1rem; line-height: 1.35; font-weight: 600; color: var(--head);
    margin: 2.1rem 0 .6rem; padding-top: 1.2rem; border-top: 1px solid var(--line);
    letter-spacing: -.01em; scroll-margin-top: 18px;
  }
  h3::before {
    content: counter(work, decimal-leading-zero);
    color: var(--mark); font-weight: 400; margin-right: .7em;
    font-variant-numeric: tabular-nums;
  }
  /* client + period sit on their own quiet line, so a long project title never
     wraps the date onto a lonely second line */
  h3 + p { font-size: 11px; text-transform: uppercase; letter-spacing: .12em; color: var(--dim); margin: -.25rem 0 .85rem; }
  h3 + p em { font-style: normal; }
  p { margin: 0 0 1rem; }
  ul { padding-left: 1.1rem; margin: 0 0 1rem; }
  li { margin: .3rem 0; }
  li::marker { color: var(--dim); }
  strong { color: var(--head); }
  code { background: var(--code); padding: .1em .35em; border-radius: 3px; color: var(--subhead); }
  /* a blockquote closes each work entry: "Ask me about ..." */
  blockquote { margin: 1rem 0 0; padding: 7px 0 7px 12px; border-left: 2px solid var(--prompt); font-size: .92em; }
  blockquote p { margin: 0; color: var(--dim); }
  h1 + blockquote { margin: 0 0 1.4rem; padding: 10px 14px; background: var(--quote); font-size: 1em; }
  h1 + blockquote p { color: var(--ink); }
  table { width: 100%; border-collapse: collapse; margin: 1rem 0; font-size: .9rem; }
  th {
    text-align: left; color: var(--dim); font-weight: 400; text-transform: uppercase;
    font-size: .72rem; letter-spacing: .1em; padding: 6px 10px 6px 0; border-bottom: 1px solid var(--line);
  }
  td { padding: 7px 10px 7px 0; border-bottom: 1px dotted var(--rule-dot); }
  hr { border: 0; border-top: 1px solid var(--line); }

  /* the metadata line: mono, upright, quiet — a URL is not prose */
  h1 + blockquote + p { font-size: 12px; line-height: 1.6; color: var(--dim); margin: -.4rem 0 1.6rem; }
  h1 + blockquote + p em { font-style: normal; }
  h1 + blockquote + p a { display: block; margin-top: 3px; }

  /* rules for agents: real content, deliberately quiet */
  .agentnote { margin: 2.4rem 0 0; padding: 16px 18px; border: 1px dashed var(--line); border-radius: 8px; }
  .agentnote h2 { margin: 0 0 .6rem; padding: 0; border: 0; font-size: .8rem; color: var(--dim); }
  .agentnote h2::before { content: "// "; }
  .agentnote p, .agentnote li { font-size: .86rem; color: var(--dim); }
  .agentnote ul { margin: .5rem 0 0; }

  footer.page { margin-top: 2.4rem; padding-top: 14px; border-top: 1px solid var(--line);
                font-size: 11.5px; color: var(--dim); }
  footer.page a { border: 0; }

  /* ---- responsive ------------------------------------------------------ */
  @media (max-width: 900px) {
    /* minmax(0,1fr) is required: a child wider than the track (the swipeable
       nav) would otherwise grow the column and push the page off-screen */
    .shell { grid-template-columns: minmax(0, 1fr); }
    .rail, .rail nav { min-width: 0; max-width: 100%; }
    .rail {
      position: static; height: auto; flex-direction: row; flex-wrap: wrap;
      align-items: baseline; gap: 8px 16px; padding: 12px 16px;
      border-right: 0; border-bottom: 1px solid var(--line);
    }
    .rail .id { margin: 0; padding: 0; }
    /* one swipeable row instead of five wrapped rows: 12 links wrapped to ~250px
       of header on a 390px screen and pushed the profile below the fold */
    .rail nav { flex-direction: row; flex-wrap: nowrap; gap: 0 14px; overflow-x: auto;
                scrollbar-width: none; -webkit-overflow-scrolling: touch; }
    .rail nav::-webkit-scrollbar { display: none; }
    .rail nav a { border-left: 0; border-bottom: 2px solid transparent; padding: 0 2px;
                  min-height: 44px; display: inline-flex; align-items: center; white-space: nowrap; }
    .rail nav a.active { border-left: 0; border-bottom-color: var(--prompt); background: transparent; }
    .rail .mdlink { display: none; }
    .rail .util { border: 0; padding: 0; margin: 0; display: flex; flex-wrap: wrap; gap: 0 14px; }
    .rail .util a { min-height: 44px; align-items: center; padding: 0; }
    .rail .util a em { display: none; }
    main { padding: 0 12px; }
    .win { margin: 14px auto 24px; border-radius: 8px; }
    .win .body { padding: 22px 18px 26px; }
    h1 { font-size: 1.4rem; }
    body { font-size: 15px; }
  }
  @media (max-width: 430px) {
    h1::before { content: "\\276F "; }
    h1 { font-size: 1.3rem; }
  }
  @media (prefers-reduced-motion: reduce) { * { scroll-behavior: auto !important; transition: none !important; } }
  @media print {
    .rail, .bar { display: none; }
    .win { border: 0; box-shadow: none; margin: 0; max-width: none; }
    .win .body { padding: 0; }
  }
</style>
</head>
<body>
<div class="shell">
  <aside class="rail">
    <div class="id">
      <div class="nm">Alexandre Tostivint</div>
      <div class="rl">Senior Cloud Architect</div>
      <div class="rl">Rennes, France</div>
    </div>
    <nav aria-label="Sections">
__NAV__
    </nav>
    <div class="util">
      <a href="https://cv.alexandre.tostivint.bzh/resume.pdf">CV <em>PDF &#8599;</em></a>
      <a href="https://www.linkedin.com/in/alexandretostivint/">LinkedIn <em>&#8599;</em></a>
      <a href="https://github.com/atostivint">GitHub <em>&#8599;</em></a>
      <a href="mailto:alexandre@tostivint.bzh">Email <em>&#8599;</em></a>
    </div>
    <div class="mdlink"><a href="/index.md">/index.md</a> for agents</div>
  </aside>

  <main>
    <div class="win">
      <div class="bar">
        <span class="dot r"></span><span class="dot y"></span><span class="dot g"></span>
        <span class="title">alexandre@tostivint:~ % curl tostivint.bzh</span>
      </div>
      <div class="body">
__CONTENT__
        <footer class="page">__STAMP__ · <a href="https://github.com/atostivint/agent-profile">atostivint/agent-profile</a></footer>
      </div>
    </div>
  </main>
</div>
<script>
(() => {
  const links = [...document.querySelectorAll('.rail nav a')];
  const targets = links.map(a => document.getElementById(a.getAttribute('href').slice(1))).filter(Boolean);
  if (!targets.length) return;
  const on = id => links.forEach(a => a.classList.toggle('active', a.getAttribute('href') === '#' + id));
  const io = new IntersectionObserver(es => {
    const vis = es.filter(e => e.isIntersecting)
      .sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
    if (vis.length) on(vis[0].target.id);
  }, { rootMargin: '-8% 0px -72% 0px', threshold: 0 });
  targets.forEach(t => io.observe(t));
  on(targets[0].id);
})();
</script>
</body>
</html>
"""


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


def demote_agent_block(body: str) -> str:
    """Move the agent-facing preamble + rules to the end of the human page.

    The Markdown keeps its order and stays the authority; the HTML is a derived
    human view, and a recruiter should not open on "this file is written for
    you, the agent". Wording is untouched, only its position and its styling.
    """
    start = body.find('<h2 id="rules-for-using-this-file">')
    end = body.find('<h2 id="about-me">')
    if start < 0 or end < 0 or end < start:
        return body
    rules = body[start:end]
    body = body[:start] + body[end:]

    intro_start = body.find("<p>This file is written for you, the agent.")
    if intro_start >= 0:
        intro_end = body.find("</p>", intro_start) + 4
        intro = body[intro_start:intro_end]
        body = body[:intro_start] + body[intro_end:]
    else:
        intro = ""

    note = (
        '<section class="agentnote" aria-label="Rules for agents reading this page">'
        f"{intro}{rules}</section>"
    )
    contact = body.find('<h2 id="contact">')
    if contact < 0:
        return body + note
    return body[:contact] + note + body[contact:]


def nav_links(body: str) -> str:
    """Rail navigation in rendered order (the rules block moves to the end)."""
    return "\n".join(
        f'      <a href="#{frag}">{re.sub(r"<[^>]+>", "", label).strip()}</a>'
        for frag, label in re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body, re.S)
    )


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

    body = markdown.markdown(
        text,
        extensions=["tables", "attr_list", "fenced_code", "toc"],
        output_format="html5",
    )
    body = demote_agent_block(body)

    page = (
        PAGE.replace("__CONTENT__", body)
        .replace("__NAV__", nav_links(body))
        .replace("__STAMP__", f"Last updated {date}")
        .replace("__SITE_URL__", SITE_URL)
    )
    (ROOT / "index.html").write_text(page, encoding="utf-8")

    print(f"stamped {date}")
    print("wrote llms.txt, AGENTS.md, index.html")
    print(f"site: {SITE_URL}/")


if __name__ == "__main__":
    main()
