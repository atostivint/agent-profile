# Domaine : edge

## Possède

- `worker/content-negotiation.js` — Cloudflare Worker optionnel : sert `index.md` en Markdown sur
  `/` aux clients qui le demandent via négociation de contenu.

## Ne possède pas

- Le site GitHub Pages lui-même ni le dépôt : le Worker n'intervient que sur domaine custom.
- Les portes `gates` ni le générateur `generator` : ce Worker ne modifie aucun fichier généré.

## Invariants

- Ne sert que sur domaine custom, jamais sur `*.github.io`.
- Toute modification se vérifie en **lecture du fichier**, pas en déploiement : pas de `wrangler`
  dans le périmètre sans demande explicite.
- La publication / le déploiement du Worker reste sur demande explicite, comme tag, release et
  publication GitHub Pages.
- Le comportement de négociation (Markdown seulement quand le client le demande) reste le contrat.

## Commandes de vérification

```powershell
Get-Content worker/content-negotiation.js
git diff -- worker/content-negotiation.js
git status --porcelain
```

## Pièges connus

- Un Worker déployé sur `*.github.io` n'a pas de sens : le domaine custom doit être câblé avant,
  avec `SITE_URL` ajusté dans `scripts/build.py` (`generator`).
- Lire le fichier ne prouve pas le comportement réseau : sans déploiement, le rendu réel reste non
  vérifié et doit partir dans `gaps:`.
- `wrangler` n'est pas une commande de vérification locale ici : l'introduire sans demande sortirait
  du périmètre.

## Preuve attendue

- `git diff --stat` + le diff de `worker/content-negotiation.js`.
- Lecture du fichier après modification (contenu effectif), avec `git status --porcelain`.
- `gaps:` si le Worker n'a pas été déployé (comportement réseau non vérifié) ou si aucun domaine
  custom n'est câblé.

## Fils ouverts

- (aucun)
