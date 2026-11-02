#!/usr/bin/env python3
"""Contrôle de cohérence interne des corrections (relançable).

Usage : python3 tools/coherence.py            -> écrit docs/COHERENCE.md et affiche le bilan
        python3 tools/coherence.py --stdout   -> affiche le rapport sans l'écrire

Ne modifie jamais les données. Contrôles, pour chaque question :
  a) ans == lettres des propositions où v est vrai
  b) QRU/QCS : exactement une vraie ; QCM/QRM : au moins une (questions annulées à part)
  c) explication qui contredit v : verdict explicite (« Vrai », « Faux »… au début ou à la fin),
     verdict par lettre (« D vrai, E faux ») comparé aux v de la question,
     type cité dans l'explication ou la note (« C'est une QRU ») différent du champ type
  d) même proposition (similarité > 90 %) dans plusieurs questions avec des v différents
  e) lettres continues (A, B, C…), aucune lettre de ans absente des propositions
  f) questions réalignées pendant la relecture : réponse et explications en face de la bonne
     proposition ; plus, sur toutes les questions, explication qui décrit une autre proposition.
Les conclusions de la relecture humaine sont dans MANUEL (plus bas) : elles sont reprises dans le rapport.
"""
import collections, difflib, json, os, re, subprocess, sys, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILES = ['data_S1.json', 'data_m2_23.json', 'data_new.json', 'data_las25.json']
BASE_RELECTURE = '064fe99'   # commit d'avant la relecture texte (anciens textes des questions réalignées)
PRIORITE = ['PACES-2017-14', 'PACES-2017-20', 'PACES-2017-21', 'PACES-2017-26', 'PACES-2018-14', 'PACES-2018-20',
            'PACES-2018-25', 'PACES-2019-25', 'HB-2021-35', 'HB-2023-26', '2023-M2-10', '2021-M2-50', '2021-M2-51']
CERTAINE, A_VERIFIER, NORMAL = 'erreur de saisie certaine', 'à vérifier dans le cours', 'pas une anomalie'

# Relecture humaine (novembre 2026). Clé : (id, lettre ou '') ; valeur : (classement, commentaire).
MANUEL = {
    # c)
    ('2024-M1-44', ''): (CERTAINE, "Le sujet indique « 44) QRU » (scan 2024-12) et la rectification s'appuie sur « C'est une QRU », "
                                   "mais le champ type disait QRM. Type corrigé en QRU, réponse D inchangée.",
                         'c', "explication / note : « C'est une QRU », type = QRM (corrigé en QRU)"),
    ('2024-M4-27', 'C'): (A_VERIFIER, "Pas une contradiction de saisie : la note rappelle que la seconde correction compte B vrai et que "
                                      "la réponse de la première correction (B faux) est gardée, à confirmer. Statut passé en « À vérifier »."),
    # f) questions réalignées : contrôle sur le scan et, pour la chimie, sur la réaction
    ('PACES-2017-14', ''): (NORMAL, "Clé B (corrigé par lettre, sans explication) : en face de « Br2/FeBr3 ; Mg ; CO2 ; H3O+ ; Zn/Hg/HCl », "
                                    "qui donne bien l'acide 3-éthylbenzoïque G à partir de l'acétophénone F."),
    ('PACES-2017-20', ''): (NORMAL, "Clé BDE : B (nitronium) vrai, A (acylium « R+ ») faux, D et E vrais : cohérent avec le texte réaligné."),
    ('PACES-2017-21', ''): (NORMAL, "Clé D : alkylation en méta, oxydation KMnO4, réduction, déshydratation → acide 3-vinylbenzoïque G. Cohérent."),
    ('PACES-2017-26', ''): (NORMAL, "Clé D : hydrogénation du vinyle, Clemmensen, ozonolyse, aldolisation → cycloheptènone G. Cohérent."),
    ('PACES-2018-14', ''): (NORMAL, "Chaque explication (A, B, C) décrit la proposition réalignée ; clé D cohérente."),
    ('PACES-2018-20', ''): (NORMAL, "Explications B (nitronium électrophile), C, D, E en face des bonnes propositions."),
    ('PACES-2018-25', ''): (NORMAL, "B = NaBH4 (explication : réduit seulement la cétone, vrai), C = LiAlH4 en excès (faux) : cohérent."),
    ('PACES-2019-25', ''): (NORMAL, "B = Zn/Hg/HCl (vrai), C = LiAlH4 en excès (faux) : explications en face des bonnes propositions."),
    ('HB-2021-35', ''): (NORMAL, "Explications A à E en face des propositions réalignées ; clé ADE cohérente."),
    ('HB-2023-26', ''): (NORMAL, "Explications B à E en face des propositions réalignées (D : 1/2 et non 1/4 ; E : 1/2 et non 1) ; clé AC cohérente."),
    ('2023-M2-10', ''): (NORMAL, "Explications B à E en face des propositions réalignées ; clé BCD cohérente."),
    ('2021-M2-50', ''): (NORMAL, "Scan : Q50 = valeur de 1 mm Hg ; clé A = 136 Pa, confirmée par le calcul de l'explication "
                                 "(10⁻³ × 13,6·10³ × 10). A_RELIRE.md disait à tort « B : 1,36 kPa » (corrigé)."),
    ('2021-M2-51', ''): (NORMAL, "Scan : Q51 = 100 mm Hg en mm H2O ; clé B = 1360 mm H2O, confirmée par l'explication."),
    # f) explication qui semble décrire une autre proposition (contrôle sur toutes les questions)
    ('HB-2024-19', 'A'): (A_VERIFIER, "L'explication de A (glande mammaire apocrine) parle des glandes sébacées (sujet de D). "
                                      "Réponse non touchée ; explication à reprendre. Statut « À vérifier »."),
    ('HB-2023-12', 'C'): (A_VERIFIER, "L'explication de C (contraste de phase) parle de la microscopie confocale (sujet de D). "
                                      "Réponse non touchée ; explication à reprendre. Statut « À vérifier »."),
    ('2022-M4-23', 'D'): (NORMAL, "L'explication oppose surveillance et veille sanitaire : elle répond bien à D."),
    ('2023-M2-14', 'B'): (NORMAL, "Explication sur la réduction de Birch : c'est bien le sujet de B."),
    ('2023-M2-14', 'C'): (NORMAL, "Explication sur l'halogénation : c'est bien le sujet de C."),
    ('HB-2022-30', 'D'): (NORMAL, "« G est chirale » répond bien à « G est achirale » (D faux)."),
    ('2020-M4-51', 'A'): (NORMAL, "Explication = définition de la littératie : répond à A (faux)."),
    ('2021-M1-15', 'B'): (NORMAL, "Explication sur la voie intraveineuse : répond à B."),
    ('HB-2021-25', 'C'): (NORMAL, "Explication sur la translocation (échange, pas chromosome surnuméraire) : répond à C."),
    ('HB-2022-20', 'D'): (NORMAL, "Définition de la métaplasie : répond à D."),
    ('2024-M1-44', 'E'): (NORMAL, "Explication de la rectification (question à une seule réponse) : concerne E."),
}

def load(rev=None):
    qs = []
    for f in FILES:
        if rev:
            r = subprocess.run(['git', '-C', ROOT, 'show', f'{rev}:data/{f}'], capture_output=True, text=True)
            if r.returncode:
                return None
            qs += json.loads(r.stdout)
        else:
            qs += json.load(open(os.path.join(ROOT, 'data', f), encoding='utf-8'))
    return qs

def clean(s):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', s or '')).strip()

def norm(s):
    s = unicodedata.normalize('NFKC', clean(s)).lower().replace('’', "'")
    return s.strip(' .;')

def ascii_words(s):
    s = unicodedata.normalize('NFKD', norm(s))
    return re.findall(r'[a-z0-9]+', ''.join(c for c in s if not unicodedata.combining(c)))

STOP = set("le la les l un une des de du d a à au aux en et est sont".split())
STOP2 = STOP | set("ne pas que qui se sa son ses il elle on par pour dans sur avec ce cette ces plus moins ou donc car mais si y etre ete the of to and is are in an".split())

def toks(s):
    return [w.rstrip('s') for w in ascii_words(s) if w not in STOP]

def wordset(s):
    return {w.rstrip('s') for w in ascii_words(s) if len(w) >= 3 and w not in STOP2}

def meme_enonce(sa, sb, rs):
    """Même énoncé : très proche (> 90 %) et les mots qui changent ne sont que des accords (peut / peuvent)."""
    if rs < 0.9:
        return False
    wa, wb = toks(sa), toks(sb)
    diff = [w[2:] for w in difflib.ndiff(wa, wb) if w[:1] in '+-']
    moins = [w for w in diff if w not in wb]; plus = [w for w in diff if w not in wa]
    return len(moins) == len(plus) and all(a[:3] == b[:3] for a, b in zip(moins, plus))

MENTION = re.compile(r' ?- ?Propriété exclusive du [^-]*?(?: -$|$)')

def short(s, n=90):
    s = clean(s)
    return (s[:n] + '…') if len(s) > n else s

def md(s):
    return str(s).replace('|', '\\|').replace('\n', ' ')

SINGLE = ('QRU', 'QCS')

def run():
    qs = load()
    Q = {q['id']: q for q in qs}
    R = collections.OrderedDict((k, []) for k in 'abcdef')

    def add(k, qid, probleme, extrait, classement, lettre=''):
        m = MANUEL.get((qid, lettre)) or MANUEL.get((qid, ''))
        com = ''
        if m and ((qid, lettre) in MANUEL or k in 'cf'):
            classement, com = m[0], m[1]
        R[k].append({'id': qid, 'l': lettre, 'probleme': probleme, 'extrait': extrait, 'classement': classement,
                     'commentaire': com, 'status': Q[qid]['status'] if qid in Q else ''})

    for q in qs:
        L = [it['l'] for it in q['items']]
        vrais = ''.join(it['l'] for it in q['items'] if it['v'])
        # a)
        if vrais != q['ans']:
            add('a', q['id'], f"ans = {q['ans'] or '∅'} mais propositions vraies = {vrais or '∅'}", '',
                CERTAINE if not q.get('annul') else NORMAL)
        # b)
        n = len(vrais)
        if (q['type'] in SINGLE and n != 1) or (q['type'] not in SINGLE and n < 1):
            add('b', q['id'], f"{q['type']} avec {n} proposition(s) vraie(s)" + (' (question annulée)' if q.get('annul') else ''),
                '', NORMAL if q.get('annul') else A_VERIFIER)
        # e)
        attendu = [chr(65 + i) for i in range(len(L))]
        if L != attendu:
            add('e', q['id'], f"lettres {''.join(L)} (attendu {''.join(attendu)})", '', CERTAINE)
        manq = sorted(set(q['ans']) - set(L))
        if manq:
            add('e', q['id'], f"lettre(s) de ans absente(s) des propositions : {''.join(manq)}", '', CERTAINE)

    # c) explication qui contredit v
    debut_v = re.compile(r'^\W*(vrai|exact|juste|correct)e?s?\b', re.I)
    debut_f = re.compile(r'^\W*(faux|fausse|inexact|incorrect|erron)', re.I)
    fin_v = re.compile(r"\b(donc|c'est|est)\s+(vrai|exact|juste)e?\W*$", re.I)
    fin_f = re.compile(r"\b(donc|c'est|est)\s+(faux|fausse|inexacte?)\W*$", re.I)
    lettre = re.compile(r'(?<![A-Za-zÀ-ÿ’\'])(?:item\s+|proposition\s+)?([A-E])\s*(?:\)\s*)?(?:est\s+(?:donc\s+)?)?(?:=|:|→)?\s*'
                        r'(vraie?s?|exacte?s?|justes?|fausses?|faux|inexactes?|erronée?s?)\b', re.I)
    type_cite = re.compile(r"c'est une (QRU|QCS|QCM|QRM)\b", re.I)
    for q in qs:
        V = {it['l']: it['v'] for it in q['items']}
        for it in q['items']:
            ex = clean(it['ex'])
            if (debut_v.search(ex) or fin_v.search(ex)) and not it['v']:
                add('c', q['id'], f"{it['l']} : l'explication dit vrai, v = faux", short(ex), A_VERIFIER, it['l'])
            if (debut_f.search(ex) or fin_f.search(ex)) and it['v'] and not ex.startswith('Rectifié'):
                add('c', q['id'], f"{it['l']} : l'explication dit faux, v = vrai", short(ex), A_VERIFIER, it['l'])
            for m in lettre.finditer(ex):
                X, w = m.group(1).upper(), m.group(2).lower()
                val = not w.startswith(('faux', 'fauss', 'inex', 'erron'))
                if X in V and V[X] != val:
                    i = m.start()
                    add('c', q['id'], f"l'explication de {it['l']} dit « {X} {w} », v de {X} = {'vrai' if V[X] else 'faux'}",
                        '…' + short(ex[max(0, i - 70):i + 30], 110), A_VERIFIER, it['l'])
        txt = ' '.join(clean(it['ex']) for it in q['items']) + ' ' + clean(q.get('note'))
        for t in sorted({m.upper() for m in type_cite.findall(txt)}):
            meme = (t in SINGLE) == (q['type'] in SINGLE)
            if not meme:
                add('c', q['id'], f"explication / note : « C'est une {t} », type = {q['type']}", short(q.get('note') or txt), A_VERIFIER)

    # d) propositions semblables dans plusieurs questions
    CTX = re.compile(r"(\b[A-Z]\b(?![’'])|structure|compos[ée]|mol[ée]cule|ci-dess|figure|sch[ée]ma|courbe|graph|tableau|réaction)")
    GEN = re.compile(r'^parmi les propositions suivantes')
    items = []
    for q in qs:
        if q.get('annul'):
            continue
        for it in q['items']:
            n = norm(it['t'])
            if len(n) >= 20:
                items.append((q['id'], it['l'], it['v'], n, it['t']))
    idx = collections.defaultdict(set)
    for i, x in enumerate(items):
        w = x[3].split()
        for k in range(max(1, len(w) - 2)):
            idx[' '.join(w[k:k + 3])].add(i)
    vus = set(); d_normal = collections.Counter(); d_exemples = collections.defaultdict(list)
    for s in idx.values():
        if len(s) > 60:
            continue
        s = sorted(s)
        for a in range(len(s)):
            for b in range(a + 1, len(s)):
                A, B = items[s[a]], items[s[b]]
                if (s[a], s[b]) in vus or A[0] == B[0] or A[2] == B[2]:
                    continue
                vus.add((s[a], s[b]))
                la, lb = len(A[3]), len(B[3])
                if min(la, lb) / max(la, lb) < 0.9:
                    continue
                r = difflib.SequenceMatcher(None, A[3], B[3]).ratio()
                if r <= 0.9:
                    continue
                sa, sb = norm(Q[A[0]]['stem']), norm(Q[B[0]]['stem'])
                rs = difflib.SequenceMatcher(None, sa, sb).ratio()
                ta, tb = toks(A[4]), toks(B[4])
                paire = f"{A[0]} {A[1]} ({'V' if A[2] else 'F'}) / {B[0]} {B[1]} ({'V' if B[2] else 'F'})"
                if ta != tb:
                    diff = [w for w in difflib.ndiff(ta, tb) if w[:1] in '+-']
                    d_normal['un mot change (sens différent)'] += 1
                    d_exemples['un mot change (sens différent)'].append(f"{paire} : {' '.join(w[2:] for w in diff[:4])}")
                elif not meme_enonce(sa, sb, rs):
                    d_normal['même texte, énoncé différent'] += 1
                    d_exemples['même texte, énoncé différent'].append(f"{paire} : « {short(A[4], 50)} »")
                elif GEN.match(sa) or CTX.search(clean(A[4])):
                    d_normal['même texte, énoncé général mais molécule / figure propre à chaque sujet'] += 1
                    d_exemples['même texte, énoncé général mais molécule / figure propre à chaque sujet'].append(f"{paire} : « {short(A[4], 50)} »")
                else:
                    R['d'].append({'id': f"{A[0]} {A[1]} / {B[0]} {B[1]}", 'l': '',
                                   'probleme': f"même proposition, même énoncé (« {short(Q[A[0]]['stem'], 45)} ») : "
                                               f"{A[0]} {A[1]} = {'vrai' if A[2] else 'faux'}, {B[0]} {B[1]} = {'vrai' if B[2] else 'faux'}",
                                   'extrait': short(A[4], 80), 'classement': A_VERIFIER,
                                   'commentaire': 'Les deux questions passent en « À vérifier » : seul le cours peut dire laquelle est juste.',
                                   'status': f"{Q[A[0]]['status']} / {Q[B[0]]['status']}", 'ids': [A[0], B[0]]})

    # f) questions réalignées + explication qui décrit une autre proposition
    old = load(BASE_RELECTURE)
    O = {q['id']: q for q in old} if old else {}

    def alignement(q):
        T = [wordset(it['t']) for it in q['items']]
        out = []
        for i, it in enumerate(q['items']):
            ex = clean(it['ex'])
            if len(ex) < 25 or re.match(r'cf\.?\s', ex, re.I):
                continue
            E = wordset(ex)
            sc = [len(E & t) / max(1, len(t)) for t in T]
            j = max((k for k in range(len(T)) if k != i), key=lambda k: sc[k], default=None)
            if j is not None and sc[i] <= 0.2 and sc[j] >= 0.75 and len(T[j]) >= 3:
                out.append((it['l'], q['items'][j]['l'], sc[i], sc[j]))
        return out

    for qid in [x for x in PRIORITE if x in Q]:
        q = Q[qid]
        vrais = ''.join(it['l'] for it in q['items'] if it['v'])
        bad = alignement(q)
        nex = sum(1 for it in q['items'] if clean(it['ex']))
        change = ''
        if qid in O:
            ch = [it['l'] for it, o in zip(q['items'], O[qid]['items']) if clean(it['t']) != clean(o['t'])]
            change = f"texte modifié en {''.join(ch) or '—'} depuis {BASE_RELECTURE}"
            if any(it['v'] != o['v'] or it['ex'] != MENTION.sub('', o['ex'], count=1) for it, o in zip(q['items'], O[qid]['items'])):
                change += ' ; ATTENTION : v ou ex ont changé'
        prob = (f"ans {q['ans']} {'=' if vrais == q['ans'] else '≠'} propositions vraies ; {nex} explication(s) ; "
                + ('explications en face de leur proposition' if not bad else 'explication(s) décalée(s) : ' +
                   ', '.join(f"{a}→{b}" for a, b, _, _ in bad)) + (f" ; {change}" if change else ''))
        add('f', qid, prob, '', NORMAL if (not bad and vrais == q['ans']) else A_VERIFIER)
    prio = set(PRIORITE)
    for q in qs:
        if q['id'] in prio:
            continue
        for a, b, so, sb in alignement(q):
            it = [x for x in q['items'] if x['l'] == a][0]
            add('f', q['id'], f"l'explication de {a} ressemble à la proposition {b} ({sb:.0%} des mots) plus qu'à {a} ({so:.0%})",
                f"{a} : {short(it['t'], 50)} — ex : {short(it['ex'], 60)}", A_VERIFIER, a)
    # cas relevés à la relecture humaine, non repérés par les contrôles automatiques
    deja = {(k, r['id'], r['l']) for k, rows in R.items() for r in rows} | {(k, r['id'], '') for k, rows in R.items() for r in rows}
    for (qid, l), m in MANUEL.items():
        cl = m[0]
        present = (m[2], qid, l) in deja if len(m) > 2 else any((k, qid, l) in deja for k in R)
        if cl != NORMAL and not present and qid in Q:
            it = [x for x in Q[qid]['items'] if x['l'] == l]
            ext = f"{l} : {short(it[0]['t'], 50)} — ex : {short(it[0]['ex'], 60)}" if it else short(Q[qid].get('note'))
            sec = m[2] if len(m) > 2 else 'f'
            prob = m[3] if len(m) > 3 else 'relevé à la relecture (sous le seuil du contrôle automatique)'
            add(sec, qid, prob, ext, cl, l)
    return Q, R, d_normal, d_exemples

TITRES = {'a': "a) Réponse (`ans`) différente des propositions marquées vraies (`v`)",
          'b': "b) Nombre de propositions vraies incompatible avec le type",
          'c': "c) Explication qui contredit `v` (ou le type)",
          'd': "d) Même proposition dans plusieurs questions, avec des `v` différents",
          'e': "e) Lettres non continues ou lettre de `ans` absente",
          'f': "f) Questions réalignées pendant la relecture, et explications décalées"}

def rapport(Q, R, d_normal, d_exemples):
    L = ["# Cohérence interne des corrections", "",
         "Rapport produit par `python3 tools/coherence.py` (relançable ; le script ne modifie pas les données). "
         "Classement : **erreur de saisie certaine** (les données se contredisent elles-mêmes et la bonne valeur ne fait aucun doute : corrigée, "
         "ancienne valeur gardée dans `orig` ou dans `note`, ligne dans `DONNEES.md`) ; **à vérifier dans le cours** (statut « À vérifier », rien tranché) ; "
         "**pas une anomalie** (cas signalé par le contrôle automatique puis écarté à la relecture, raison donnée).", "",
         "## Bilan", "", "| Contrôle | Cas signalés | Erreurs de saisie certaines | À vérifier dans le cours | Pas une anomalie |", "|---|---|---|---|---|"]
    for k, rows in R.items():
        c = collections.Counter(r['classement'] for r in rows)
        L.append(f"| {TITRES[k].split(')')[0]}) | {len(rows)} | {c[CERTAINE]} | {c[A_VERIFIER]} | {c[NORMAL]} |")
    L.append(f"| d) écartés d'office (sens ou contexte différent) | {sum(d_normal.values())} | 0 | 0 | {sum(d_normal.values())} |")
    L.append("")
    for k, rows in R.items():
        L += [f"## {TITRES[k]}", ""]
        if k == 'c':
            L += ["Recherche : « Vrai / Faux / Exact… » au début ou à la fin de l'explication, verdict par lettre (« D vrai, E faux ») comparé aux `v`, "
                  "type cité (« C'est une QRU ») comparé au champ `type`. Les explications donnent rarement un verdict explicite : "
                  "ce contrôle ne peut pas repérer une explication qui dit le contraire de `v` sans employer ces mots.", ""]
        if k == 'd':
            L += ["Similarité du texte > 90 % (comparaison caractère par caractère, balises et ponctuation ignorées), questions différentes. "
                  "Seuls les cas où le texte et l'énoncé sont les mêmes (et l'énoncé n'est pas un « Parmi les propositions suivantes » "
                  "qui dépend d'une figure propre au sujet) sont des contradictions possibles.", ""]
        if k == 'f':
            L += [f"Questions réalignées : anciens textes lus au commit `{BASE_RELECTURE}` (avant la relecture), comparés au texte actuel, aux `v` "
                  "et aux explications, puis vérifiés sur le scan. Aucun corrigé d'origine n'est dans le dépôt : pour la chimie PACES "
                  "(clé par lettre, sans explication), la clé a été vérifiée par la chimie de la réaction sur le scan. "
                  "Pour toutes les questions : explication dont les mots correspondent à une autre proposition de la même question (≥ 75 %) "
                  "et presque pas à la sienne (≤ 20 %).", ""]
        if not rows:
            L += ["Aucun cas.", ""]
        else:
            L += ["| Question | Problème | Extrait | Classement | Relecture |", "|---|---|---|---|---|"]
            for r in rows:
                qid = r['id'] + (f" {r['l']}" if r['l'] and k in 'cf' and r['l'] not in r['id'] else '')
                L.append(f"| {md(qid)} | {md(r['probleme'])} | {md(r['extrait'])} | {r['classement']} | {md(r['commentaire'])} |")
            L.append("")
        if k == 'd' and d_normal:
            L += ["Cas écartés d'office (pas une anomalie) :", ""]
            for cat, n in d_normal.most_common():
                L += [f"<details><summary>{cat} : {n}</summary>", "", *[f"- {md(e)}" for e in d_exemples[cat]], "", "</details>", ""]
    return '\n'.join(L) + '\n'

if __name__ == '__main__':
    Q, R, d_normal, d_exemples = run()
    txt = rapport(Q, R, d_normal, d_exemples)
    if '--stdout' in sys.argv:
        print(txt)
    else:
        open(os.path.join(ROOT, 'docs', 'COHERENCE.md'), 'w', encoding='utf-8').write(txt)
    for k, rows in R.items():
        c = collections.Counter(r['classement'] for r in rows)
        print(f"{k}) {len(rows)} cas : {c[CERTAINE]} certaines, {c[A_VERIFIER]} à vérifier, {c[NORMAL]} écartés")
    print(f"d) écartés d'office : {sum(d_normal.values())} paires ({dict(d_normal)})")
    av = sorted({i for rows in R.values() for r in rows if r['classement'] == A_VERIFIER for i in (r.get('ids') or [r['id']])})
    print('questions à mettre en « À vérifier » :', ', '.join(av))
