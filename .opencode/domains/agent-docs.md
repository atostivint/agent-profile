# Domaine : agent-docs

## Possède

- `README.md` à la racine.
- `.orchestrator/**` — la mémoire de l'orchestrateur (POLICY, registry, inbox, decisions).
- `.opencode/domains/**` — les notes de domaine, y compris la présente.

## Ne possède pas

- `AGENTS.md` (racine) : il est **généré** par `scripts/build.py`, copie de `index.md`. Une
  correction de fond se fait dans `index.md` (`content`), jamais dans `AGENTS.md` ; on régénère
  ensuite avec `python scripts/build.py`.
- `index.html`, `llms.txt` : générés, même règle. Les scripts, le Worker et la CI appartiennent à
  leurs domaines respectifs (`generator`, `edge`, `gates`) : la documentation les décrit, elle ne
  les corrige pas.

## Invariants

- **Fusion, jamais écrasement.** On ajoute des sections, on ne remplace pas un fichier existant
  pour y perdre des consignes validées.
- Toute commande citée doit exister sur la machine et avoir tourné au moins une fois (`python
  scripts/build.py`, `python scripts/verify_facts.py ..\curriculum-vitae`, `python
  scripts/check_links.py`, `git status --porcelain`). Sur Windows, citer `python`, pas `python3`
  (alias WindowsApps).
- Aucun secret ni chemin personnel de configuration de machine dans un fichier versionné. Le
  mapping Hindsight est déjà décidé et daté dans `decisions.md` : ne pas le recopier ici.
- Une seule source de vérité par sujet : `index.md` pour le contenu, `POLICY.md` pour les règles
  d'orchestration, la note de domaine pour la surface exacte.
- Réponses en français, courtes.

## Commandes de vérification

```powershell
python scripts/build.py
git status --porcelain
python scripts/verify_facts.py ..\curriculum-vitae
python scripts/check_links.py
Get-Command python, git | Select-Object Name, Source
```

**Contrôle anti-copie — aucun reste d'un autre projet dans la config.**
Vérifier avec le contrôle prévu au brief que les termes d'un autre dépôt n'apparaissent pas dans
`.orchestrator/` ni `.opencode/domains/`. Ne pas recopier le motif littéralement ici : la recherche
se trouverait elle-même dans ses propres résultats.

## Pièges connus

- `AGENTS.md` est généré : le corriger à la main le fait écraser au prochain `build.py` et trompe
  le job `consistency`. La bonne cible est toujours `index.md`.
- `README.md` (racine) et `POLICY.md` peuvent se recouvrir : une règle ajoutée dans l'un sans l'autre
  laisse une consigne contradictoire.
- Une règle posée ici ne contraint un worker que si elle figure dans son **brief**, dont
  `POLICY.md` est la source canonique.
- Ne pas coller le chemin absolu du fichier de configuration Hindsight : `decisions.md` porte déjà
  la décision sans exposer la configuration de la machine.

## Preuve attendue

- `git diff --stat` + le diff des fichiers `.orchestrator/` et `.opencode/domains/`.
- Chaque commande citée, exécutée, avec code de sortie ; le contrôle anti-copie sans correspondance.
- `gaps:` ce qui n'a pas été vérifié (run CI, comportement d'un agent réel).

## Fils ouverts

- (aucun)