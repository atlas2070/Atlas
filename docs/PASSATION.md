# Passation

## État actuel (novembre 2026)
- Site complet : 1 088 questions, 3 parcours, 5 onglets (Accueil, Cours, Annales, Révisions, Statistiques), mode série avec correction immédiate ou à la fin, chrono, favoris, notes perso, révision espacée des erreurs (J+1, J+3, J+7), recherche, export PDF du carnet d'erreurs.
- **Publication** : GitHub Pages, à l'adresse https://atlas2070.github.io/Atlas/. Le workflow `.github/workflows/pages.yml` lance `python3 build.py` et publie `dist/` à chaque push sur `main`.
- **Comptes (Supabase)** : connexion par code reçu par e-mail, réservée aux adresses de la table `members` (membres inscrits). Pas de mot de passe, pas d'invitation envoyée par le site.
- **Progression synchronisée** : table `progress`, une ligne par élève. Copie locale gardée, envoi au compte en différé, la version la plus récente gagne entre deux appareils, fonctionne hors ligne.
- **Onglet Membres** (admins seulement) : liste, recherche, retrait, note, import depuis un tableur (sans e-mail), signalements avec bouton « Traité ».
- **Signalements** : table `reports`. Ils ne modifient jamais une correction : l'admin vérifie dans le cours, puis corrige les données à la main en respectant les règles de `CLAUDE.md`.
- **Mode sombre** en vrai noir. Page « Mentions et confidentialité » (`src/confidentialite.html`), lien en bas de page.
- Réglages à faire dans GitHub et Supabase : **`docs/DEPLOIEMENT.md`**.

## Où est quoi dans le code
- `src/app_template.html` : l'appli (affichage, séries, statistiques, export PDF).
  - `persist()` écrit la copie locale (clé `annales-tours`) et appelle `syncTouch()`.
  - `fixState()` / `DEF_STATE()` : état par défaut et nettoyage. L'objet `state` contient tout : `ans`, `srs`, `fav`, `notes`, `run`, `parcours`, `theme`, `mode`, `chrono`.
  - `openReport()` : formulaire de signalement (envoi par `sendReport()`).
  - `exportPDF()` : export (jsPDF, CDN cdnjs).
- `src/config.js` (intégré par `build.py` au marqueur `__CONFIG__`, dans la page et dans les mentions) : réglages.
- `src/compte.js` (intégré par `build.py` au marqueur `__COMPTE__`) : tout ce qui touche à Supabase.
  - Connexion : `bootCompte()`, `screenLogin()`, `sendCode()`, `screenCode()`, `afterLogin()`, `recheck()`, `signOut()`.
  - Progression : `startApp()`, `syncInit()`, `push()`, `pullNewer()`, `flushNow()`. Métadonnées locales : clé `annales-tours-sync` (`uid`, `t` = dernière modification, `dirty`, `base`).
  - Membres et signalements : `vMembres()`, `parseEmails()`, `loadReports()`, `sendReport()`, `showQuestion()`.
- `supabase/setup.sql` : tables, fonctions (`is_admin()`, `is_member()`, `can_join(e)`), règles RLS, GRANT, déclencheur « la plus récente gagne ».

## Points d'attention
- **Données publiques** : GitHub Pages gratuit publie depuis un dépôt public. Le code, les questions et les corrections sont lisibles par tout le monde. La connexion réserve le site aux membres inscrits, elle ne cache pas les données. Pour vraiment les cacher, il faudrait servir les questions depuis Supabase (table protégée par RLS) au lieu de les mettre dans la page.
- **Contrôle d'accès** fait dans le navigateur ; les vraies protections sont les règles RLS (liste des membres, progression, signalements).
- **Pause Supabase** : projet gratuit mis en pause après 7 jours sans activité. Voir `DEPLOIEMENT.md`.
- **Hors ligne** : le site reste ouvert 30 jours après la dernière vérification de l'accès (`OFFLINE_DAYS` dans `config.js`). Il faut être en ligne pour se connecter la première fois. Il n'y a pas de cache hors ligne des pages : recharger le site sans réseau ne marche pas.
- **Déconnexion** : efface la copie locale de la progression (appareils partagés). Si un envoi est en attente (hors ligne), le site demande confirmation.
- **Ancienne progression sur claude.ai** : elle ne se transfère pas. Une sauvegarde locale d'avant les comptes (clé `annales-tours`) est reprise à la première connexion si le compte n'a pas encore de progression.
- **Réglages** dans `src/config.js` : `ORG_NAME` (nom de l'association, vide par défaut : aucun nom affiché ; s'il est rempli, il apparaît dans le sous-titre de l'écran de connexion et dans les mentions) et `CONTACT_EMAIL` (adresse e-mail Atlas, affichée dans les mentions et les messages d'erreur ; **à remplir**). Aussi l'adresse et la clé publique Supabase, et `OFFLINE_DAYS`.

## Tests
Les tests ont été faits avec la vraie bibliothèque Supabase (2.45.4) et un faux serveur Supabase simulé dans Playwright, plus `setup.sql` exécuté sur PostgreSQL 16 avec un faux schéma `auth`. Ils ne sont pas dans le dépôt. Le vrai projet Supabase et l'envoi réel des e-mails n'ont pas pu être testés.

## Ajouter un sujet plus tard
1. Recopier les questions à l'identique dans un nouveau `data/xxx.json` (même format).
2. Corrections : première correction, recoupées avec le cours ; remplir `orig`, `ans`, `status`, `src`, `note`.
3. Ajouter le fichier dans `FILES` de `build.py`. Pour L.AS bio ou hors-bio, compléter `lass.json` / `hb.json`.
4. Les images de pages vont dans `public/pages/`.
