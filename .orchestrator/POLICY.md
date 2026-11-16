# Politique d'orchestration — agent-profile

L'orchestrateur lit ce fichier au triage. Un worker ne reçoit que ce que son brief cite.

## Règles dures (non négociables)

- **L'orchestrateur n'édite un fichier du projet que dans `.orchestrator/` et
  `.opencode/domains/`.** Tout le reste passe par un worker.
- **`git commit` et `git push` sont le comportement par défaut** une fois la tâche vérifiée
  (précédent : curriculum-vitae, décision du 2026-11-11) : le travail ne reste pas en local, on ne
  redemande pas. Le **tag, la release et la publication GitHub Pages** restent sur demande explicite.
  L'utilisateur est son propre contrôle qualité : une tâche n'est « finie » qu'après sa vérification.
- **Le travail non commité de l'utilisateur est sacré.** `git status` est lu avant chaque tâche ;
  un fichier déjà modifié (ou non suivi) n'est touché que s'il est dans le SCOPE du brief.
- Réponses **en français, courtes**.
- **Aucune expérience inventée** : le CV privé `../curriculum-vitae` fait autorité et
  `scripts/verify_facts.py` est la porte. Les chiffres se citent avec leur période — « 300+
  environnements clients » est la base DoiT 2020–2025, pas 300 projets livrés seuls ni 300 aujourd'hui.
  Le nom professionnel est « Alexandre Tostivint », jamais « Elektro ».
- **Ne jamais publier de tarif, salaire, TJM, téléphone ni date de disponibilité** : ces informations
  sont « sur demande ». Ne contacter personne au nom d'Alexandre.
- **AWS est le cloud principal** ; Azure n'est pas le premier cloud. Kubernetes et CI/CD
  transfèrent, les services Azure spécifiques sont une connaissance de travail.
- **Un seul `scripts/build.py` à la fois** : `index.md` et ses trois dérivés forment une unité
  atomique. La machine sert aussi au jeu et à d'autres agents.

## Contrat de preuve

Une tâche n'est acceptée que si son bloc PROOF contient :

1. `git diff --stat` **et** le diff des fichiers du SCOPE.
2. **Chaque commande exécutée**, avec code de sortie et sortie pertinente. Minimum :
   - `python scripts/build.py` **deux fois de suite** : les trois générés doivent être identiques
     d'un passage à l'autre (`Get-FileHash index.html, llms.txt, AGENTS.md` avant/après). C'est
     l'idempotence du build, et la seule forme de preuve faisable sur un arbre déjà modifié ;
   - `python scripts/verify_facts.py ..\curriculum-vitae` (`OK`) ;
   - `python scripts/check_links.py` (`0 failing`). Sans réseau, le script compte chaque URL en
     `FAIL` et sort en erreur : ce n'est pas un `SKIP`, la porte est en échec et va dans `gaps:`.
3. La liste des fichiers touchés, un par un, avec ce qui a changé.
4. Les commandes de vérification propres au domaine (voir `.opencode/domains/<domaine>.md`).
5. `gaps:` ce qui n'a pas pu être vérifié (réseau absent, worker non déployé, rendu non ouvert).

Un rapport sans diff ni commande est **renvoyé une fois**. La deuxième fois, la tâche est close en
échec.

**Le contrôle « diff vide » se fait après le commit, jamais avant.** Avant commit, `index.md` est
modifié par construction, donc `git diff --exit-code -- index.md index.html llms.txt AGENTS.md` ne
peut pas être vide : l'exiger d'un worker rend le contrat impossible. C'est l'orchestrateur qui le
lance sur arbre propre après le commit, exactement comme le job `consistency`.

## Pas de mort silencieuse

- Un worker écrit le **code d'abord**, vérifie ensuite, rapporte enfin. Un rapport sans fichier
  modifié est un échec, même poli.
- Chaque brief finit par : « laisse le fichier dans un état compilable/vérifiable et dis exactement
  ce qui manque ; ne termine jamais sur un plan ».
- L'orchestrateur relit `git status` et `git diff --stat` après **chaque** worker, avant de lire son
  rapport. Un « ça marche » sans diff ne vaut rien.
- Un worker qui échoue deux fois sur la même tâche la voit **découpée**, pas relancée à l'identique.
- Après une compaction, `registry.md` et `inbox.md` sont la mémoire : les relire avant de trier.

## Périmètre et parallélisme

- Le brief liste des **fichiers exacts**. Aucun fichier hors liste ne bouge.
- **Unité atomique** : `index.md` + `index.html` + `llms.txt` + `AGENTS.md` (les trois derniers sont
  générés). Une seule tâche active dessus à la fois, jamais deux `scripts/build.py` en parallèle.
- Deux tâches en parallèle : fichiers **disjoints** uniquement.
- Avant de créer une tâche : `git status` puis `git worktree list`. Le travail peut déjà exister
  (branche `orch-*`, fichier non suivi). Ne jamais le dupliquer.

## Routage

| Le sujet est | Domaine |
|---|---|
| contenu du profil `index.md` | `content` |
| `scripts/build.py`, `assets/fonts/**`, rendu de `index.html` | `generator` |
| `scripts/verify_facts.py`, `scripts/check_links.py`, `.github/workflows/check.yml` | `gates` |
| `worker/content-negotiation.js` | `edge` |
| `README.md`, `.orchestrator/**`, `.opencode/domains/**` | `agent-docs` |

## Format de réponse (triage)

8 lignes maximum :

```
#<ID> (reformulation en une ligne) - lié : #<AUTRE>.
Domaine (session) : <domaine> (<id ou nouvelle>).
Couvre : <ce que le correctif change>.
Non vérifié : <réseau absent / worker non déployé / rendu non ouvert>.
```

## Après chaque tâche

- Mettre à jour `.orchestrator/registry.md` (ligne du domaine).
- Mettre à jour les « Fils ouverts » de la note de domaine si ça a bougé.
- Mettre à jour `.orchestrator/inbox.md` (statut de l'item).
- Contrôle post-commit : sur arbre propre, `git diff --exit-code -- index.md index.html llms.txt
  AGENTS.md` doit être vide — c'est ce que vérifie le job `consistency`.
- Les décisions durables vont dans `.orchestrator/decisions.md`, une ligne par arbitrage.
- L'orchestrateur ne peut rien écrire d'autre : le projet est modifié par le worker, pas par lui.
