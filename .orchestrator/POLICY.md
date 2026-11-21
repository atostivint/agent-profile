# Politique d'orchestration — agent-profile

Un profil pour agent, c'est un fichier texte. Cette politique tient en une page ; si une règle ne tient pas ici, elle n'est pas une règle.

## Règles dures

- L'orchestrateur n'écrit que dans `.orchestrator/` et `.opencode/domains/`. Tout le reste passe par un worker.
- `git status` est lu avant chaque tâche. Le travail non commité de l'utilisateur n'est pas touché.
- Réponses en français, courtes, 8 lignes maximum.
- Le brief liste des fichiers exacts. Aucun fichier hors liste ne bouge.
- `git commit` et `git push` une fois la tâche vérifiée. Tag et publication GitHub Pages sur demande explicite.
- `index.md` est la source de vérité. `AGENTS.md` en est la copie pour les agents locaux ; `index.html` est la page statique lisible rendue depuis `index.md`. Les trois forment une unité atomique : une seule tâche active, `index.md` = `AGENTS.md` octet pour octet, et `index.html` reflète le même contenu. Pas de build versionné : la resynchronisation est manuelle ou confiée à l'agent Hermes de l'utilisateur.
- `/` sert le HTML aux humains (Safari, mobile) ; `/index.md` reste le Markdown brut pour les agents, annoncé par `<link rel="alternate" type="text/markdown">`.
- Aucune expérience inventée. Le CV privé `../curriculum-vitae` fait autorité ; le vérifier à la main puisqu'il n'y a plus de porte automatique.
- `https://alexandre.tostivint.bzh/` est le **domaine public du profil** (CNAME vérifié, canonical dans `index.html`), pas un blog : l'ancien blog reste chez Hashnode à `https://hashnode.com/@atostivint`. Le CV public reste `https://cv.alexandre.tostivint.bzh/resume.pdf`. `alexandre.osyvan.bzh` ne résout pas.
- Chiffres avec leur période : « 300+ environnements clients » = base DoiT 2020–2025. Pas de tarif, salaire, TJM, téléphone ni date de disponibilité : « sur demande ». AWS est le cloud principal. Ne pas contacter la personne.

## Contrat de preuve

Un rapport n'est accepté que s'il contient :

1. `git diff --stat` et le diff des fichiers du SCOPE ;
2. chaque commande exécutée, avec son code de sortie et sa sortie pertinente ;
3. la liste des fichiers touchés, un par un, avec ce qui a changé ;
4. `gaps:` ce qui n'a pas pu être vérifié (liens, faits CV, rendu Pages).

Il n'y a plus de build ni de CI ici : ne pas inventer de commande de vérification. La vérification est `git diff --no-index index.md AGENTS.md` (doit être vide), la relecture des faits et des liens à la main, et un contrôle `git diff --exit-code` sur arbre propre après commit.

Un rapport sans diff ni commande est renvoyé une fois, puis clos en échec. Après chaque worker, l'orchestrateur relit `git status` et `git diff --stat` avant de croire le rapport.

## Routage

| Sujet | Domaine |
|---|---|
| `index.md`, `AGENTS.md`, `README.md`, `index.html`, `.nojekyll` | `content` |
| `.orchestrator/**`, `.opencode/domains/**` | `agent-docs` |

## Format de triage

```
#<ID> (reformulation) — lié : #<AUTRE>.
Domaine (session) : <domaine> (<id ou nouvelle>).
Couvre : <ce qui change>.
Non vérifié : <ce qui n'a pas pu être contrôlé>.
```

## Après chaque tâche

Mettre à jour `registry.md`, `inbox.md` et, si besoin, `decisions.md` et la note de domaine. Après une compaction, ce sont là les seules sources de mémoire.
