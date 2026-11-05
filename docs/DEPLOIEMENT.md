# Mettre Atlas en ligne : ce que tu dois faire toi-même

Adresse du site : **https://atlas2070.github.io/Atlas/**

Le code est prêt. Il reste des réglages à faire à la main, une seule fois, dans GitHub et dans Supabase.
Compte environ 30 minutes. Fais les étapes dans l'ordre.

> Les noms de menus ci-dessous sont ceux de Supabase fin 2026. Je n'ai pas pu ouvrir le site de Supabase
> pendant la préparation : si un menu a changé de nom, cherche le mot-clé indiqué en **gras**.

---

## 0. GitHub : activer la publication

1. Sur GitHub, ouvre le dépôt **Atlas** → **Settings** → **Pages**.
2. Dans *Build and deployment* → *Source*, choisis **GitHub Actions**.
3. Fusionne la branche de travail dans `main`. Chaque modification de `main` reconstruit et publie le site
   (onglet **Actions**, workflow « Publication », 1 à 2 minutes).
4. Ouvre https://atlas2070.github.io/Atlas/ : l'écran de connexion d'Atlas doit s'afficher.

Rappel (voir `PASSATION.md`) : avec GitHub Pages gratuit, le dépôt est public. Le code, les questions et
les corrections sont donc lisibles par tout le monde sur GitHub. La connexion réserve **le site** aux membres inscrits,
elle ne cache pas les données.

---

## 1. Créer les tables

1. Ouvre ton projet sur supabase.com.
2. Menu de gauche : **SQL Editor** → **New query**.
3. Copie tout le contenu du fichier `supabase/setup.sql` du dépôt, colle-le, clique **Run**.
4. Tu dois voir « Success. No rows returned ». Le script peut être relancé sans danger.

Il crée trois tables, toutes protégées (RLS activé) :
- `members` : la liste des membres (e-mail, rôle, note, date d'ajout) ;
- `progress` : la progression de chaque élève (une ligne par personne, lisible par elle seule) ;
- `reports` : les signalements d'erreur (seuls les admins les lisent).

## 2. T'ajouter en administrateur

Toujours dans **SQL Editor**, dans une **nouvelle** requête, remplace l'adresse par la tienne (en minuscules) :

```sql
insert into public.members(email, role) values ('ton.adresse@exemple.fr', 'admin');
```

Clique **Run**. N'écris jamais ton adresse dans le dépôt GitHub.

Pour ajouter un autre admin plus tard : onglet **Membres** du site → bouton **Rendre admin** sur sa ligne (deux clics). On ne peut pas changer son propre rôle.

## 3. Envoyer les e-mails avec Gmail

Le service d'e-mail fourni par Supabase n'envoie qu'aux membres de ton équipe Supabase, et très peu par heure.
Il faut donc brancher un compte Gmail.

### 3a. Créer un mot de passe d'application Gmail
1. Utilise de préférence un compte Gmail dédié à Atlas (ex. `atlas.annales@gmail.com`).
2. Sur https://myaccount.google.com → **Sécurité** : active la **Validation en deux étapes** (obligatoire).
3. Cherche **Mots de passe des applications** (ou va sur https://myaccount.google.com/apppasswords).
4. Nom : `Atlas Supabase` → **Créer**. Google affiche 16 lettres. Copie-les (sans les espaces).
   Tu ne pourras plus les revoir ensuite.

### 3b. Le brancher dans Supabase
**Authentication** → **Emails** → onglet **SMTP Settings** → active **Enable custom SMTP** :

| Champ | Valeur |
|---|---|
| Sender email | l'adresse Gmail elle-même (ex. `atlas.annales@gmail.com`) |
| Sender name | `Atlas` |
| Host | `smtp.gmail.com` |
| Port | `465` |
| Username | l'adresse Gmail complète |
| Password | le mot de passe d'application (16 lettres) |

Clique **Save**. Gmail impose que l'expéditeur soit l'adresse du compte : n'en mets pas une autre.

## 4. Mettre le code dans les e-mails

**Authentication** → **Emails** → onglet **Templates**. Modifie **les deux** modèles :
**Confirm signup** (envoyé à la toute première connexion d'une adresse) et **Magic Link** (les fois suivantes).

Sujet (le même pour les deux) :
```
Ton code Atlas : {{ .Token }}
```

Corps (le même pour les deux) :
```html
<h2>Connexion à Atlas</h2>
<p>Ton code :</p>
<p style="font-size:28px;font-weight:bold;letter-spacing:6px">{{ .Token }}</p>
<p>Saisis-le sur <a href="https://atlas2070.github.io/Atlas/">Atlas</a>. Il ne sert qu'une fois et expire dans une heure.</p>
<p>Tu n'as rien demandé ? Ignore cet e-mail.</p>
```

Clique **Save** pour chaque modèle. Sans `{{ .Token }}`, l'e-mail ne contient pas de code et personne ne peut se connecter.

## 5. Adresse du site

**Authentication** → **URL Configuration** :
- **Site URL** : `https://atlas2070.github.io/Atlas/`
- **Redirect URLs** → **Add URL** : `https://atlas2070.github.io/Atlas/`

**Save**.

## 6. Durée et longueur du code

**Authentication** → **Sign In / Providers** → **Email** :
- **Email OTP Expiration** : `3600` secondes (1 heure, valeur par défaut). C'est la durée annoncée dans l'e-mail.
  Si tu la changes, change aussi le texte du modèle (étape 4). Ne dépasse pas 86 400 s (un jour).
- **Email OTP Length** : `6` conseillé. Le site accepte de 6 à 10 chiffres.
- Laisse **Enable Email provider** activé. Pas besoin de « Confirm email » ni de mot de passe.

## 7. Limite d'envoi : 100 e-mails par heure

**Authentication** → **Rate Limits** → **Rate limit for sending emails** : `100` par heure → **Save**.
(Ce réglage n'apparaît qu'une fois le SMTP de l'étape 3 activé.)

À savoir :
- Par défaut, une même personne ne peut redemander un code qu'au bout de 60 secondes. Le site l'explique.
- Gmail a aussi sa propre limite par jour (environ 500 e-mails pour un compte gratuit, d'après les guides
  que j'ai trouvés ; chiffre non vérifié sur le site de Google). Pour une promo de 50 à 200 personnes, ça suffit.

## 8. Adresse de contact (et nom de l'association, si un jour tu veux l'afficher)

Ouvre `src/config.js` dans le dépôt (sur GitHub : le fichier → icône crayon) :
- `CONTACT_EMAIL:'…'` : mets l'adresse e-mail d'Atlas (par exemple celle de l'étape 3). Elle apparaît dans
  « Mentions et confidentialité » et dans les messages « contacte l'équipe Atlas ». Vide, le site dit seulement
  « l'équipe Atlas », sans adresse.
- `ORG_NAME:''` : laisse vide pour n'afficher aucun nom. Si tu le remplis, le nom apparaît dans le sous-titre de
  l'écran de connexion et dans les mentions.

Enregistre (commit sur `main`) : le site se met à jour tout seul en 1 à 2 minutes.

## 9. Tester

1. Ouvre https://atlas2070.github.io/Atlas/ dans une fenêtre privée.
2. Saisis ton adresse → tu reçois un e-mail « Ton code Atlas : 123456 » → saisis le code.
3. L'onglet **Membres** apparaît (tu es admin).
4. Essaie une adresse absente de la liste : le site doit dire « Cette adresse n'est pas dans la liste des membres. »
   et ne rien envoyer.

---

## Ajouter les membres

Onglet **Membres** du site → **Ajouter depuis un tableur** :
1. Dans ton tableur, copie la colonne des e-mails (ou tout le tableau).
2. Colle-la dans la zone, ajoute une note si tu veux (ex. `2026-2027`), clique **Voir l'aperçu**.
3. Vérifie : nouvelles adresses, déjà présentes, doublons, adresses invalides.
4. Clique **Ajouter**. **Aucun e-mail n'est envoyé** : préviens la promo toi-même (message, groupe…)
   en donnant l'adresse du site.

Retirer quelqu'un : bouton **Retirer** dans la liste. La personne est déconnectée la prochaine fois qu'elle
ouvre le site en ligne (si elle garde l'onglet ouvert, la vérification se refait toutes les 6 heures environ).

## Supprimer les données de quelqu'un (demande RGPD)

1. Onglet **Membres** → **Retirer** son adresse.
2. Supabase → **Authentication** → **Users** → cherche l'adresse → **Delete user**.
   Sa progression est supprimée avec le compte ; ses signalements restent, sans lien vers elle.

---

## Si le projet Supabase est en pause

Sur l'offre gratuite, Supabase met le projet **en pause après 7 jours sans activité** (personne ne s'est connecté
ni n'a utilisé le site). Ça arrive surtout pendant les vacances.

Ce qu'on voit : le site affiche « Connexion impossible » ou n'arrive pas à envoyer le code.
Les élèves déjà connectés sur leur appareil peuvent continuer (jusqu'à 30 jours après leur dernière
vérification) : leur progression reste sur l'appareil et sera envoyée au retour du service.

Que faire :
1. Va sur supabase.com → ton organisation → le projet (marqué *Paused*).
2. Clique **Resume project** (ou **Restore project**) et confirme. Compte quelques minutes.
3. Les données, les réglages et les modèles d'e-mail reviennent tels quels.

À savoir :
- Un projet en pause ne peut être relancé que pendant une durée limitée (90 jours ou 1 an selon les versions
  de la documentation de Supabase que j'ai trouvées : vérifie sur leur page « Project Pausing »).
  Ne le laisse pas en pause trop longtemps.
- Supabase envoie normalement un e-mail d'avertissement avant la pause.
- Pour éviter la pause : connecte-toi au site au moins une fois par semaine, ou passe à l'offre payante (Pro).

---

## Ce qui est public, ce qui est protégé

- **Public** : le code du site, les questions et les corrections (dépôt GitHub public, et la page elle-même).
  L'adresse du projet Supabase et sa clé « anon » sont dans le code : c'est normal, elles sont faites pour ça.
  **Ne mets jamais la clé `service_role` dans le dépôt.**
- **Protégé par Supabase (RLS)** : la liste des membres (seuls les admins la lisent), la progression
  (chacun lit seulement la sienne, et seulement s'il est membre), les signalements (seuls les admins les lisent).
- La vérification « est-ce un membre ? » se fait dans le navigateur. Elle réserve le site aux membres,
  mais une personne motivée peut lire le code source. C'est acceptable : il n'y a pas de secret dans les annales.

Facultatif : n'importe qui peut créer un compte Supabase vide avec la clé publique, mais sans ligne dans `members`
il ne voit rien et le site le refuse. Supabase propose un *Auth Hook « Before User Created »* pour bloquer
ces comptes dès la création, si un jour c'est utile.

---

Sources consultées (novembre 2026) :
[Supabase – Project Pausing](https://supabase.com/docs/guides/platform/free-project-pausing) ·
[Supabase – Passwordless email logins](https://supabase.com/docs/guides/auth/auth-email-passwordless) ·
[Supabase – Production checklist (limites d'e-mails)](https://supabase.com/docs/guides/deployment/going-into-prod) ·
[Guide Brevo pour le SMTP Supabase](https://developers.brevo.com/docs/supabase-smtp-integration) ·
[Réglages SMTP Gmail (Nylas)](https://developer.nylas.com/docs/cookbook/email/gmail-smtp-settings/)

## Modifier une correction depuis le site (admins)
1. Une seule fois : Supabase → SQL Editor → New query → coller le contenu de `supabase/corrections.sql` → Run.
2. Sur le site, un admin ouvre une question (par exemple avec « Voir la question » sous un signalement), affiche la correction, puis clique sur « Modifier la correction ».
3. Il coche les bonnes réponses, corrige les explications et écrit une note (obligatoire si la réponse change : ce qui la justifie dans le cours). La modification est visible par tous les membres dès leur prochain chargement.
4. « Revenir à l'original » efface la modification. L'historique (qui, quand, avant / après) est dans la table `corrections_log`.
