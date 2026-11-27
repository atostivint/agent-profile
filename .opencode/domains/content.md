# Domaine : content

## Possède

- `index.md` — le profil, seule source de vérité.
- `AGENTS.md` — sa copie pour les agents qui lisent la racine du dépôt.
- `README.md`, `index.html` (page statique bilingue rendue depuis `index.md`, sans build versionné), `img/` (logos AWS et Azure copiés du CV), `.nojekyll`.

## Ne possède pas

- Le CV privé `../curriculum-vitae` : il fait autorité mais n'est pas modifiable ici.
- Les fichiers d'orchestration → `agent-docs`.

## Invariants

- `index.md` et `AGENTS.md` restent **octet pour octet identiques**. Une seule tâche active dessus à la fois ; `git diff --no-index index.md AGENTS.md` doit être vide.
- Aucune expérience inventée ; le CV fait autorité et la vérification se fait à la main depuis le 2026-11-17 (plus de `verify_facts.py`).
- Chiffres avec période ; pas de tarif, téléphone, salaire ni date de disponibilité ; AWS est le cloud principal ; ne pas contacter la personne.
- `index.html` doit rester une page statique autonome : CSS intégré, images **locales** dans `img/` autorisées (aucun CDN ni asset externe), un `<link rel="alternate" type="text/markdown" href="/index.md">`. Elle contient deux couches : `lang-en` (rendu fidèle de `index.md`, seule source de vérité des faits) et `lang-fr` (traduction manuelle). Le bouton FR/EN, `?lang=`, `localStorage` et `navigator.language` pilotent la couche visible ; les ids FR portent le suffixe `-fr` et le script réécrit les href de la nav. Les faits (chiffres, dates, liens) doivent être identiques dans les deux couches.
- Toute modification de faits dans `index.md` est répercutée dans `AGENTS.md` **et dans les deux couches de `index.html` dans le même commit**. Pas de `index.fr.md` : ce serait une seconde source de vérité à synchroniser.
- Le profil reste plat : pas de sous-dossiers pour le contenu (URL canonique `/index.md`, copie `AGENTS.md` à la racine, aucun build pour recomposer des partiels). Des détails sortants peuvent aller dans `docs/<sujet>.md` liés depuis l'annexe.
- `.nojekyll` reste présent : c'est ce qui fait servir `index.md` en texte brut par Pages.
- La rangée `.quicklinks` de `index.html` est **présentationnelle et dérivée** : elle ne contient que des liens déjà listés dans la section Contact de `index.md`. Une URL ajoutée là doit exister dans Contact, et une URL retirée de Contact doit disparaître des pastilles. Elle n'a pas à être répliquée dans `index.md`.
- Deux jetons de lecture, jamais interchangeables : `packet-capture` pour les humains (phrase « Test de lecture (pour les humains) » près de Contact, dans les deux couches) et `machine-signal` pour les agents (annexe « Appendix: rules for agents », `index.md`, `AGENTS.md`, et le bloc `<!-- machine-signal -->`). La phrase humaine doit rester explicitement adressée à un humain, sinon un agent croit devoir l'utiliser.

## Commandes de vérification

```powershell
git diff --no-index index.md AGENTS.md
git status --porcelain
git diff --exit-code -- index.md AGENTS.md README.md index.html .nojekyll
```

La dernière commande se lance **après commit**, sur arbre propre. Relire ensuite les faits dans `../curriculum-vitae` et ouvrir les liens à la main : il n'existe plus de porte automatique.

## Pièges connus

- Corriger `AGENTS.md` sans corriger `index.md` : la copie locale diverge du profil publié.
- Modifier une couche de `index.html` sans l'autre : la bascule FR/EN affiche deux versions différentes des mêmes faits. Le contrôle DOM (ids uniques, 6 logos par couche, mêmes hrefs) est obligatoire.
- Oublier le suffixe `-fr` sur un nouvel id FR : la nav mènerait à la couche masquée.
- Réintroduire un script de génération parce que la synchronisation est manuelle : ce serait réintroduire la mécanique supprimée.
- Supprimer `index.html` en croyant que Pages servira le Markdown à la racine : sans fichier d'index, l'URL racine renvoie 404.

## Preuve attendue

- `git diff --stat` et le diff des fichiers du SCOPE.
- `git diff --no-index index.md AGENTS.md` avec son code de sortie.
- Faits et liens vérifiés à la main, ou déclarés dans `gaps:`.

## Fils ouverts

- (aucun)
