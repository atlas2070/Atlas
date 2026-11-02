#!/usr/bin/env python3
"""Intègre dans data/*.json les explications rédigées à partir des cours.

Usage : python3 tools/appliquer_explications.py CHEMIN/atlas-cours/paquets

Lit paquets/lot-XXX.json (sources des extraits) et paquets/reponses/lot-XXX.json
(explications). Ne modifie JAMAIS : énoncés, propositions, vrai/faux, réponses.
Remplace l'explication de chaque proposition traitée ; met à jour status, src et note.
Les désaccords avec le cours ne changent pas la réponse : la question passe
« À vérifier (désaccord avec le cours) » et part dans docs/A_TRANCHER.md.
Aucun extrait de cours n'est copié dans ce dépôt (seulement « fichier, page »).
"""
import json, os, sys, glob, copy, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILES = ['data_S1', 'data_m2_23', 'data_new', 'data_las25']
def _court(src):
    m = re.match(r'(.*?)( p\.\d+| \(partie \d+\))?$', src.strip())
    name = re.sub(r'\.(pdf|docx|pptx|odt)$', '', m.group(1).split('/')[-1], flags=re.I)
    return re.sub(r'(?i)poly\s*tutorat|tutorat', 'poly', name).strip() + (m.group(2) or '')

VERDICTS = {'ok', 'sans_source', 'incertain', 'contredit', 'langue'}

def main(pq):
    sources, rep = {}, {}
    for f in sorted(glob.glob(os.path.join(pq, 'lot-*.json'))):
        for q in json.load(open(f, encoding='utf-8')):
            sources[q['id']] = {e['id']: e['source'] for e in q.get('extraits', [])}
    for f in sorted(glob.glob(os.path.join(pq, 'reponses', 'lot-*.json'))):
        try:
            for qid, items in json.load(open(f, encoding='utf-8')).items():
                rep.setdefault(qid, {}).update(items)  # lots R (rattrapage) complètent les lettres manquantes
        except Exception as e:
            print('FICHIER ILLISIBLE (ignoré) :', f, e)
    a_trancher, n_q, n_items, ignores = [], 0, 0, []
    for name in FILES:
        p = os.path.join(ROOT, 'data', name + '.json')
        raw = open(p, encoding='utf-8').read()
        data = json.loads(raw)
        before = copy.deepcopy(data)
        for q in data:
            r = rep.get(q['id'])
            if not r or q.get('tranche'):  # tranche : décision humaine, ne jamais écraser
                continue
            src_used, contre, verdicts = [], [], []
            for it in q['items']:
                v = r.get(it['l'])
                if not isinstance(v, list) or len(v) < 3 or v[2] not in VERDICTS:
                    if v is not None:
                        ignores.append(f"{q['id']}{it['l']}")
                    continue
                ex, eid, verdict = (v + [''])[:3]
                verdicts.append(verdict)
                if verdict == 'contredit':
                    contre.append((it['l'], v[3] if len(v) > 3 else ''))
                    it['ex'] = ''
                else:
                    it['ex'] = str(ex).strip()
                s = sources.get(q['id'], {}).get(eid)
                s = _court(s) if s else s
                if s and s not in src_used:
                    src_used.append(s)
                n_items += 1
            if not verdicts:
                continue
            n_q += 1
            q['exSrc'] = 'cours'
            if src_used:
                q['src'] = 'Cours : ' + ' ; '.join(src_used[:3])
            st = q.get('status', '')
            if contre:
                q['status'] = 'À vérifier (désaccord avec le cours)'
                q['note'] = re.sub(r'\s*\(E\d+(, ?E\d+)*\)', '', ' '.join(f"Proposition {l} : {why}" for l, why in contre)).strip()
                a_trancher.append((q['id'], q.get('ans', ''), contre, q.get('src', '')))
            elif all(x in ('ok', 'langue') for x in verdicts) and src_used and (
                    st.startswith('Non comparée') or st.startswith('Incertaine') or st.startswith('Correction unique')):
                q['status'] = 'Confirmée par le cours'
        # garde-fou : rien d'autre que ex / status / src / note / exSrc ne doit bouger
        for a, b in zip(before, data):
            assert a['id'] == b['id'] and a.get('ans') == b.get('ans') and a.get('stem') == b.get('stem'), a['id']
            assert [(i['l'], i.get('v'), i.get('t')) for i in a['items']] == \
                   [(i['l'], i.get('v'), i.get('t')) for i in b['items']], a['id']
        out = json.dumps(data, ensure_ascii=False) if raw.count('\n') < 3 else json.dumps(data, ensure_ascii=False, indent=0)
        open(p, 'w', encoding='utf-8').write(out)
    with open(os.path.join(ROOT, 'docs', 'A_TRANCHER.md'), 'w', encoding='utf-8') as f:
        f.write('# Désaccords avec le cours, à trancher par l\'équipe\n\n'
                'Produit par `tools/appliquer_explications.py`. La réponse affichée n\'a PAS été changée : '
                'vérifier dans le cours puis corriger à la main (garder `orig`, remplir `src` et `note`).\n\n'
                '| Question | Réponse actuelle | Proposition(s) | Pourquoi | Source |\n|---|---|---|---|---|\n')
        for i, ans, c, s in a_trancher:
            f.write(f"| {i} | {ans} | {', '.join(l for l, _ in c)} | {' / '.join(w for _, w in c)} | {s} |\n")
    print(f'{n_q} questions mises à jour, {n_items} propositions, {len(a_trancher)} désaccords (docs/A_TRANCHER.md)')
    if ignores:
        print('Entrées mal formées ignorées :', ', '.join(ignores[:30]))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
