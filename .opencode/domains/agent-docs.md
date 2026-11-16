# Domaine : agent-docs

## Possède

- `README.md` à la racine, `.orchestrator/**`, `.opencode/domains/**`.

## Ne possède pas

- `AGENTS.md` : c'est la copie de `index.md`, domaine `content`. Une correction de fond se fait dans `index.md`, puis la copie est resynchronisée à la main.
- Le profil, le site, les scripts ou la CI : la documentation les décrit, elle ne les corrige pas.

## Invariants

- Fusionner, jamais écraser : les fichiers existants portent des consignes validées.
- Toute commande citée dans une note doit exister et avoir tourné ; il n'y a plus de build ni de CI ici.
- Aucun secret ni chemin personnel de machine dans un fichier versionné.
- Une seule source de vérité par sujet : `index.md` pour les faits, `POLICY.md` pour les règles.
- Deux domaines seulement. Ne pas recréer `generator`, `gates` ou `edge` : leurs fichiers n'existent plus.

## Commandes de vérification

```powershell
git status --porcelain
git diff --stat
Get-ChildItem .orchestrator, .opencode\domains -Recurse -File
Select-String -Path .orchestrator\*, .opencode\domains\* -Pattern 'build\.py|check_links|verify_facts|content-negotiation'
```

## Pièges connus

- Une règle posée ici ne contraint un worker que si elle figure dans son brief, dont `POLICY.md` est la source canonique.
- Laisser une note de domaine d'un fichier supprimé rend le routage faux : la supprimer en même temps que le fichier.

## Preuve attendue

- `git diff --stat` et le diff des fichiers d'orchestration.
- Commandes ci-dessus avec codes de sortie, et absence de références aux anciens scripts.
- `gaps:` ce qui n'a pas été vérifié.

## Fils ouverts

- (aucun)
