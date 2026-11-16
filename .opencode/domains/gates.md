# Domaine : gates

## Possède

- `scripts/verify_facts.py [chemin/vers/curriculum-vitae]` — porte anti-dérive. Le CV privé
  `../curriculum-vitae` fait autorité ; échoue si une certif, un employeur, une école, une année ou
  un chiffre compté du profil ne correspond plus, ou si un téléphone / un tarif apparaît.
  Sortie : `checked N claim groups` puis `OK` ou `DRIFT`.
- `scripts/check_links.py` — vérifie chaque URL du profil (réseau). Sortie :
  `11 links checked, 0 failing`.
- `.github/workflows/check.yml` — job `consistency` (régénère avec `build.py`, exige un
  `git diff --exit-code` vide sur `index.md index.html llms.txt AGENTS.md`, puis `check_links.py`)
  et job `drift` (clone le CV via `CV_REPO_TOKEN`, sinon job qui dit qu'il saute).

## Ne possède pas

- Le contenu vérifié (`index.md`) → `content`, ni le générateur → `generator`.
- Le déploiement du Worker → `edge`, ni la publication GitHub Pages (sur demande explicite).

## Invariants

- `verify_facts.py` doit sortir `OK` sur `../curriculum-vitae`.
- `check_links.py` doit sortir `0 failing` (11 liens attendus aujourd'hui).
- Le job `drift` saute sans `CV_REPO_TOKEN` : ne pas lire ce saut comme une vérification réussie.
  La vérification de fond se fait localement avec `verify_facts.py`.
- La CI installe `markdown==3.7` : toute modification de `check.yml` doit le rester ou le justifier.
- Un échec de porte bloque la tâche : on ne « passe » pas une porte en l'assouplissant.

## Commandes de vérification

```powershell
python scripts/verify_facts.py ..\curriculum-vitae
python scripts/check_links.py
python scripts/build.py
git status --porcelain
```

Le contrôle « diff vide » sur `index.md` + les trois générés se fait après commit, sur arbre propre
(job `consistency`) : il n'a pas sa place dans la preuve d'un worker.

Sur Windows, utiliser `python` : `python3` pointe vers l'alias WindowsApps.

## Pièges connus

- **Réseau absent** : `check_links.py` ne renvoie pas `SKIP` — chaque URL en échec réseau est comptée
  `FAIL` et le script sort en erreur (`11 links checked, 11 failing`). Une porte en échec n'est pas
  une porte passée : `0 failing` obtenu hors ligne n'a aucun sens, écrire `gaps:`.
- Le job `drift` vert sans `CV_REPO_TOKEN` ne prouve rien : il n'affiche qu'une notice « skipped ».
- Le CV privé peut être absent de `../curriculum-vitae` sur une autre machine : `verify_facts.py`
  échoue alors pour cause de chemin, pas de dérive — le dire dans `gaps:`.
- Modifier une porte pour masquer un échec détruit la protection : corriger la source (`index.md`),
  pas le test.

## Preuve attendue

- `git diff --stat` + le diff de `verify_facts.py` / `check_links.py` / `check.yml`.
- Chaque commande de vérification avec code de sortie et sortie pertinente (`OK`, `0 failing`,
  `git status --porcelain`), et le diff vide sur les quatre fichiers vérifié après commit.
- `gaps:` si le réseau manque, si le CV privé est absent, ou si la CI n'a pas été relancée.

## Fils ouverts

- (aucun)
