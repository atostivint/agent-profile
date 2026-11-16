# Inbox — agent-profile

File de travail. Une ligne par item. Statuts autorisés : `ready` (prêt à partir), `blocked` (attend
une information de l'utilisateur), `in_progress`, `done` (vérifié), `cancelled`. Les décisions qui
expliquent ces items sont dans `decisions.md`.

| id | item | domain | status | note |
|---|---|---|---|---|
| ORCH-1 | mise en place de l'espace d'orchestration | agent-docs | done | 10 fichiers, revue en une passe (7 constats traités), portes vertes |
| CI-1 | `check.yml` estampille avec la date de HEAD au lieu de celle du dernier commit touchant `index.md` : tout commit hors contenu fait échouer `consistency` (run 43973960585, 11 s) | gates | done | `--date` retiré ; panne reproduite localement (exit 1) puis invariant vérifié (exit 0) ; run `43975219001` vert en 14 s |
