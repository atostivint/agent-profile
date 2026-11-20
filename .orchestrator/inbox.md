# Inbox — agent-profile

| id | item | domain | status | note |
|---|---|---|---|---|
| ORCH-1 | mise en place de l'espace d'orchestration | agent-docs | done | 10 fichiers à l'époque, revue en une passe |
| CI-1 | date d'estampille de `check.yml` | gates | cancelled | correctif livré et run vert, puis workflow supprimé par SIMP-1 |
| SIMP-1 | réduire le dépôt à `index.md` + copie + redirect statique | agent-docs | done | commit `c8821f6`, −2021 lignes ; Pages vérifié : racine 200 (redirect), `/index.md` 200 `text/markdown` |
| DOM-1 | domaine `alexandre.tostivint.bzh` pour le profil | content | done | PR rouedad-infra #374 mergée, apply CI vert (0/1/0), DNS confirmé, CNAME et URL canoniques publiés, liens Blog corrigés |
| SITE-1 | page d'accueil HTML statique lisible sur mobile/Safari | content | done | commit `d0682d5`, `/` sert du HTML rendu (h1/table/style, pas de `##`), `/index.md` reste brut ; Pages `44322544985` vert |
| UI-1 | correctifs de la critique Impeccable (18/32) | content | done | commits `ded7c2d` + `743f4fa` ; mojibakes → entités, prose system-ui 16 px, métadonnées agrandies, nav et a11y ; détecteur 3 → 1 avertissement (faux positif `.util`) ; Pages `44326379397` vert |
| CONTENT-2 | aplatir index.md, ajouter faits CV et positionnement agentique, date + commit | content | done | commits `f8b27bd` + `2d10188` ; HTML régénéré, Pages `44721181574` vert, rendu vérifié via navigateur |
| TEXT-1 | critique de fond du texte (destinataires mélangés, redites) | content | pending | rapport rendu à l'utilisateur ; aucun changement appliqué sans accord |
| PROFILE-1 | aligner le profil sur le CV (15/11) et le README GitHub ; nuance management ; projets ouverts ; lien CV | content | done | Skills rafraîchies, 5 projets nommés, estampille 2026-11-17, `index.md` = `AGENTS.md`, 20 liens vérifiés / 0 failing |

Statuts : `ready`, `blocked`, `in_progress`, `done`, `cancelled`. Les arbitrages sont dans `decisions.md`.
