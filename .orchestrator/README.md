# Espace de travail de l'orchestrateur — agent-profile

Deux fichiers techniques, deux notes de domaine. Rien de plus pour un profil qui est un fichier texte.

| Fichier | Rôle |
|---|---|
| `POLICY.md` | Règles dures, preuve, routage, format de réponse. |
| `registry.md` | Domaine → session worker, fichiers en jeu, statut. |
| `inbox.md` | Items et leur état (`ready`, `blocked`, `in_progress`, `done`, `cancelled`). |
| `decisions.md` | Arbitrages datés, une ligne chacun. |

Les notes de domaine vivent dans `.opencode/domains/`.

## Ordre de démarrage

1. `AGENTS.md` (racine) — ce que le dépôt attend d'un agent.
2. `.orchestrator/POLICY.md` — le contrat.
3. `.orchestrator/registry.md` — la session à reprendre.
4. `.orchestrator/inbox.md` — ce qu'il reste à faire.
5. `.orchestrator/decisions.md` — pourquoi c'est comme ça.
6. `.opencode/domains/<domaine>.md` — la surface exacte avant d'écrire un brief.

## La boucle

1. Prendre le prochain item de l'inbox.
2. Lire `git status`, classer contre les domaines, écrire un brief GOAL / SCOPE / ACCEPTANCE / PROOF / STOP.
3. Un worker par tâche ; aucun fichier hors SCOPE.
4. Pas de bloc PROOF → renvoyer une fois → sinon clore en échec.
5. Revue du diff en une passe, puis mise à jour de registry, inbox, décisions et note de domaine.

## À ne pas faire

- Laisser l'orchestrateur éditer un fichier du projet.
- Deux tâches actives sur `index.md` et `AGENTS.md`.
- Réintroduire un générateur, une CI ou un script de contrôle sans que l'utilisateur le demande : c'est précisément ce qui a été retiré le 2026-11-17.
- Publier sans demande explicite.
