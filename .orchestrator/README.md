# Espace de travail de l'orchestrateur — agent-profile

Ce dossier est la mémoire de l'orchestrateur. Il est versionné pour survivre aux sessions, aux
compactions et aux reprises. Il s'adapte à un dépôt où `index.md` est la seule source de vérité et
où `index.html`, `llms.txt` et `AGENTS.md` sont générés.

| Fichier | Rôle |
|---|---|
| `POLICY.md` | Règles dures, contrat de preuve, périmètre, routage, format de réponse. Lu au triage. |
| `registry.md` | Domaine → session worker, fichiers en jeu, statut. Mémoire à long terme. |
| `inbox.md` | Items à trier et leur état (`ready`, `blocked`, `in_progress`, `done`, `cancelled`). |
| `decisions.md` | Arbitrages datés, une ligne par décision. |

Les notes de domaine vivent dans `.opencode/domains/`. `AGENTS.md` (racine) décrit ce que le dépôt
attend de tout agent ; il est généré, jamais édité ici.

## Ordre de démarrage

1. `AGENTS.md` (racine) — ce que le dépôt attend de tout agent.
2. `.orchestrator/POLICY.md` — le contrat : preuve, périmètre, interdits.
3. `.orchestrator/registry.md` — où en est chaque domaine, quelle session reprendre.
4. `.orchestrator/inbox.md` — ce qui reste à faire.
5. `.orchestrator/decisions.md` — pourquoi c'est comme ça.
6. `.opencode/domains/<domaine>.md` — la surface exacte avant d'écrire un brief.

## La boucle

1. « Prends le prochain item de `.orchestrator/inbox.md` » (ou `/triage <item>`).
2. L'orchestrateur classe l'item contre `.opencode/domains/`, lit `git status` et
   `git worktree list`, puis écrit un brief GOAL / SCOPE / ACCEPTANCE / PROOF / STOP.
3. Un `worker` par tâche indépendante, en parallèle si les fichiers sont disjoints — jamais deux
   `scripts/build.py` en parallèle sur l'unité atomique `index.md` + générés.
4. Relire `git status` et `git diff --stat` après le worker, avant son rapport.
5. Pas de bloc PROOF → renvoi une fois → sinon échec ; revue en une passe sur le diff courant.
6. L'orchestrateur met à jour `registry.md`, la note de domaine et le statut dans `inbox.md`,
   puis commit et push par défaut une fois vérifié.

## À ne pas faire

- Laisser l'orchestrateur éditer un fichier du projet : il n'écrit que dans `.orchestrator/` et
  `.opencode/domains/`, c'est interdit volontairement.
- Lancer deux items sur `index.md` : c'est une unité atomique avec `index.html`, `llms.txt` et
  `AGENTS.md`, une seule tâche active à la fois.
- Lancer deux `scripts/build.py` en parallèle : les fichiers générés se marcheraient dessus.
- Éditer à la main un fichier généré (`index.html`, `llms.txt`, `AGENTS.md`) : toute correction de
  fond se fait dans `index.md`, puis `python scripts/build.py`.
- Dupliquer un travail déjà présent sur une branche `orch-*` ou dans un fichier non commité.
- Taguer, releaser ou publier sur GitHub Pages sans que l'utilisateur le demande. Commiter et
  pousser, si (voir `.orchestrator/POLICY.md`).
