#!/usr/bin/env python3
"""Check every external link in index.md resolves.

LinkedIn answers 999 (or 403) to non-browser clients; that is a bot wall, not a
dead link, so it counts as reachable. Everything else must return 2xx or 3xx.

Usage: python3 scripts/check_links.py
Exit 0 = all reachable, exit 1 = at least one dead link.
"""
from __future__ import annotations

import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
URL_RE = re.compile(r"https?://[^\s)>\]\"']+")
BOT_WALL_HOSTS = ("linkedin.com", "www.linkedin.com")
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"


def check(url: str) -> tuple[bool, str]:
    request = urllib.request.Request(url, method="GET", headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return True, f"{response.status}"
    except urllib.error.HTTPError as exc:
        if exc.code in (403, 999) and any(host in url for host in BOT_WALL_HOSTS):
            return True, f"{exc.code} (bot wall, link assumed alive)"
        return False, f"{exc.code}"
    except Exception as exc:  # noqa: BLE001 - network errors of every kind
        return False, type(exc).__name__


def main() -> int:
    text = (ROOT / "index.md").read_text(encoding="utf-8")
    urls = sorted({u.rstrip(".,;") for u in URL_RE.findall(text)})
    site = "https://atostivint.github.io/agent-profile"
    failures = 0
    for url in urls:
        if url.startswith(site):
            # The site's own canonical URL: dead until the first publish, alive
            # after. Checking it is the post-publication verification step.
            print(f"SKIP {'not published yet':>34}  {url}")
            continue
        ok, detail = check(url)
        print(f"{'OK  ' if ok else 'FAIL'} {detail:>34}  {url}")
        if not ok:
            failures += 1
    print(f"\n{len(urls)} links checked, {failures} failing")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
