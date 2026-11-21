# agent-profile

An agent-facing profile of Alexandre Tostivint, published as raw Markdown on
GitHub Pages: <https://alexandre.tostivint.bzh/>. The canonical,
authoritative file is [`index.md`](index.md); everything else here is support.

## Files

| File | Role |
| ---- | ---- |
| `index.md` | Single source of truth — the agent-facing profile. Edit this one. |
| `AGENTS.md` | Local copy of `index.md`. Resynchronise by hand when the source changes. |
| `index.html` | Static bilingual page for humans. English layer rendered from `index.md`, French layer translated by hand; no build. |
| `img/` | AWS and Azure logos copied from the CV repository, served locally. |
| `.nojekyll` | Tells GitHub Pages to serve `index.md` raw as `text/markdown`. |
| `README.md` | This file. |

## Publish

Push to `main`. GitHub Pages serves the root directory; there is no build step
and no generated page to keep in sync.

## Verify by hand

Automatic gates have been removed — drift is a human responsibility again.
Before and after each edit:

1. Compare the two copies: `git diff --no-index index.md AGENTS.md` (no output
   means they match).
2. Re-read every fact in `index.md` against the CV at
   <https://cv.alexandre.tostivint.bzh/resume.pdf>.
3. Check that the links still resolve.
4. Check both language layers of `index.html`: the FR/EN switch, every section anchor, and the six certification logos in each layer.

## Rules the profile carries

Do not invent facts; quote numbers with their timeframe; state no rate or phone
number; AWS is the primary cloud, not Azure. When in doubt, say you do not know
and point to the Contact section.
