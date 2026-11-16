# Domaine : content

## Possède

- `index.md` — seule source de vérité du profil. Tout le contenu public en part.

## Ne possède pas

- `index.html`, `llms.txt`, `AGENTS.md` : générés par `scripts/build.py`, jamais édités à la main.
  Une correction de fond se fait dans `index.md`, puis on régénère.
- Le rendu HTML lui-même → `generator` ; les portes de vérification → `gates`.

## Invariants

- Le CV privé `../curriculum-vitae` fait autorité : aucune expérience, certification, école ou
  techno inventée. `scripts/verify_facts.py` est la porte anti-dérive.
- Les chiffres se citent avec leur période : « 300+ environnements clients » = base DoiT 2020–2025,
  ni 300 projets livrés seuls, ni 300 aujourd'hui.
- Jamais de tarif, salaire, TJM, téléphone ni date de disponibilité dans le profil : c'est « sur
  demande ». Ne contacter personne au nom d'Alexandre.
- AWS est le cloud principal ; Azure n'est pas présenté comme le premier cloud. Les services Azure
  sont une connaissance de travail.
- Nom professionnel : « Alexandre Tostivint », jamais « Elektro ».
- Après toute édition de `index.md` : `python scripts/build.py`, puis les trois générés doivent
  suivre dans le même commit — `git status --porcelain` doit lister `index.md` **et** `index.html`,
  `llms.txt`, `AGENTS.md`. Un second `build.py` ne doit plus rien changer (idempotence).
  `index.md` + générés forment une unité atomique : une seule tâche active à la fois.

## Commandes de vérification

```powershell
python scripts/build.py
git status --porcelain          # index.md et les trois générés bougent ensemble
python scripts/verify_facts.py ..\curriculum-vitae
python scripts/check_links.py
```

Le contrôle « diff vide » sur les quatre fichiers se fait **après le commit**, sur arbre propre :
c'est le job `consistency`, pas une preuve de worker.

Sur Windows, utiliser `python` : `python3` pointe vers l'alias WindowsApps.

## Pièges connus

- Éditer `llms.txt` ou `AGENTS.md` à la main donne un diff que `build.py` écrase au prochain
  passage : la modification est perdue et la CI `consistency` échoue.
- Un chiffre déplacé hors de sa période change le sens : garder la mention d'année collée au chiffre.
- La ligne `last-modified` est estampillée par `build.py` depuis le dernier commit touchant
  `index.md` : la modifier à la main ne tient pas.
- La machine a `markdown 3.8.2`, la CI installe `markdown==3.7` : un rendu HTML vérifié en local peut
  différer en CI (voir `generator`).

## Preuve attendue

- `git diff --stat` + le diff de `index.md` et des trois générés.
- `python scripts/build.py` deux fois : les trois générés identiques d'un passage à l'autre,
  puis `verify_facts.py` → `OK`, `check_links.py` → `0 failing` : commandes avec code de sortie
  et sortie. Le diff vide sur les quatre fichiers est vérifié après commit, par l'orchestrateur.
- `gaps:` si le CV privé est absent, si le réseau manque pour les liens, ou si le rendu HTML n'a pas
  été ouvert.

## Fils ouverts

- (aucun)
