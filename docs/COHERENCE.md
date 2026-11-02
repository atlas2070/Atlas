# Cohérence interne des corrections

Rapport produit par `python3 tools/coherence.py` (relançable ; le script ne modifie pas les données). Classement : **erreur de saisie certaine** (les données se contredisent elles-mêmes et la bonne valeur ne fait aucun doute : corrigée, ancienne valeur gardée dans `orig` ou dans `note`, ligne dans `DONNEES.md`) ; **à vérifier dans le cours** (statut « À vérifier », rien tranché) ; **pas une anomalie** (cas signalé par le contrôle automatique puis écarté à la relecture, raison donnée).

## Bilan

| Contrôle | Cas signalés | Erreurs de saisie certaines | À vérifier dans le cours | Pas une anomalie |
|---|---|---|---|---|
| a) | 0 | 0 | 0 | 0 |
| b) | 2 | 0 | 0 | 2 |
| c) | 1 | 1 | 0 | 0 |
| d) | 2 | 0 | 2 | 0 |
| e) | 0 | 0 | 0 | 0 |
| f) | 8 | 0 | 3 | 5 |
| d) écartés d'office (sens ou contexte différent) | 242 | 0 | 0 | 242 |

## a) Réponse (`ans`) différente des propositions marquées vraies (`v`)

Aucun cas.

## b) Nombre de propositions vraies incompatible avec le type

| Question | Problème | Extrait | Classement | Relecture |
|---|---|---|---|---|
| 2020-M2-44 | QCS avec 0 proposition(s) vraie(s) (question annulée) |  | pas une anomalie |  |
| 2021-M2-44 | QCS avec 0 proposition(s) vraie(s) (question annulée) |  | pas une anomalie |  |

## c) Explication qui contredit `v` (ou le type)

Recherche : « Vrai / Faux / Exact… » au début ou à la fin de l'explication, verdict par lettre (« D vrai, E faux ») comparé aux `v`, type cité (« C'est une QRU ») comparé au champ `type`. Les explications donnent rarement un verdict explicite : ce contrôle ne peut pas repérer une explication qui dit le contraire de `v` sans employer ces mots.

| Question | Problème | Extrait | Classement | Relecture |
|---|---|---|---|---|
| 2024-M1-44 | explication / note : « C'est une QRU », type = QRM (corrigé en QRU) | C'est une QRU : une seule réponse est possible, alors que la correction d'origine en donne… | erreur de saisie certaine | Le sujet indique « 44) QRU » (scan 2024-12) et la rectification s'appuie sur « C'est une QRU », mais le champ type disait QRM. Type corrigé en QRU, réponse D inchangée. |

## d) Même proposition dans plusieurs questions, avec des `v` différents

Similarité du texte > 90 % (comparaison caractère par caractère, balises et ponctuation ignorées), questions différentes. Seuls les cas où le texte et l'énoncé sont les mêmes (et l'énoncé n'est pas un « Parmi les propositions suivantes » qui dépend d'une figure propre au sujet) sont des contradictions possibles.

| Question | Problème | Extrait | Classement | Relecture |
|---|---|---|---|---|
| LASSP-2023-50 C / HB-2023-9 C | même proposition, même énoncé (« Concernant les indicateurs de santé : ») : LASSP-2023-50 C = faux, HB-2023-9 C = vrai | La mortalité évitable correspond à la mortalité avant l’âge de 75 ans | à vérifier dans le cours | Les deux questions passent en « À vérifier » : seul le cours peut dire laquelle est juste. |
| 2020-M4-32 B / 2022-M4-41 B | même proposition, même énoncé (« Le pharmacien hospitalier peut avoir comme mi… ») : 2020-M4-32 B = vrai, 2022-M4-41 B = faux | la production des chimiothérapies ; | à vérifier dans le cours | Les deux questions passent en « À vérifier » : seul le cours peut dire laquelle est juste. |

Cas écartés d'office (pas une anomalie) :

<details><summary>un mot change (sens différent) : 168</summary>

- 2020-M1-1 C (V) / 2024-M1-9 C (F) : amont aval
- 2024-M1-9 C (F) / LAS25-15 C (V) : aval amont
- 2020-M2-16 A (V) / 2021-M2-16 A (F) : aldehyde cetone
- 2020-M2-16 A (V) / 2022-M2-16 B (F) : aldehyde cetone
- 2020-M2-16 A (V) / 2024-M2-19 B (F) : aldehyde cetone
- 2020-M2-16 A (V) / 2023-M2-19 B (F) : aldehyde cetone
- 2020-M1-3 B (V) / 2021-M1-49 D (F) : trophotrope ergotrope
- 2021-M1-49 D (F) / 2023-M1-23 C (V) : ergotrope trophotrope
- 2024-M1-12 A (F) / HB-2024-45 C (V) : k na k na
- 2022-M2-56 D (F) / 2024-M2-52 D (V) : diminution augmentation
- 2022-M2-56 D (F) / HB-2022-40 D (V) : diminution augmentation
- 2024-M2-52 D (V) / HB-2022-40 C (F) : augmentation diminution
- 2021-M1-31 C (F) / 2022-M1-10 E (V) : favorise  oppose
- 2021-M1-31 C (F) / 2023-M1-4 E (V) : favorise  oppose
- 2021-M1-31 C (F) / LAS25-19 D (V) : favorise  oppose
- 2023-M1-22 C (V) / HB-2021-43 D (F) : asymetrique symetrique
- 2021-M1-43 B (V) / 2024-M1-6 B (F) : indirecte directe lente rapide
- 2024-M1-6 B (F) / LAS25-12 A (V) : rapide lente
- 2022-M1-10 B (F) / HB-2022-52 C (V) : 60 120
- 2022-M1-10 B (F) / HB-2024-42 B (V) : 60 120 par minute
- 2023-M1-4 B (F) / HB-2022-52 C (V) : 60 120
- 2023-M1-4 B (F) / HB-2024-42 B (V) : 60 120 par minute
- 2022-M1-10 D (V) / 2024-M1-4 D (F) : vasoconstriction vasodilatation
- 2023-M1-4 D (V) / 2024-M1-4 D (F) : vasoconstriction vasodilatation
- 2024-M1-4 D (F) / LAS25-19 E (V) : vasodilatation vasoconstriction
- 2020-M2-5 D (V) / 2021-M2-5 D (F) : c3h6o3 nh3 g
- 2023-M1-9 B (V) / HB-2024-47 A (F) : egale inferieure
- 2023-M1-9 C (V) / HB-2024-47 A (F) : pleurale alveolaire
- 2023-M1-10 B (V) / HB-2021-45 C (F) : inferieure superieure
- 2024-M1-26 B (V) / HB-2024-47 A (F) : pleurale alveolaire
- HB-2023-52 D (V) / HB-2024-55 D (F) : permettent permet
- 2020-M1-43 A (F) / 2024-M1-46 C (V) : depolarisation hyperpolarisation
- 2020-M1-43 B (F) / 2023-M1-52 D (V) : activateur inhibiteur
- 2020-M1-43 B (F) / 2024-M1-46 D (V) : activateur inhibiteur
- 2023-M1-52 C (F) / 2024-M1-46 C (V) : depolarisation hyperpolarisation
- 2020-M1-43 A (F) / 2024-M1-46 A (V) : anionique cationique
- 2023-M1-52 C (F) / 2024-M1-46 A (V) : anionique cationique
- 2024-M1-46 A (V) / LAS25-31 A (F) : cationique sodique
- 2024-M1-46 A (V) / LAS25-31 D (F) : cationique calcique
- 2020-M1-43 D (V) / 2023-M1-52 C (F) : cationique anionique
- 2020-M1-43 D (V) / LAS25-31 A (F) : cationique sodique
- 2020-M1-43 D (V) / LAS25-31 D (F) : cationique calcique
- 2020-M1-43 B (F) / 2023-M1-52 B (V) : anionique cationique activateur excitateur
- 2020-M1-43 B (F) / 2024-M1-46 B (V) : anionique cationique activateur excitateur
- 2020-M1-43 D (V) / 2023-M1-52 A (F) : depolarisation hyperpolarisation
- 2023-M1-52 A (F) / 2024-M1-46 A (V) : hyperpolarisation depolarisation
- 2020-M1-44 A (V) / HB-2022-48 D (F) : ce principe actif cette
- 2022-M1-45 C (V) / 2023-M1-53 C (F) : dopaminergique histaminergique h1 5ht2
- 2022-M1-45 D (V) / 2023-M1-53 C (F) : serotoninergique histaminergique h1 histaminergique
- 2022-M1-45 D (V) / HB-2022-48 D (F) : 5ht2 histaminergique dopaminergique d2
- HB-2021-53 C (V) / HB-2022-48 D (F) : ce principe actif cette
- 2023-M1-53 A (V) / HB-2022-48 B (F) : ne pa
- 2021-M2-12 E (F) / 2022-M2-9 E (V) : i g
- 2022-M2-9 E (V) / 2022-M2-12 D (F) : g i
- 2021-M2-27 D (V) / 2021-M2-28 E (F) : arn adn
- 2020-M1-47 E (V) / 2024-M1-48 E (F) : elle
- 2023-M4-51 B (V) / 2024-M4-35 B (F) : constitution elaboration
- 2024-M4-35 B (F) / LAS25-51 B (V) : elaboration constitution
- HB-2021-38 A (V) / HB-2022-28 A (F) : oxygene carbone
- HB-2023-38 A (F) / HB-2024-28 A (V) : azote oxygene 2p2 2p4
- 2020-M2-2 E (V) / 2024-M2-2 D (F) : h2 he2 h 1
- 2021-M2-2 A (V) / 2024-M2-2 D (F) : f2 he2 f 9
- 2020-M2-3 C (V) / 2021-M2-4 C (F) : volume pression constant constante
- 2021-M1-53 A (V) / 2023-M1-20 A (F) : systole diastole
- 2020-M2-6 A (V) / HB-2022-29 C (F) : chirale achirale
- 2020-M2-6 A (V) / HB-2023-39 C (F) : chirale achirale
- 2020-M2-6 A (V) / HB-2024-29 C (F) : chirale achirale
- HB-2021-40 B (F) / HB-2022-29 B (V) : r 
- HB-2021-40 B (F) / HB-2022-30 B (V) : r 
- HB-2021-40 B (F) / HB-2023-39 B (V) : r 
- HB-2021-40 B (F) / HB-2024-29 D (V) : r 
- HB-2022-29 B (V) / HB-2023-39 D (F) :  r
- HB-2022-29 B (V) / HB-2024-29 B (F) :  r
- HB-2022-29 D (F) / HB-2022-30 B (V) : r 
- HB-2022-29 D (F) / HB-2023-39 B (V) : r 
- HB-2022-29 D (F) / HB-2024-29 D (V) : r 
- HB-2022-30 B (V) / HB-2023-39 D (F) :  r
- HB-2022-30 B (V) / HB-2024-29 B (F) :  r
- HB-2023-39 B (V) / HB-2024-29 B (F) :  r
- HB-2023-39 D (F) / HB-2024-29 D (V) : r 
- 2021-M2-6 C (F) / 2023-M2-14 D (V) : cf3 cl
- 2022-M2-6 C (F) / 2023-M2-14 D (V) : nh2 cl
- 2024-M2-6 C (F) / 2023-M2-14 D (V) : nh2 cl
- 2023-M2-6 C (F) / 2023-M2-14 D (V) : ch3 cl
- 2020-M2-9 D (F) / 2024-M2-17 C (V) : f g
- 2022-M2-9 B (F) / 2023-M2-12 C (V) : f h
- 2024-M2-12 C (F) / 2023-M2-12 C (V) : electrophile nucleophile
- 2023-M2-12 C (V) / HB-2023-40 C (F) : addition substitution
- 2023-M2-12 C (V) / HB-2024-30 C (F) : addition substitution
- HB-2021-41 A (V) / HB-2022-31 D (F) : h2so4 kmno4
- HB-2021-41 A (V) / HB-2023-41 D (F) : h2so4 kmno4
- HB-2021-41 A (V) / HB-2024-31 C (F) : h2so4 kmno4
- HB-2021-41 D (F) / HB-2022-31 A (V) : kmno4 h2so4
- HB-2021-41 D (F) / HB-2023-41 C (V) : kmno4 h2so4
- HB-2021-41 D (F) / HB-2024-31 E (V) : kmno4 h2so4
- HB-2022-31 A (V) / HB-2023-41 D (F) : h2so4 kmno4
- HB-2022-31 A (V) / HB-2024-31 C (F) : h2so4 kmno4
- HB-2022-31 D (F) / HB-2023-41 C (V) : kmno4 h2so4
- HB-2022-31 D (F) / HB-2024-31 E (V) : kmno4 h2so4
- HB-2023-41 C (V) / HB-2024-31 C (F) : h2so4 kmno4
- HB-2023-41 D (F) / HB-2024-31 E (V) : kmno4 h2so4
- 2022-M2-10 B (V) / 2023-M2-14 B (F) : par avec g h
- 2021-M2-17 A (V) / 2022-M2-17 B (F) : ester acide
- 2021-M2-17 A (V) / 2023-M2-20 B (F) : ester acide
- 2021-M2-11 E (V) / 2022-M2-11 E (F) : h2so4
- 2020-M2-15 E (V) / 2021-M2-15 E (F) : cetolisation aldolisation
- 2021-M2-15 E (F) / 2022-M2-15 A (V) : aldolisation cetolisation
- 2021-M2-12 C (V) / 2022-M2-12 C (F) : h i
- 2020-M2-17 E (V) / 2022-M2-19 E (F) : i h
- 2020-M2-17 E (V) / 2024-M2-22 E (F) : i h
- 2020-M2-19 E (V) / 2021-M2-17 E (F) : h i
- 2020-M2-19 E (V) / 2024-M2-20 E (F) : h i
- 2021-M2-17 E (F) / 2021-M2-19 E (V) : i h
- 2021-M2-17 E (F) / 2023-M2-22 E (V) : i h
- 2021-M2-19 E (V) / 2024-M2-20 E (F) : h i
- 2022-M2-17 E (V) / 2022-M2-19 E (F) : i h
- 2022-M2-17 E (V) / 2024-M2-22 E (F) : i h
- 2022-M2-19 E (F) / 2023-M2-20 E (V) : h i
- 2024-M2-20 E (F) / 2023-M2-22 E (V) : i h
- 2024-M2-22 E (F) / 2023-M2-20 E (V) : h i
- 2020-M2-33 C (V) / HB-2022-34 E (F) : 11 2
- 2020-M2-33 C (V) / HB-2024-34 E (F) : 11 2
- 2022-M1-43 D (V) / LAS25-33 C (F) : longue courte
- 2022-M2-35 D (V) / HB-2021-30 B (F) : 2 3
- 2022-M2-35 D (V) / HB-2022-35 B (F) : 2 troi
- 2022-M2-35 D (V) / HB-2024-35 C (F) : 2 3
- 2021-M1-46 C (F) / HB-2021-42 C (V) : tissu cellule
- 2020-M4-25 D (F) / 2021-M4-32 D (V) : maladie
- 2020-M4-41 E (F) / 2021-M4-51 D (V) : 2 1
- 2020-M4-41 E (F) / 2022-M4-48 D (V) : 2 1
- 2021-M1-18 C (F) / 2022-M1-44 C (V) : calcium sodium
- HB-2021-52 E (V) / HB-2023-54 D (F) : induisent induit
- 2022-M4-21 C (F) / LASSP-2024-49 C (V) : r0 rr
- 2022-M4-21 C (F) / HB-2024-8 C (V) : r0 rr
- 2021-M1-30 D (F) / 2023-M1-3 C (V) : distal proximal
- 2021-M1-30 D (F) / 2024-M1-3 C (V) : distal proximal
- 2021-M1-44 D (V) / 2022-M1-21 B (F) : gnosie praxie
- 2021-M1-45 E (F) / 2024-M1-10 C (V) : positive negative
- 2021-M1-49 E (F) / 2023-M1-23 B (V) : orthosympathique parasympathique
- 2021-M2-26 E (F) / 2021-M2-27 E (V) : 3
- 2021-M2-27 E (V) / 2021-M2-28 C (F) : 3 deux
- 2021-M2-31 A (F) / 2022-M2-31 A (V) : 8 6
- 2021-M2-31 A (F) / 2024-M2-30 D (V) : 8 6
- 2024-M2-38 A (V) / 2023-M2-41 E (F) : a1 a2 phospholipide glycerophospholipide
- 2021-M4-49 B (F) / 2022-M4-49 B (V) : fixe amovible
- 2024-M4-31 A (V) / LAS25-49 A (F) : conjointe adjointe
- 2024-M4-31 B (V) / LAS25-49 A (F) : amovible fixe
- 2022-M2-56 C (V) / 2024-M2-52 C (F) : diminution augmentation pco2 pco
- 2022-M2-56 E (V) / HB-2022-40 E (F) : hyperventilation hypoventilation
- 2024-M2-52 C (F) / HB-2024-39 C (V) : augmentation diminution pco pco2
- HB-2024-39 E (V) / HB-2022-40 E (F) : hyperventilation hypoventilation
- 2023-M1-50 B (V) / HB-2022-43 C (F) : faible elevee
- 2022-M2-28 E (F) / HB-2023-27 A (V) : c
- HB-2021-47 C (F) / HB-2023-42 D (V) : reabsorption secretion correspond
- HB-2021-47 C (F) / HB-2024-42 C (V) : reabsorption secretion correspond
- 2024-M1-26 A (V) / LAS25-7 B (F) : externe interne
- 2023-M1-42 A (F) / HB-2023-49 C (V) : officinale magistrale
- 2023-M1-52 A (F) / 2024-M1-46 C (V) : cationique anionique
- 2024-M2-54 B (F) / 2023-M2-54 A (V) : hypo hyper
- 2024-M2-52 A (F) / HB-2024-39 A (V) : tim mr 
- 2024-M2-52 B (V) / HB-2024-39 B (F) : tim mr 
- 2024-M4-31 D (F) / LAS25-49 D (V) : dur soutien
- HB-2021-14 A (V) / HB-2024-13 A (F) : il
- HB-2021-23 D (F) / HB-2024-23 D (V) : presentent presente
- HB-2022-23 D (F) / HB-2024-23 D (V) : presentent presente lh fsh
- HB-2023-23 D (F) / HB-2024-23 D (V) : elle presentent presente
- HB-2021-37 C (F) / HB-2022-27 C (V) : orbital orbitale p 
- HB-2022-36 E (V) / HB-2024-36 E (F) : 23 21

</details>

<details><summary>même texte, énoncé différent : 56</summary>

- HB-2021-45 D (V) / HB-2024-47 E (F) : « le calibre des voies aériennes intrapulmonaires au… »
- HB-2024-47 E (F) / LAS25-7 E (V) : « le calibre des voies aériennes intrapulmonaires au… »
- 2023-M1-10 A (V) / HB-2024-47 A (F) : « la pression alvéolaire est inférieure à la pressio… »
- HB-2021-45 B (V) / HB-2024-47 A (F) : « la pression alvéolaire est inférieure à la pressio… »
- 2020-M1-41 A (V) / 2021-M1-15 A (F) : « est une voie d'administration transmuqueuse »
- 2020-M1-49 D (V) / 2021-M1-23 D (F) : « est habituellement détecté avant l'autorisation de… »
- 2020-M1-49 C (V) / 2021-M1-23 C (F) : « est dépendant de la dose »
- 2022-M4-24 E (V) / 2022-M4-25 B (F) : « L’estimation de la relation de cause à effet. »
- 2022-M4-24 E (V) / LAS25-55 B (F) : « L’estimation de la relation de cause à effet. »
- 2021-M2-33 E (V) / 2024-M2-40 C (F) : « Le nombre d'électrons transférés est de 2. »
- LASSP-2022-49 C (F) / HB-2023-9 C (V) : « La mortalité évitable correspond à la mortalité av… »
- HB-2022-8 C (F) / HB-2023-9 C (V) : « La mortalité évitable correspond à la mortalité av… »
- 2020-M2-6 B (V) / HB-2021-40 B (F) : « La molécule F est de configuration R »
- 2020-M2-6 B (V) / HB-2022-29 D (F) : « La molécule F est de configuration R »
- 2020-M2-6 B (V) / HB-2023-39 D (F) : « La molécule F est de configuration R »
- 2020-M2-6 B (V) / HB-2024-29 B (F) : « La molécule F est de configuration R »
- 2020-M2-16 C (F) / 2021-M2-16 C (V) : « G est un mélange d’oléfines de stéréochimie Z et E »
- 2020-M2-16 C (F) / 2022-M2-16 D (V) : « G est un mélange d’oléfines de stéréochimie Z et E »
- 2020-M2-19 E (V) / 2022-M2-19 E (F) : « Le composé H a pour structure : »
- 2020-M2-19 E (V) / 2024-M2-22 E (F) : « Le composé H a pour structure : »
- 2020-M2-15 D (F) / 2021-M2-15 D (V) : « H possède une fonction cétone »
- 2020-M2-19 B (F) / 2022-M2-19 B (V) : « Le composé G intermédiaire a pour structure : »
- 2020-M2-19 B (F) / 2023-M2-22 B (V) : « Le composé G intermédiaire a pour structure : »
- 2020-M2-17 E (V) / 2021-M2-17 E (F) : « Le composé I a pour structure : »
- 2020-M2-17 E (V) / 2024-M2-20 E (F) : « Le composé I a pour structure : »
- 2020-M4-50 A (V) / 2023-M4-24 D (F) : « la mortalité prématurée fait partie des déterminan… »
- 2022-M2-22 C (V) / 2024-M2-27 C (F) : « est un acide aminé essentiel »
- 2022-M2-22 C (V) / HB-2024-34 D (F) : « est un acide aminé essentiel »
- 2022-M1-43 E (F) / HB-2022-43 A (V) : « est d'autant plus élevée que la dose est élevée »
- 2020-M2-46 A (F) / 2020-M2-47 A (V) : « Est une base purique »
- 2020-M4-5 A (V) / 2022-M4-8 A (F) : « As you grow old, you may find that your joints are… »
- 2022-M4-27 A (V) / 2023-M4-33 D (F) : « Droit de représentation des usagers du système de … »
- 2020-M4-32 D (V) / 2021-M4-42 D (F) : « l'éducation thérapeutique des patients ; »
- 2021-M4-42 D (F) / 2022-M4-41 D (V) : « l'éducation thérapeutique des patients »
- 2020-M4-42 B (F) / 2023-M4-55 E (V) : « de rechercher, de traiter et d'analyser des donnée… »
- 2021-M4-23 D (V) / 2021-M4-24 C (F) : « Actions visant à réduire l'incidence puis la préva… »
- 2020-M4-55 A (F) / HB-2023-10 C (V) : « le droit de la personne au respect de sa vie privé… »
- 2020-M4-55 E (F) / HB-2023-10 B (V) : « le droit de la personne au respect de sa dignité. »
- 2022-M4-27 B (F) / 2023-M4-33 A (V) : « Droit au respect de sa dignité. »
- 2022-M4-27 E (F) / 2023-M4-33 C (V) : « Droit de refuser un traitement ou un acte médical. »
- HB-2021-52 E (V) / HB-2024-52 E (F) : « induisent un effet maximal de moindre intensité qu… »
- 2022-M4-21 D (F) / LASSP-2024-49 C (V) : « Si le RR< 1 alors le facteur étudié est un facteur… »
- 2022-M4-21 D (F) / HB-2024-8 C (V) : « Si le RR< 1 alors le facteur étudié est un facteur… »
- 2022-M2-25 C (V) / 2022-M2-27 B (F) : « est un ose réducteur »
- 2021-M4-23 B (F) / 2021-M4-24 A (V) : « Actions visant à éviter la surmédicalisation d'un … »
- 2022-M1-51 A (V) / HB-2022-46 C (F) : « Les solutions buvables »
- 2022-M2-22 D (F) / 2024-M2-27 B (V) : « porte une fonction alcool primaire »
- HB-2022-34 B (F) / HB-2024-34 B (V) : « porte une fonction alcool »
- 2022-M2-28 E (F) / 2023-M2-25 A (V) : « C'est un isomère du glucose. »
- HB-2023-27 A (V) / HB-2023-28 B (F) : « Est un isomère du glucose »
- 2022-M4-27 D (V) / 2023-M4-33 B (F) : « Droit à l’action de groupe en santé. »
- 2022-M4-40 A (V) / 2024-M4-36 E (F) : « la dispensation des médicaments. »
- 2023-M1-46 D (V) / 2024-M1-51 D (F) : « donne son avis sur la place du médicament dans la … »
- 2024-M2-26 D (F) / HB-2023-28 D (V) : « contient du galactose »
- 2023-M2-26 C (V) / HB-2023-28 A (F) : « Contient du fructose »
- HB-2021-23 B (V) / HB-2022-23 B (F) : « elles sont habituellement organisées en amas (îlot… »

</details>

<details><summary>même texte, énoncé général mais molécule / figure propre à chaque sujet : 18</summary>

- 2024-M2-14 B (V) / 2023-M2-14 B (F) : « Le traitement de F avec Na/NH3 liquide/tBuOH condu… »
- 2024-M2-13 A (V) / 2023-M2-13 A (F) : « Le traitement de F par 1) H2SO4 dilué ; 2) H2SO4 c… »
- 2021-M2-19 E (V) / 2022-M2-19 E (F) : « Le composé H a pour structure : »
- 2021-M2-19 E (V) / 2024-M2-22 E (F) : « Le composé H a pour structure : »
- 2022-M2-19 E (F) / 2023-M2-22 E (V) : « Le composé H a pour structure : »
- 2024-M2-22 E (F) / 2023-M2-22 E (V) : « Le composé H a pour structure : »
- 2020-M2-18 E (V) / 2021-M2-18 E (F) : « 1) Zn/Hg/HCl ; 2) O3, puis hydrolyse en milieu réd… »
- 2020-M2-18 B (F) / 2021-M2-18 D (V) : « 1) H2 (1 mole) Pd/C ; 2) Zn/Hg/HCl ; 3) O3, puis h… »
- 2021-M2-15 D (V) / 2022-M2-15 E (F) : « H possède une fonction cétone »
- 2021-M2-19 B (F) / 2022-M2-19 B (V) : « Le composé G intermédiaire a pour structure : »
- 2021-M2-19 B (F) / 2023-M2-22 B (V) : « Le composé G intermédiaire a pour structure : »
- 2022-M2-19 B (V) / 2024-M2-22 B (F) : « Le composé G intermédiaire a pour structure : »
- 2024-M2-22 B (F) / 2023-M2-22 B (V) : « Le composé G intermédiaire a pour structure : »
- 2021-M2-17 E (F) / 2022-M2-17 E (V) : « Le composé I a pour structure : »
- 2021-M2-17 E (F) / 2023-M2-20 E (V) : « Le composé I a pour structure : »
- 2022-M2-17 E (V) / 2024-M2-20 E (F) : « Le composé I a pour structure : »
- 2024-M2-20 E (F) / 2023-M2-20 E (V) : « Le composé I a pour structure : »
- 2024-M2-17 E (V) / 2023-M2-17 E (F) : « La molécule H est achirale. »

</details>

## e) Lettres non continues ou lettre de `ans` absente

Aucun cas.

## f) Questions réalignées pendant la relecture, et explications décalées

Questions réalignées : anciens textes lus au commit `064fe99` (avant la relecture), comparés au texte actuel, aux `v` et aux explications, puis vérifiés sur le scan. Aucun corrigé d'origine n'est dans le dépôt : pour la chimie PACES (clé par lettre, sans explication), la clé a été vérifiée par la chimie de la réaction sur le scan. Pour toutes les questions : explication dont les mots correspondent à une autre proposition de la même question (≥ 75 %) et presque pas à la sienne (≤ 20 %).

| Question | Problème | Extrait | Classement | Relecture |
|---|---|---|---|---|
| HB-2021-35 | ans ADE = propositions vraies ; 5 explication(s) ; explications en face de leur proposition ; texte modifié en ABCDE depuis 064fe99 ; ATTENTION : v ou ex ont changé |  | pas une anomalie | Explications A à E en face des propositions réalignées ; clé ADE cohérente. |
| HB-2023-26 | ans AC = propositions vraies ; 5 explication(s) ; explications en face de leur proposition ; texte modifié en BCDE depuis 064fe99 ; ATTENTION : v ou ex ont changé |  | pas une anomalie | Explications B à E en face des propositions réalignées (D : 1/2 et non 1/4 ; E : 1/2 et non 1) ; clé AC cohérente. |
| 2023-M2-10 | ans BCD = propositions vraies ; 5 explication(s) ; explications en face de leur proposition ; texte modifié en ABCDE depuis 064fe99 ; ATTENTION : v ou ex ont changé |  | pas une anomalie | Explications B à E en face des propositions réalignées ; clé BCD cohérente. |
| 2021-M2-50 | ans A = propositions vraies ; 5 explication(s) ; explications en face de leur proposition ; texte modifié en ABCDE depuis 064fe99 ; ATTENTION : v ou ex ont changé |  | pas une anomalie | Scan : Q50 = valeur de 1 mm Hg ; clé A = 136 Pa, confirmée par le calcul de l'explication (10⁻³ × 13,6·10³ × 10). A_RELIRE.md disait à tort « B : 1,36 kPa » (corrigé). |
| 2021-M2-51 | ans B = propositions vraies ; 5 explication(s) ; explications en face de leur proposition ; texte modifié en ABCDE depuis 064fe99 ; ATTENTION : v ou ex ont changé |  | pas une anomalie | Scan : Q51 = 100 mm Hg en mm H2O ; clé B = 1360 mm H2O, confirmée par l'explication. |
| 2024-M4-27 C | relevé à la relecture (sous le seuil du contrôle automatique) | C : La réanimation pédiatrique — ex : La sage-femme réalise la réanimation du nouveau-né, pas la r… | à vérifier dans le cours | Pas une contradiction de saisie : la note rappelle que la seconde correction compte B vrai et que la réponse de la première correction (B faux) est gardée, à confirmer. Statut passé en « À vérifier ». |
| HB-2024-19 A | relevé à la relecture (sous le seuil du contrôle automatique) | A : la glande mammaire est une glande apocrine ; — ex : La glande mammaire élimine son produit avec la couronne de c… | à vérifier dans le cours | L'explication de A (glande mammaire apocrine) parle des glandes sébacées (sujet de D). Réponse non touchée ; explication à reprendre. Statut « À vérifier ». |
| HB-2023-12 C | relevé à la relecture (sous le seuil du contrôle automatique) | C : la microscopie à contraste de phase nécessite l’ut… — ex : Le contraste de phase permet d'observer des cellules vivante… | à vérifier dans le cours | L'explication de C (contraste de phase) parle de la microscopie confocale (sujet de D). Réponse non touchée ; explication à reprendre. Statut « À vérifier ». |

