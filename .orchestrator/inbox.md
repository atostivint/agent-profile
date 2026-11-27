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
| TEXT-1 | critique de fond du texte (destinataires mélangés, redites) | content | done | commits `7c58d60` + `7327902` + `ffc560b` ; règles déplacées en annexe, 3 callouts, contradictions et redites corrigées ; Pages `44742489324` vert, HTML live vérifié |
| PLUG-1 | ajouter Hermes Compute Priority aux listes de plugins | content | done | vérifié marketplace 200 et dépôt public non-fork ; commits `027ca67` + `0845aa1` (profil) et `466acbc` (README GitHub) ; Pages `44780173203` vert |
| MOB-1 | revue visuelle petits écrans et correctif du tableau Carrière | content | done | captures réelles 390/360 px via Edge CDP ; tableau empilé en cartes à ≤600 px (`9ef7879`, `57f8e9a`), libellés avec espace insécable ; Pages `44893635353` vert, captures vérifiées |
| MOB-2 | en-tête et estampille compacts sur mobile | content | done | `4c5b448` + `664fe89` + `e2b6da2` ; identité 1 ligne, utilitaires réduits à CV + /index.md, libellé « Canonical Markdown: » retiré ; captures 390/360 vérifiées, Pages `44895437030` vert |
| MOB-3 | supprimer la barre de fenêtre sur téléphone | content | done | `adf2977` : `.bar { display:none }` sous 600 px, `> Alexandre Tostivint` conservé ; capture 390 vérifiée, Pages `44903063516` vert |
| BIL-1 | refonte bilingue et restructuration selon les commentaires | content | done | plan Mistral Large 4 ; commits `a424066` + `457169b`, Pages `44934784531` vert ; FR/EN, logos, mois, ordre des sections, ancres et scroll-spy vérifiés en navigateur |
| DOC-1 | gouvernance bilingue et dossier img/ | agent-docs | done | `content.md`, `README.md`, `decisions.md` mis à jour |
| HIER-1 | hiérarchie humain d'abord | content | done | `dd06fbe` : ordre About → Selected work → Open source → Skills → Certs → Career → Education → Where I fit → Availability → Contact → Citing → Annexe ; index.md/AGENTS.md/html alignés, ancres préservées, annexe repliée en `<details>` ; Pages `44938887722` vert |
| MISS-1 | hook missions, signal machine, CTA dual | content | done | revue Mistral/DeepSeek/GLM ; `7eeec3e` : phrase de valeur + 3 preuves datées, section Missions (5 offres issues de faits existants), `primary_cloud=AWS` en commentaire + JSON-LD Person, CTA recruteur/projet ; 2 couches FR/EN vérifiées en navigateur, Pages `45081492064` vert |
| FIX-1 | corrections de la revue Mistral | content | done | `ae660f3` : estampille 2026-11-23 / `7eeec3e` (dernier commit de contenu), meta description conforme à la source, redites supprimées, lien Agent rules ouvrant le `<details>` ; vérifié en navigateur, Pages `45082540184` vert |
| PROFILE-1 | aligner le profil sur le CV (15/11) et le README GitHub ; nuance management ; projets ouverts ; lien CV | content | done | Skills rafraîchies, 5 projets nommés, estampille 2026-11-17, `index.md` = `AGENTS.md`, 20 liens vérifiés / 0 failing |

| HOME-1 | accueil : supprimer le vide à droite, rangée de liens humains, mots-clés humain/agent | content | done | `55a0636` ; `.win` pleine largeur, 5 pastilles par couche, `packet-capture` (humain) / `machine-signal` (agent) ; Pages `46025352134` vert, live vérifié (5+5 liens, `role=group`, estampille `ae660f3`, aucun débordement) | |

Statuts : `ready`, `blocked`, `in_progress`, `done`, `cancelled`. Les arbitrages sont dans `decisions.md`.
