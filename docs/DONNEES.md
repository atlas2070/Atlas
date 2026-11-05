# Données

## Question (`data/*.json`, tableau d'objets)
| Champ | Sens |
|---|---|
| `id` | identifiant unique : `2023-M2-14`, `HB-2022-40`, `LAS25-54`, `PACES-…` |
| `y`, `mod`, `q` | année, module (M1, M2, M4, L.AS HB, PACES UE1…), numéro dans le sujet |
| `type` | `QCM` (plusieurs réponses) ou `QRU`/`QCS` (une seule) |
| `stem` | énoncé, recopié à l'identique (balises autorisées : `<sub>`, `<sup>`, `<i>`, `<u>` ; retour à la ligne `\n` pour un bloc de données ou un titre de question) |
| `items[]` | propositions `{l: lettre, t: texte, v: vrai/faux, ex: explication}` |
| `ans` | réponse retenue (ex. `ACD`) |
| `orig` | réponse de la première correction d'origine |
| `status` | état de la vérification (voir ci-dessous) |
| `src`, `note` | source du cours (chapitre, page) et justification |
| `mat`, `ch` | matière et chapitre |
| `crop` | `[[page, haut, bas]]` : découpe de l'image `public/pages/<page>.jpg`, en px sur une largeur ramenée à 1000 (`pw`) |
| `forceImg` | afficher l'énoncé en image (figure indispensable : structures, schémas, courbes, tableaux complexes) |
| `manual` | texte relu mot à mot sur le scan (identique au sujet) : la question s'affiche en texte, sauf si `forceImg` |
| `noFig` | l'énoncé contient un mot comme « formule » ou « tableau » mais aucune figure : ne pas passer en image pour ce mot |
| `sk`, `sl`, `gl` | clé et libellé de session (par défaut `dec<année>`) |
| `par` | parcours concernés (`pass`, `lasbio`, `lashb`) si différent du défaut |
| `annul` | question annulée |
| `ocr`, `ok`, `chAuto`, `lasn` | marqueurs internes de construction (`ocr` sans `manual` = texte non relu, affiché en image) |

## Statuts (`status`)
- **Validée** (482) : première correction et seconde correction d'accord.
- **Non comparée** (448) : première correction seule, pas de seconde source.
- **Cours** (63) : corrigée à partir du cours (pas de première correction, ex. L.AS bio 2025).
- **Correction unique** : une seule correction existe (questions de chimie PACES retirées en novembre 2026).
- **Rectification proposée** (34) : première correction contredite par un passage précis du cours ; `orig` garde l'ancienne réponse.
- **Incertaine** (30), **Maintenue** (16 : confirmée par le cours malgré un désaccord).
- **À vérifier** (4) : L.AS bio 2025 Q2, Q5, Q43, Q54. Ne pas trancher sans le cours.
- **À vérifier (cohérence)** (11) : les données de la correction se contredisent (voir `docs/COHERENCE.md`). La raison et le statut précédent sont dans `note`. Ne pas trancher sans le cours.

## Sujets par parcours
- PASS : toutes les sessions de décembre 2020 à 2024.
- `lass.json` : `[{y, ids, bonus, note}]` sujets officiels L.AS bio (2022 à 2025). Pour 2020-2021 il n'y a pas de sujet L.AS officiel : ce sont les questions PASS des matières communes (message d'explication affiché sur la page Annales).
- `hb.json` : `{année: [ids]}` sujets L.AS hors-bio 2021 à 2024 (mélange de questions PASS et de questions `HB-…`).

## Historique utile
- L.AS bio 2025 : pas de première correction, corrigé sur les cours des professeurs. Q14 C fausse (c'est le cortex préfrontal). Q54 : BCE laissée « À vérifier ».
- L.AS hors-bio 2022 : la correction PDF contenait deux questions de chimie en plus, ce qui décalait les réponses d'un cran à partir de Q38 ; corrigé. HB-2022-40 (gaz du sang) remplace une mauvaise association avec PASS 2022-M2-56.
- PASS 2023 : cahier M2 ajouté (59 questions).
- Novembre 2026 : contrôle de cohérence `python3 tools/coherence.py` (rapport `docs/COHERENCE.md`). Erreur de saisie certaine corrigée : 2024-M1-44 type QRM → QRU (le sujet indique « 44) QRU » et la rectification s'appuie sur ce format ; réponse D et `orig` DE inchangés, explication dans `note`). Passées en « À vérifier (cohérence) », sans changer les réponses : LASSP-2023-50 et HB-2023-9, HB-2022-33 et HB-2024-33, 2020-M4-32 et 2022-M4-41, HB-2022-36 et HB-2024-36 (même proposition, même énoncé, `v` opposés) ; HB-2023-12 C et HB-2024-19 A (explication qui parle d'une autre proposition) ; 2024-M4-27 (B discuté, « à confirmer »).
- Novembre 2026 : type aligné sur le sujet officiel (vérifié sur le scan) : 2020-M1-30 QCM → QCS (« 30) QCS »), 2022-M4-38 QCS → QCM (« 38) QCM »). Réponses inchangées (une seule vraie dans les deux cas, cohérent avec le nouveau type). Effet : 2020-M1-30 se note en tout ou rien, 2022-M4-38 avec la grille QCM.
- Novembre 2026 : retiré de 47 explications (`ex` de 2023-M2, HB-2023, HB-2024) la mention « - Propriété exclusive du l'auteur de la première correction » (avec le « - » final quand elle terminait le texte). Aucun autre mot touché, contrôlé par script. Restes de pied de page laissés dans ces explications, à nettoyer sur décision de l'équipe : « Page N sur 22 » (17, 2023-M2), « Correction Annales L.AS Hors -Bio Année 2024 -2025… » (15), nom de matière (4, HB-2023), caractères parasites (HB-2023-33 E).

## Affichage texte / image
Une question s'affiche en scan (`imgMode`) si : `forceImg`, ou `ocr` sans `manual`, ou un mot du filtre `FIG` dans l'énoncé (sauf `noFig`), ou `ok` faux. Sinon elle s'affiche en texte, avec « Voir l'énoncé original » replié en dessous.
Les questions dont un passage du scan est illisible sont listées dans `docs/A_RELIRE.md`.

### Relecture texte des énoncés (novembre 2026)
Les questions affichées en scan sont relues une à une sur le scan : texte corrigé à l'identique (accents, mots coupés, exposants, indices…), puis passage en texte (`manual`) ou maintien en image (`forceImg`) si une figure est indispensable. Aucune correction (`ans`, `orig`, `v`, `ex`, `status`, `src`, `note`) n'est modifiée.

Lots 1 à 40 : les 785 questions affichées en scan avant la relecture. Lots marqués * (41 et suivants) : questions qui s'affichaient déjà en texte mais avec des caractères cassés (apostrophes et parenthèses perdues, « ¶ » pour « ô », « ° » pour « î », etc.), relues de la même façon.

| Lot | Questions | Passées en texte | Gardées en image |
|---|---|---|---|
| 1 | 2020-M1-1–20 | 20 | 0 |
| 2 | 2020-M1-21–40 | 19 | 1 : 2020-M1-31 |
| 3 | 2020-M1-41–55 ; 2020-M2-1–5 | 20 | 0 |
| 4 | 2020-M2-6–25 | 3 | 17 : 2020-M2-6–13, 15–22, 25 |
| 5 | 2020-M2-26–37, 41, 44, 52–55 ; 2020-M4-1, 2 | 16 | 4 : 2020-M2-27, 34, 44, 52 |
| 6 | 2020-M4-3–22 | 20 | 0 |
| 7 | 2020-M4-23–42 | 20 | 0 |
| 8 | 2020-M4-43–55 ; 2021-M1-1–7 | 20 | 0 |
| 9 | 2021-M1-8–27 | 20 | 0 |
| 10 | 2021-M1-28–47 | 20 | 0 |
| 11 | 2021-M1-48–55 ; 2021-M2-1–12 | 13 | 7 : 2021-M2-6–12 |
| 12 | 2021-M2-13–32 | 12 | 8 : 2021-M2-13, 15–21 |
| 13 | 2021-M2-33–52 | 18 | 2 : 2021-M2-35, 40 |
| 14 | 2021-M2-53–55 ; 2021-M4-1–17 | 18 | 2 : 2021-M2-53, 55 |
| 15 | 2021-M4-18–37 | 20 | 0 |
| 16 | 2021-M4-38–55 ; 2022-M1-1, 2 | 20 | 0 |
| 17 | 2022-M1-3–22 | 20 | 0 |
| 18 | 2022-M1-23–42 | 20 | 0 |
| 19 | 2022-M1-43–55 ; 2022-M2-1–7 | 18 | 2 : 2022-M2-6, 7 |
| 20 | 2022-M2-8–27 | 8 | 12 : 2022-M2-8–13, 15–20 |
| 21 | 2022-M2-28–47 | 15 | 5 : 2022-M2-28, 32, 33, 38, 46 |
| 22 | 2022-M2-48–56 ; 2022-M4-1–11 | 20 | 0 |
| 23 | 2022-M4-12–31 | 20 | 0 |
| 24 | 2022-M4-32–51 | 20 | 0 |
| 25 | 2022-M4-52–55 ; 2023-M1-36 ; 2023-M4-48–51 ; 2024-M1-55 ; 2024-M2-6–15 | 10 | 10 : 2023-M1-36 ; 2024-M2-6–11, 13–15 |
| 26 | 2024-M2-16–23, 41, 48 ; 2024-M4-34–36 ; 2023-M2-5–11 | 4 | 16 : 2024-M2-16–23, 41, 48 ; 2023-M2-6–11 |
| 27 | 2023-M2-12–23, 25, 32, 41–43, 52 ; PACES-2019-12, 17 | 3 | 17 : 2023-M2-12–23, 32, 41, 42 ; PACES-2019-12, 17 |
| 28 | PACES-2019-15, 16, 18–20, 22–24, 27, 29 ; PACES-2018-12, 16–18, 23 ; PACES-2017-12, 16–18, 20 | 5 | 15 : PACES-2019-15, 18, 19, 22–24, 27, 29 ; PACES-2018-12, 17, 18, 23 ; PACES-2017-12, 17, 18 |
| 29 | PACES-2019-14, 21, 25, 26, 28 ; PACES-2018-14, 15, 19, 21, 22, 24, 28, 29 ; PACES-2017-14, 21, 22, 24, 26–28 | 0 | 20 : PACES-2019-14, 21, 25, 26, 28 ; PACES-2018-14, 15, 19, 21, 22, 24, 28, 29 ; PACES-2017-14, 21, 22, 24, 26–28 |
| 30 | PACES-2018-10, 11, 13, 20, 25, 26 ; PACES-2017-10, 11, 13, 15, 19, 23, 25 ; PACES-2019-10, 11, 13 ; HB-2021-12–15 | 5 | 15 : PACES-2018-10, 11, 13, 25, 26 ; PACES-2017-10, 11, 13, 15, 19, 23, 25 ; PACES-2019-10, 11, 13 |
| 31 | HB-2021-16–35 | 20 | 0 |
| 32 | HB-2021-36–55 | 17 | 3 : HB-2021-39–41 |
| 33 | HB-2022-8–27 | 20 | 0 |
| 34 | HB-2022-28–39, 41–48 | 17 | 3 : HB-2022-29–31 |
| 35 | HB-2022-49–55 ; HB-2023-8–20 | 19 | 1 : HB-2023-13 |
| 36 | HB-2023-21–40 | 19 | 1 : HB-2023-39 |
| 37 | HB-2023-41–55 ; HB-2024-8–12 | 19 | 1 : HB-2023-41 |
| 38 | HB-2024-13–32 | 18 | 2 : HB-2024-29, 31 |
| 39 | HB-2024-33–52 | 20 | 0 |
| 40 | HB-2024-53–55 ; LAS25-50, 51 | 5 | 0 |
| 41* | 2023-M1-4, 5, 7, 9, 11, 14, 16, 22, 23, 25–34, 37 | 20 | 0 |
| 42* | 2023-M1-38, 39, 41, 44, 45, 49–55 ; 2023-M4-1, 5, 9, 11, 13, 14, 16, 21 | 20 | 0 |
| 43* | 2023-M4-22, 27, 31, 35–39, 41, 42, 44, 45, 47, 52, 54, 55 ; 2024-M1-24 ; 2024-M2-2, 28, 40 | 20 | 0 |
| 44* | 2024-M2-46, 50, 51, 53, 54 ; 2023-M2-3, 30, 31, 54 ; LAS25-24, 42 | 11 | 0 |
| 45* | 2024-M2-26, 32, 37, 45, 58 (numéro de page « 10/18 »… collé à la proposition E, recadrage réduit) | 5 | 0 |

**Bilan** : 982 questions en texte, 164 en image (scan indispensable : structures, schémas, courbes, tableaux complexes). Les questions en image gardent leur texte exact (sauf propositions entièrement dessinées). Contrôle : `ans`, `orig`, `v`, `ex`, `status`, `src`, `note` identiques à la version d'avant la relecture pour les 1 146 questions. Points à vérifier par l'équipe : `docs/A_RELIRE.md`.

| Matière | Questions | En image avant | En texte après | En image après |
|---|---|---|---|---|
| Physiologie | 191 | 109 | 191 | 0 |
| Biophysique (BAME) | 75 | 50 | 71 | 4 |
| Biophysique (BMI) | 57 | 40 | 53 | 4 |
| Initiation aux médicaments | 124 | 77 | 124 | 0 |
| Chimie organique | 187 | 178 | 47 | 140 |
| Biochimie | 141 | 85 | 126 | 15 |
| Biologie cellulaire | 28 | 28 | 27 | 1 |
| Histologie | 16 | 16 | 16 | 0 |
| Biologie de la reproduction | 8 | 8 | 8 | 0 |
| Génétique | 8 | 8 | 8 | 0 |
| Anglais | 100 | 60 | 100 | 0 |
| Santé publique | 101 | 57 | 101 | 0 |
| Découverte des métiers | 110 | 69 | 110 | 0 |
| **Total** | **1146** | **785** | **982** | **164** |
- Novembre 2026 (suite) : explications nettoyées des restes de mise en page des PDF de correction (« Page N sur 22 », « Correction Annales … », noms de matière en fin de texte) et des messages d'encouragement de l'équipe de correction ; nom de la première correction retiré partout (site, statuts, sources, notes, docs). Statuts renommés : « Non comparée (correction d'origine seule) », « Incertaine (correction d'origine) », « Maintenue (correction d'origine) », « Cours (sans correction d'origine) ». Aucune réponse, aucun énoncé ni aucune proposition modifiés (contrôlé par script). Filigranes des scans PACES atténués par seuillage des gris (le texte noir et les structures restent intacts).
- Novembre 2026 : réécriture des explications à partir des cours. Les lots (questions + extraits de cours) et les réponses sont dans le dépôt privé `atlas-cours/paquets` (voir `LANCEMENT.md`). `tools/appliquer_explications.py` intègre les réponses : remplace `ex`, ajoute `exSrc: "cours"`, met `src` (« Cours : fichier p.N ») et le statut « Confirmée par le cours » ; les désaccords passent « À vérifier (désaccord avec le cours) » et sont listés dans `docs/A_TRANCHER.md`. Réponses jamais modifiées par le script.
- Novembre 2026 : 18 désaccords avec le cours tranchés (16 rectifications, 2 « Incertaine »), détail dans docs/A_TRANCHER.md.
- Novembre 2026 (fin) : 18 nouveaux désaccords tranchés (10 rectifications, 1 confirmée, 7 « Incertaine ») ; explications manquantes complétées (43 propositions) ; 3 rectifications de plus (2021-M1-6, HB-2022-36, 2024-M2-16) ; 41 questions douteuses passées « Incertaine ». Les propositions encore sans explication sont toutes dans des questions « Incertaine ». Liste complète : docs/A_TRANCHER.md.
- Novembre 2026 (fin) : 75 questions de plus passées « Confirmée par le cours » (toutes leurs propositions appuyées sur un passage précis du cours).
- Novembre 2026 (fin) : les 58 questions de chimie organique PACES 2017-2019 (scans d'une prépa privée, autorisation non établie) et leurs 39 pages scannées sont retirées du site. Il reste 1 088 questions.
- Novembre 2026 : 2e passe « preuves dans le cours » (`tools/appliquer_preuves.py`, lots dans atlas-cours/paquets/preuves) : 951 propositions de plus appuyées sur un passage des cours officiels, 185 questions de plus « Confirmée par le cours » (332 au total). 4 désaccords laissés « À vérifier », réponse inchangée (docs/A_TRANCHER_2.md). Aucune réponse modifiée.
- Novembre 2026 : 2024-M1-25 rectifiée (ACE → ABCE) sur signalement d'un élève : le cours décrit une compliance à peu près constante à bas volume, très faible seulement près de la CPT. Références à des fiches non officielles retirées de 5 notes/sources.
- 5 novembre 2026 : relecture des 76 questions Incertaine / À vérifier (cours + connaissances) : 9 rectifiées d'après un passage du cours (2020-M4-50, 2021-M1-12, 2021-M1-38, 2021-M4-27, 2022-M1-5, HB-2023-9, HB-2024-10, HB-2024-45, LAS25-3), 30 confirmées (« Maintenue »), 6 signalées « À vérifier » (connaissances ou calcul) sans changer la réponse. Liste restante : docs/A_RELIRE_HUMAIN.md.
