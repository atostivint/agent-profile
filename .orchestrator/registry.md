# Registry — agent-profile

Deux domaines. `session` est le `sessionID` rendu par l'outil subagent : le repasser au worker suivant pour garder le contexte, en ouvrir un neuf si le fournisseur bloque ou si le contexte ne correspond plus.

| domain | session | last item | files in play | status |
|---|---|---|---|---|
| content | ses_de2746c98ffex4N4QclVVTm7UB | HOME-1 accueil : largeur, liens, handshake | `index.md`, `AGENTS.md`, `index.html` | done |
| agent-docs | ses_e1966539affeAMf700bj0rCssA | SIMP-1 simplification du dépôt | `.orchestrator/**`, `.opencode/domains/**` | done |

## Historique des sessions

- `ses_e197da042ffeNtGBy95KR2mI6q` — scaffolding initial, deux réponses bloquées. Morte.
- `ses_e197807efffehZ6UR7McNydL21` — correctifs du scaffolding, appliqués malgré les blocages.
- `ses_e19768117ffe0HPWIIw2SwSPaU` — reviewer, lecture seule, réutilisable.
- `ses_e196c61d3ffe2fLevsmIcMwHzp` — CI-1, workflow supprimé depuis. Morte.
- `ses_e1966539affeAMf700bj0rCssA` — SIMP-1, retrait de la mécanique.
- `ses_de2746c98ffex4N4QclVVTm7UB` — HOME-1, accueil pleine largeur, pastilles, handshake. Réutilisable pour `content`.
- `ses_de26f9f1fffeJ7zTgEDuH8DiQm` — reviewer, lecture seule, réutilisable.

## Règles

- Un seul item actif par domaine, les autres attendent dans `inbox.md`.
- Mettre la ligne à jour avant de répondre à l'utilisateur.
- Après une compaction, ce tableau et l'inbox sont la mémoire : les relire en premier.
