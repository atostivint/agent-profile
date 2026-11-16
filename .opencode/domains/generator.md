# Domaine : generator

## Possède

- `scripts/build.py` — estampille la ligne `last-modified` depuis le dernier commit touchant
  `index.md`, régénère `llms.txt` et `AGENTS.md` (copies octet pour octet) et rend `index.html`.
  Usage : `python scripts/build.py [--date YYYY-MM-DD]`. Constante `SITE_URL` en tête de fichier.
- `assets/fonts/**` — polices auto-hébergées et `fonts.css`.

## Ne possède pas

- `index.md` → `content` : le générateur consomme la source, il ne la réécrit pas (hors estampille
  `last-modified`).
- Les portes qui vérifient le résultat (`check.yml`, `verify_facts.py`, `check_links.py`) → `gates`.

## Invariants

- Aucune dépendance CDN : les polices sont auto-hébergées dans `assets/fonts/**`.
- Le HTML reste sans JavaScript, hors scroll-spy inline autorisé.
- Thème clair/sombre par variables CSS pilotées par la préférence de l'OS.
- `SITE_URL` est à changer le jour où un domaine custom est câblé ; ne pas le modifier avant.
- Un seul build à la fois : jamais deux `scripts/build.py` en parallèle sur l'unité atomique
  `index.md` + `index.html` + `llms.txt` + `AGENTS.md`.
- Le HTML généré doit rester identique à celui de la CI (voir piège markdown).

## Commandes de vérification

```powershell
python scripts/build.py
git status --porcelain
```

Le contrôle « diff vide » sur `index.md` + les trois générés se fait **après le commit**, sur arbre
propre (job `consistency`) : avant commit, `index.md` est modifié par construction.

Sur Windows, utiliser `python` : `python3` pointe vers l'alias WindowsApps.

## Pièges connus

- **Écart de version markdown** : la CI (`check.yml`) installe `markdown==3.7` alors que la machine
  a `markdown 3.8.2`. Un changement de rendu peut passer en local et casser la CI. Vérifier la
  version locale avec `python -c "import markdown; print(markdown.__version__)"` (sortie attendue
  `3.8.2`), la confronter au `markdown==3.7` de la CI, puis régénérer et comparer le rendu avant de
  conclure.
- `--date` écrase l'estampille : la CI ne l'utilise plus (correctif CI-1, 2026-11-16) et laisse
  `build.py` prendre la date du dernier commit touchant `index.md`. Un `--date` local divergent
  laisse un diff sur `index.md` et fait échouer `consistency`.
- `SITE_URL` sert aux URL absolues : le changer sans câbler le domaine custom casse les liens.

## Preuve attendue

- `git diff --stat` + le diff de `scripts/build.py` / `assets/fonts/**` et des générés.
- `python scripts/build.py` exécuté deux fois : les trois générés identiques d'un passage à
  l'autre, avec codes de sortie.
- Si le rendu a changé : comparer avec la version de la CI ; si `markdown==3.7` n'est pas disponible
  localement, le dire dans `gaps:` et ne pas conclure `OK` sur la seule version 3.8.2.
- `gaps:` si la comparaison CI n'a pas pu être faite ou si le rendu n'a pas été ouvert.

## Fils ouverts

- (aucun)
