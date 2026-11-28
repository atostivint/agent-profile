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

| PROJ-1 | cartes projets GitHub à la place du lien GitHub dans les pastilles | content | done | statiques, tirées de `index.md` ; 8 dépôts (les 6 + `tronic-printer-app` + `memedl`) ; `591c71b` + `e064f1b` ; bande scroll-snap, 4 badges Marketplace par couche, GitHub retiré des pastilles, impression en retour à la ligne ; Pages `46128693422` et `46129086609` verts, live vérifié | |
| STYLE-1 | retirer les marques d'écriture automatique (tirets cadratins, points de suspension, guillemets typographiques) | content | done | `dc0ecd6` ; 0 occurrence dans les trois fichiers (comptage), faits et jetons intacts, index.md = AGENTS.md | |

| PROJ-2 | cartes projets en grille au lieu de la bande à défilement | content | done | `8e4f49b` ; grille `auto-fill minmax(14rem,1fr)`, 2 colonnes sous 600 px, vérifié 756/390/360, Pages `46131702807` vert | |
| PROJ-3 | ajouter l'intégration Home Assistant (HACS) aux cartes et à `index.md` | content | done | `ha-carel-pcoweb`, Python + badge HACS, 9 cartes par couche, `8e4f49b`, live vérifié | |
| PROJ-4 | grille des projets repliable derrière un libellé | content | done | `<details>` natif fermé, `Projects (9)` / `Projets (9)`, ouverture clavier et impression vérifiées, publié dans `75d9029` | |
| ICON-1 | vignette locale par carte + correctifs de revue | content | done | 9 PNG 64×64 dans `img/projects/` (28 Ko), retrait du padding mobile, guillemets français supprimés, commentaire mis à jour ; `75d9029`, Pages `46132811205` vert, 9 images chargées en live | |

| ICON-2 | dessiner les icônes manquantes avec un modèle plus fort ; meme plus débile ; réutiliser les icônes existantes | content | done | A/B Gemini 4 Argon vs GPT-6 Luna, Gemini retenu ; `memedl` = visage débile A ; tronic/vitals/whoami conservés tels quels | |
| ICON-3 | publier les icônes dans les dépôts respectifs et dans le profil | content | done | 5 `docs/icon.svg` publiés (bc250, memedl, ha-carel, compute-priority, hindsight-plus) ; adaptive-effort avait déjà son icône dans `plugin-card@2x.png`, vectorisée sans PR ; `6d66974` + `be18cc3`, Pages `46146804523` vert, 9 assets en direct 200 | |
| ICON-4 | standardiser `docs/icon.svg` dans les 9 dépôts | content | done | PR #150 ouverte sur `hermes-adaptive-effort` (non mergée, 8 checks) ; commits directs tronic `e17abe7`, vitals `88967d2`, whoami `d6079b3` (PNG d'origine encapsulé) ; profil inchangé | |
| WRAP-1 | mesure de lecture 80 caractères, fenêtre 52 rem centrée | content | done | `e7da458` ; blanc intérieur 119 px à 1370 px au lieu de 440, marges 98/98, `overflow-wrap: anywhere` corrige les URL à 360 px ; Pages `46151622487` vert, live vérifié | |

Statuts : `ready`, `blocked`, `in_progress`, `done`, `cancelled`. Les arbitrages sont dans `decisions.md`.
