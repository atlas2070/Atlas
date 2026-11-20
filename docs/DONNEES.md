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

## Questions qui retombent (`retombes.json`)
`{empreinte, q: {id: [ids des autres années]}}`. Deux questions de même matière et d'années différentes sont « la même » si au moins 3 propositions sont quasi identiques, ou 2 avec un énoncé quasi identique. Affiché sur le site par la pastille « Tombée n× » (n = nombre d'années). Recalculé tout seul par `build.py` quand les questions changent (`tools/retombes.py`).

## Statuts (`status`)
Toutes les réponses sont faites par l'équipe Atlas, à partir du cours ou, quand le cours ne suffit pas, de connaissances vérifiées. Aucune réponse ne vient d'une correction extérieure.
- **Confirmée par le cours**, **Cours** : réponse prouvée par un passage du cours (source dans `src`).
- **Rectification proposée** : réponse corrigée d'après un passage du cours (source dans `src`).
- **Équipe Atlas** : réponse faite par l'équipe, sans passage de cours qui la prouve mot pour mot.
- **Incertaine (équipe)** : réponse jugée la plus probable, mais pas sûre ; la raison est dans `note`.
- **Hors cours (connaissances générales / source externe)** : le cours ne traite pas le point.

## Sujets par parcours
- PASS : toutes les sessions de décembre 2020 à 2024.
- `lass.json` : `[{y, ids, bonus, note}]` sujets officiels L.AS bio (2022 à 2025). Pour 2020-2021 il n'y a pas de sujet L.AS officiel : ce sont les questions PASS des matières communes (message d'explication affiché sur la page Annales).
- `hb.json` : `{année: [ids]}` sujets L.AS hors-bio 2021 à 2024 (mélange de questions PASS et de questions `HB-…`).

## Historique utile
- Novembre 2026 : toutes les réponses ont été refaites à l'aveugle (sans regarder une autre correction), en plusieurs passes, puis comparées et tranchées avec le cours. Les questions où le doute reste sont en « Incertaine (équipe) ».
- 15 novembre 2026 : champ `orig` (réponse de départ) retiré des données et historique du dépôt nettoyé. Une copie privée est gardée hors du dépôt par l'administrateur.
- Types alignés sur le sujet officiel (vérifié sur le scan) : 2020-M1-30 QCS, 2022-M4-38 QCM, 2024-M1-44 QRU.

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

## Sessions 2 (novembre 2026)
- `data/data_s2.json` : 169 questions, corrigées par l'équipe à partir du cours (passages déjà cités dans Atlas) ou, à défaut, par connaissances générales (statut « Hors cours »).
  - `S2-2022-B-n` : L.AS bio, session 2 du 5 juillet 2022 (55 Q), `sk` = `s2-2022`.
  - `S2-2022-HB-n` : L.AS hors-bio, même date (54 Q). Les questions communes au sujet bio sont dupliquées avec la même correction.
  - `S2-2026-n` : L.AS bio, session 2 2025-2026 (60 Q), `sk` = `s2-2026`.
- `lass.json` : les entrées de session 2 ont un champ `sk` ; `hb.json` : clé `2022s2`.
- Appli : les clés de session `s2-AAAA` sont rangées juste avant le décembre de la même année (`isS2`, `skY`).
- Nouvelles matières (L.AS bio 2022) : « Philosophie des sciences », « Données d'évidence ».
- Les scans du sujet bio 2022 et les photos du sujet 2026 portent les croix d'un étudiant : ils ne sont pas publiés. Seules les pages de chimie du sujet hors-bio (scan propre) sont dans `public/pages/hb2022s2-*.jpg`.
- Questions « Incertaine (équipe) » : à relire avec le cours (liste dans le PDF de relecture).

## 20 novembre 2026 — calculs de pH (Biophysique)
- 2023-M2-56 (acide pyruvique) et HB-2023-36 (acide salicylique) : réponse passée de C (pH = −log C) à B (pH = ½(pKa − log C)), comme le cours 2.ph p.35-38 (acide faible, 10⁻⁵ < [H+] < 10⁻² M). L'ancienne correction utilisait un critère (pH ≤ pKa − 1) absent du cours, et ses explications se contredisaient. Note ajoutée : le calcul exact donne ≈ 4, mais le cours attend la formule de l'acide faible.
- Relecture des 60 questions de Biophysique : pas d'autre erreur de réponse ; explication C de 2020-M2-24 reformulée.
