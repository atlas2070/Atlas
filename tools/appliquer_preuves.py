#!/usr/bin/env python3
"""2e passe : intègre les preuves trouvées dans le cours (paquets/preuves/reponses/P-XXX.json).

Usage : python3 tools/appliquer_preuves.py CHEMIN/atlas-cours/paquets

Ne modifie JAMAIS : énoncés, propositions, vrai/faux, réponses.
- « ok » : ajoute la source du cours ; remplit l'explication si une nouvelle est fournie.
- Une question dont toutes les propositions sont prouvées (1re passe ok/langue + 2e passe ok)
  passe « Confirmée par le cours ».
- « contredit » : la question passe « À vérifier (désaccord avec le cours) », listée dans docs/A_TRANCHER_2.md.
Les questions marquées `tranche` (décision humaine) ne sont pas touchées.
"""
import json, os, sys, glob, copy, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from appliquer_explications import _court, FILES

def main(pq):
    rep1, sources, rep2 = {}, {}, {}
    for f in sorted(glob.glob(os.path.join(pq, 'reponses', 'lot-*.json'))):
        for qid, items in json.load(open(f, encoding='utf-8')).items():
            rep1.setdefault(qid, {}).update(items)
    for f in sorted(glob.glob(os.path.join(pq, 'preuves', 'P-*.json'))):
        for q in json.load(open(f, encoding='utf-8')):
            sources[q['id']] = {e['id']: e['source'] for e in q.get('extraits', [])}
    for f in sorted(glob.glob(os.path.join(pq, 'preuves', 'reponses', 'P-*.json'))):
        try:
            for qid, items in json.load(open(f, encoding='utf-8')).items():
                rep2.setdefault(qid, {}).update(items)
        except Exception as e:
            print('FICHIER ILLISIBLE (ignoré) :', f, e)
    n_ok = n_conf = 0; contre_list = []
    for name in FILES:
        p = os.path.join(ROOT, 'data', name + '.json')
        raw = open(p, encoding='utf-8').read(); data = json.loads(raw); before = copy.deepcopy(data)
        for q in data:
            r2 = rep2.get(q['id'])
            if not r2 or q.get('tranche'):
                continue
            r1 = rep1.get(q['id'], {})
            src = [s.strip() for s in (q.get('src') or '')[len('Cours : '):].split(' ; ')] if (q.get('src') or '').startswith('Cours : ') else []
            proved, contre = [], []
            for it in q['items']:
                v1 = r1.get(it['l']); v2 = r2.get(it['l'])
                if isinstance(v1, list) and len(v1) > 2 and v1[2] in ('ok', 'langue'):
                    proved.append(it['l'])
                if not isinstance(v2, list) or len(v2) < 2:
                    continue
                eid, verdict = v2[0], v2[1]
                if verdict == 'ok' and sources.get(q['id'], {}).get(eid):
                    s = _court(sources[q['id']][eid])
                    if s not in src: src.append(s)
                    proved.append(it['l']); n_ok += 1
                    if len(v2) > 2 and str(v2[2]).strip():
                        it['ex'] = str(v2[2]).strip()
                elif verdict == 'contredit':
                    contre.append((it['l'], v2[2] if len(v2) > 2 else ''))
            if src:
                q['src'] = 'Cours : ' + ' ; '.join(src[:4]); q['exSrc'] = 'cours'
            if contre:
                q['status'] = 'À vérifier (désaccord avec le cours)'
                q['note'] = ' '.join(f"Proposition {l} : {w}" for l, w in contre)
                contre_list.append((q['id'], q.get('ans', ''), contre, q.get('src', '')))
            elif all(it['l'] in proved for it in q['items']) and not q['status'].startswith(('À vérifier', 'Rectification')):
                if not q['status'].startswith('Confirmée'): n_conf += 1
                q['status'] = 'Confirmée par le cours'
        for a, b in zip(before, data):
            assert a['id'] == b['id'] and a.get('ans') == b.get('ans') and a.get('stem') == b.get('stem'), a['id']
            assert [(i['l'], i.get('v'), i.get('t')) for i in a['items']] == [(i['l'], i.get('v'), i.get('t')) for i in b['items']], a['id']
        out = json.dumps(data, ensure_ascii=False) if raw.count('\n') < 3 else json.dumps(data, ensure_ascii=False, indent=0)
        open(p, 'w', encoding='utf-8').write(out)
    with open(os.path.join(ROOT, 'docs', 'A_TRANCHER_2.md'), 'w', encoding='utf-8') as f:
        f.write("# 2e passe : désaccords avec le cours, à trancher\n\nLa réponse affichée n'a PAS été changée.\n\n"
                '| Question | Réponse actuelle | Proposition(s) | Pourquoi | Source |\n|---|---|---|---|---|\n')
        for i, ans, c, s in contre_list:
            f.write(f"| {i} | {ans} | {', '.join(l for l, _ in c)} | {' / '.join(w for _, w in c)} | {s} |\n")
    print(f'{n_ok} propositions prouvées par le cours, {n_conf} questions passées « Confirmée par le cours », '
          f'{len(contre_list)} désaccords (docs/A_TRANCHER_2.md)')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
