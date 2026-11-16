# Registry — agent-profile

Une ligne par domaine. `session` est le `sessionID` rendu par l'outil subagent : le repasser au
worker suivant pour continuer ce domaine au lieu de repartir de zéro. `files in play` est la
surface de conflit actuelle. L'unité atomique `index.md` + générés ne peut avoir qu'une seule
tâche active, dans le domaine `content`.

| domain | session | last item | files in play | status |
|---|---|---|---|---|
| content |  |  | `index.md`, `index.html`, `llms.txt`, `AGENTS.md` (unité atomique) | idle |
| generator |  |  | `scripts/build.py`, `assets/fonts/**` | idle |
| gates |  |  | `scripts/verify_facts.py`, `scripts/check_links.py`, `.github/workflows/check.yml` | idle |
| edge |  |  | `worker/content-negotiation.js` | idle |
| agent-docs | ses_e197807efffehZ6UR7McNydL21 | ORCH-1 scaffolding + correctifs de revue | `README.md`, `.orchestrator/**`, `.opencode/domains/**` | done |

## Historique des sessions

- `ses_e197da042ffeNtGBy95KR2mI6q` (agent-docs) — scaffolding initial des 10 fichiers, puis deux
  réponses bloquées par le fournisseur. **Morte** : ne pas la réutiliser.
- `ses_e197807efffehZ6UR7McNydL21` (agent-docs) — correctifs du scaffolding, appliqués malgré deux
  réponses bloquées par le fournisseur : travail vérifié par l'orchestrateur (`build.py` idempotent,
  `verify_facts` OK, `check_links` 0 failing). Peut servir de contexte, mais le fournisseur bloque
  ses réponses : en ouvrir un neuf pour la suite.
- `ses_e19768117ffe0HPWIIw2SwSPaU` (reviewer, lecture seule) — revue de la mise en place, 7 constats
  tous traités. Réutilisable sur n'importe quel domaine.

## Règles

- Remplir `session` dès que le premier worker du domaine rend son `sessionID`. Repasser cet ID au
  worker suivant tant que le modèle est payant et que le contexte correspond au SCOPE ; en ouvrir un
  neuf quand le contexte a dérivé ou quand le fournisseur bloque la réponse.
- Session morte ou mauvaise : vider la cellule et en ouvrir une neuve. Ne jamais deviner un ID.
- Un seul item actif par domaine. Les autres attendent dans `inbox.md`.
- Mettre la ligne à jour **avant** de répondre à l'utilisateur.
- Après une compaction, ce tableau est la mémoire : le relire avant de trier quoi que ce soit.
