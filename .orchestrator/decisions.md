# Décisions — agent-profile

Une ligne par arbitrage, datée. Le pourquoi est aussi important que le choix.

- **2026-11-16 — banque mémoire** : le dépôt est **routé** vers `cv-suite` par une entrée
  `mapPathToBank` de la configuration Hindsight de la machine, comme curriculum-vitae, ask, ask-dev,
  atostivint, rover-resume et resume-json. Le mapping est lu **au démarrage d'une session** : la
  session ouverte avant le changement tourne encore sur `coding-agent::agent-profile` (0 fait), et
  `cv-suite` n'est effectif qu'à la session suivante. Vérification : `hindsight_diagnose` doit rendre
  `"bank_id": "cv-suite"`. Une banque commune évite de perdre le contexte d'un dépôt à l'autre.
- **2026-11-16 — fichiers générés** : `index.html`, `llms.txt` et `AGENTS.md` ne s'éditent jamais à
  la main. Ils sont régénérés par `scripts/build.py` depuis `index.md`, seule source de vérité ; le
  fichier de départ est une copie octet pour octet, la page HTML est rendue. Une correction de fond
  se fait toujours dans `index.md`.
- **2026-11-16 — commit, push, publication** : `git commit` et `git push` sont le comportement par
  défaut une fois la tâche vérifiée (précédent curriculum-vitae, décision 2026-11-11). Le tag, la
  release et la publication GitHub Pages restent sur demande explicite : publier n'est pas
  commiter.
- **2026-11-16 — cinq domaines et unité atomique** : routage en cinq domaines (`content`,
  `generator`, `gates`, `edge`, `agent-docs`). `index.md` et ses trois fichiers générés forment une
  unité atomique : une seule tâche active dessus à la fois, jamais deux `scripts/build.py` en
  parallèle, sinon les dérivés divergent.
- **2026-11-16 — preuve avant/après commit** : un worker ne peut pas prouver un
  `git diff --exit-code` vide sur `index.md` + générés, puisque `index.md` est modifié par
  construction pendant la tâche. Sa preuve est l'**idempotence** : `build.py` deux fois de suite,
  trois générés identiques. Le diff vide sur les quatre fichiers est un contrôle **post-commit** sur
  arbre propre, celui du job `consistency`. Exiger l'inverse rendait le contrat impossible.
