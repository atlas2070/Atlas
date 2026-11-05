# Atlas — consignes pour Claude Code

Site d'annales du S1 (première année santé, Tours) pour l'association (le nom n'est pas affiché : `ORG_NAME` dans `src/config.js`, vide par défaut). Trois parcours : PASS, L.AS bio, L.AS hors-bio. 1 088 questions corrigées, classées par session, matière et chapitre.

## Structure
- `src/app_template.html` : l'appli (CSS + JS). Les marqueurs `__DATA__`, `__LASS__`, `__HB__` sont remplacés au build.
- `src/config.js` : réglages (ORG_NAME, CONTACT_EMAIL, Supabase). Inséré au marqueur `__CONFIG__` dans la page et dans les mentions.
- `src/compte.js` : connexion, progression synchronisée, onglet Membres, signalements (Supabase). Inséré au marqueur `__COMPTE__`.
- `src/confidentialite.html` : page « Mentions et confidentialité ».
- `supabase/setup.sql` : tables, fonctions et règles RLS. `docs/DEPLOIEMENT.md` : réglages Supabase et GitHub.
- `data/*.json` : les questions (voir `docs/DONNEES.md`). `lass.json` = composition des sujets L.AS bio, `hb.json` = sujets L.AS hors-bio.
- `public/pages/*.jpg` : pages scannées des sujets (énoncés avec figures, recadrées à l'affichage).
- `build.py` → `dist/index.html` + `dist/confidentialite.html` + `dist/pages/`. Publié sur https://atlas2070.github.io/Atlas/ par `.github/workflows/pages.yml` (push sur `main`). Lancer : `python3 build.py`, puis servir `dist/` (ex. `python3 -m http.server -d dist`).

## Économiser les crédits
- Ne JAMAIS ouvrir un fichier `data/*.json` en entier (1,8 Mo au total). Faire des requêtes ciblées avec `python3 -c` ou `jq`.
- Ne pas lire les images sauf si une question précise l'exige.
- `src/app_template.html` fait ~1 000 lignes : chercher avec grep, lire par plages.
- Travailler par petites étapes, tester, puis passer à la suite.

## Règles de contenu (non négociables)
- Les énoncés et propositions sont repris **à l'identique** des sujets officiels. Seules les corrections peuvent être rectifiées.
- N'inventer JAMAIS une question, une réponse ou une correction.
- Une première correction n'est modifiée que si un passage précis du cours la contredit. Garder la trace : correction d'origine (`orig`), nouvelle (`ans`), source (`src` : cours, chapitre, page). En cas de doute : statut « À vérifier », ne pas trancher.
- Vérifier avant d'affirmer ; si on n'a pas pu vérifier, l'écrire.
- Ne jamais citer le nom de la prépa privée (filigranes des scans PACES) nulle part sur le site.
- Ne pas écrire de nom d'association sur le site ni dans la doc visible : dire « l'équipe Atlas » ou « l'association ». Le nom, s'il revient, passe uniquement par `ORG_NAME`.
- Si un site ou un Drive demande un identifiant : s'arrêter et demander, ne pas contourner.

## Design (validé par les utilisateurs, ne pas changer sans demande)
- Police Source Sans 3. Couleurs pastel : fond lavande `#f8f5fc`, bleu marine `#1d2c5e` (couleur principale), rose `#e2537e`, menthe `#2fa57e`. Chaque matière a sa couleur (`MCOL`).
- Violet = la réponse de l'élève, vert = la clé (bonne réponse).
- Accueil en mosaïque (blocs). Onglets : Accueil · Cours · Annales · Révisions · Statistiques.
- Textes : tutoiement, phrases courtes, pas de jargon technique.
- Mobile d'abord : tester à 390 px de large, sans défilement horizontal.

## Comptes et services
- Connexion par code e-mail (Supabase), réservée aux adresses de la table `members`. Tant que la personne n'est pas connectée et membre, seul l'écran de connexion s'affiche.
- Progression : `localStorage` (clé `annales-tours`) + table `progress` (la version la plus récente gagne).
- Signalements : table `reports` (ne modifient jamais une correction).
- Export PDF : `jsPDF` (CDN cdnjs) + `doc.save()`. Supabase JS : CDN jsDelivr, version figée.
- Ne jamais mettre la clé `service_role` dans le dépôt (la clé `anon` est publique par nature).
Voir `docs/PASSATION.md` et `docs/DEPLOIEMENT.md`.
- Ne jamais citer le nom de l’équipe de la première correction sur le site ni dans la doc : dire « première correction » ou « correction d'origine ».
- Corrections modifiées par les admins depuis le site : table Supabase `corrections` (`supabase/corrections.sql`, historique dans `corrections_log`). Elles s'appliquent par-dessus `data/*.json` au chargement. Avant de retoucher une question dans `data/`, demander à un admin d'exporter la table `corrections` pour intégrer ces changements (puis les retirer de la table).
