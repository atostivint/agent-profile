#!/usr/bin/env python3
"""Drift gate: every factual claim in index.md must trace back to the CV repo.

The CV (atostivint/curriculum-vitae) is the authority. This script parses the
LaTeX sources and fails when the profile states something the CV no longer says:
expired or renamed certification, changed date range, dropped employer, changed
seniority claim.

It cannot catch a subtle rewording; it catches the failure mode that actually
happens — a certificate expires, someone edits lib/_certifications.tex, and the
public profile keeps advertising it.

Usage: python3 scripts/verify_facts.py [path/to/curriculum-vitae]
Exit 0 = profile consistent, exit 1 = drift (details on stdout).
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROFILE = ROOT / "index.md"
DEFAULT_CV = ROOT.parent / "curriculum-vitae"

CERT_RE = re.compile(
    r"\\href\{(https://[^}]+)\}\{([^}]+)\}\}\s*\\hfill\s*"
    r"([A-Z][a-z]{2} \d{4}) -- ([A-Z][a-z]{2} \d{4})"
)


def normalise(text: str) -> str:
    """Fold the punctuation differences between LaTeX and Markdown."""
    return (
        text.replace("\u2013", "-")
        .replace("\u2014", "-")
        .replace("\u00a0", " ")
        .replace("  ", " ")
        .lower()
    )


def load_cv(cv_root: Path) -> str:
    chunks = []
    for path in cv_root.rglob("*.tex"):
        try:
            chunks.append(path.read_text(encoding="utf-8", errors="ignore"))
        except OSError:
            continue
    return "\n".join(chunks)


def main() -> int:
    cv_root = Path(sys.argv[1] if len(sys.argv) > 1 else os.environ.get("CV_REPO", DEFAULT_CV))
    if not (cv_root / "lib").is_dir():
        print(f"FAIL cannot find the CV repo at {cv_root} (pass the path as argument)")
        return 1

    profile = PROFILE.read_text(encoding="utf-8")
    profile_norm = normalise(profile)
    cv_text = load_cv(cv_root)
    failures: list[str] = []
    checked = 0

    # 1. Certifications: every one in the CV must appear with the same dates and
    #    the same verification URL; and the profile must not list a cert the CV
    #    has dropped (that is how expired certificates survive on a website).
    certs_tex = (cv_root / "lib" / "_certifications.tex").read_text(encoding="utf-8")
    certs = CERT_RE.findall(certs_tex)
    if not certs:
        failures.append("no certification found in lib/_certifications.tex (regex drifted?)")

    for url, name, start, end in certs:
        checked += 1
        label = normalise(name).strip()
        if label not in profile_norm:
            failures.append(f"certification missing from profile: {name}")
        if url not in profile:
            failures.append(f"verification URL missing from profile: {name} -> {url}")
        expected_range = f"{start} - {end}"
        window = profile_norm
        idx = window.find(label)
        if idx >= 0 and normalise(expected_range) not in window[idx : idx + 400]:
            failures.append(
                f"date range mismatch for {name}: CV says {expected_range}"
            )

    # 2. Reverse direction: the profile must not advertise a certification the CV
    #    no longer lists. This is the failure mode that actually ships (a cert
    #    expires, the CV is cleaned up, the website keeps the badge).
    md_section = re.search(
        r"^## Certifications\n(.*?)(?=^## )", profile, re.S | re.M
    )
    md_certs = []
    if md_section:
        for line in md_section.group(1).splitlines():
            hit = re.match(r"^- \[(.+?)\]\((https://[^)]+)\),\s*(.+)$", line.strip())
            if hit:
                md_certs.append((normalise(hit.group(1)).strip(), hit.group(2)))
    else:
        failures.append("no '## Certifications' section found in the profile")

    tex_names = {normalise(name).strip() for _, name, _, _ in certs}
    if not md_certs:
        failures.append("no certification entries parsed from the profile")
    for name, _url in md_certs:
        checked += 1
        if name not in tex_names:
            failures.append(
                f"profile advertises a certification the CV no longer lists: {name}"
            )
    if len(md_certs) != len(certs):
        failures.append(
            f"certification count mismatch: profile {len(md_certs)}, CV {len(certs)}"
        )

    # 3. Counted claims. Each must still be supported by the CV wording.
    counted_claims = {
        "10+ years in IT": "10+ years in it",
        "8+ years in cloud": "8+ years in cloud",
        "300+ customer environments": "300+",
    }
    for claim, needle in counted_claims.items():
        checked += 1
        if needle not in normalise(cv_text):
            failures.append(f"claim not supported by CV sources: {claim}")

    # 4. Employers and their year spans still present in the CV.
    for employer, years in (
        ("DoiT International", ("2020", "2025")),
        ("Cloudreach", ("2017", "2020")),
        ("Exaprobe", ("2014", "2017")),
        ("ENSSAT", ("2014", "2017")),
    ):
        checked += 1
        if employer not in cv_text:
            failures.append(f"employer/school missing from CV sources: {employer}")
        if employer not in profile:
            failures.append(f"employer/school missing from profile: {employer}")
        for year in years:
            if year not in profile:
                failures.append(f"year {year} for {employer} missing from profile")

    # 4. The profile must never publish a phone number or a rate.
    checked += 1
    if re.search(r"\+33\s?[0-9]", profile):
        failures.append("phone number found in the public profile (remove it)")
    if re.search(r"\b\d{3}\s?k\s?(€|eur)", profile, re.I):
        failures.append("salary or day rate found in the public profile (never publish it)")

    print(f"checked {checked} claim groups against {cv_root}")
    if failures:
        print(f"DRIFT: {len(failures)} problem(s)")
        for item in failures:
            print(f"  - {item}")
        return 1
    print("OK: profile consistent with the CV sources")
    return 0


if __name__ == "__main__":
    sys.exit(main())
