# Domaine : content

## Possède

- `index.md` — le profil, seule source de vérité.
- `AGENTS.md` — sa copie pour les agents qui lisent la racine du dépôt.
- `README.md`, `index.html` (redirect statique), `.nojekyll`.

## Ne possède pas

- Le CV privé `../curriculum-vitae` : il fait autorité mais n'est pas modifiable ici.
- Les fichiers d'orchestration → `agent-docs`.

## Invariants

- `index.md` et `AGENTS.md` restent **octet pour octet identiques**. Une seule tâche active dessus à la fois ; `git diff --no-index index.md AGENTS.md` doit être vide.
- Aucune expérience inventée ; le CV fait autorité et la vérification se fait à la main depuis le 2026-11-17 (plus de `verify_facts.py`).
- Chiffres avec période ; pas de tarif, téléphone, salaire ni date de disponibilité ; AWS est le cloud principal ; ne pas contacter la personne.
- `index.html` reste un redirect statique de quelques lignes vers `./index.md`, sans build : l'URL racine doit continuer à répondre.
- `.nojekyll` reste présent : c'est ce qui fait servir `index.md` en texte brut par Pages.

## Commandes de vérification

```powershell
git diff --no-index index.md AGENTS.md
git status --porcelain
git diff --exit-code -- index.md AGENTS.md README.md index.html .nojekyll
```

La dernière commande se lance **après commit**, sur arbre propre. Relire ensuite les faits dans `../curriculum-vitae` et ouvrir les liens à la main : il n'existe plus de porte automatique.

## Pièges connus

- Corriger `AGENTS.md` sans corriger `index.md` : la copie locale diverge du profil publié.
- Réintroduire un script de génération parce que la synchronisation est manuelle : ce serait réintroduire la mécanique supprimée.
- Supprimer `index.html` en croyant que Pages servira le Markdown à la racine : sans fichier d'index, l'URL racine renvoie 404.

## Preuve attendue

- `git diff --stat` et le diff des fichiers du SCOPE.
- `git diff --no-index index.md AGENTS.md` avec son code de sortie.
- Faits et liens vérifiés à la main, ou déclarés dans `gaps:`.

## Fils ouverts

- (aucun)
