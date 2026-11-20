#!/usr/bin/env python3
"""Repère les questions qui retombent d'une année à l'autre -> data/retombes.json ({id: [ids des autres années]}).
Deux questions de même matière et d'années différentes sont « la même » si au moins 3 propositions sont quasi
identiques (similarité >= 0,85), ou 2 avec un énoncé quasi identique (>= 0,8).
Les questions dont l'énoncé est une figure (forceImg, ex. molécules en chimie) sont exclues : leurs propositions
types (« la molécule F est de configuration R ») reviennent chaque année avec une figure différente.
Lancé automatiquement par build.py dès que les questions changent (empreinte stockée dans le fichier) ; ~1 min.
À la main : python3 tools/retombes.py"""
import json, os, re, unicodedata, difflib, collections, hashlib
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'data', 'retombes.json')
def norm(s):
    s = unicodedata.normalize('NFKD', re.sub(r'<[^>]+>', '', s or '').lower().replace('’', "'"))
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return re.sub(r'[^a-z0-9]+', ' ', s).strip()
sim = lambda a, b: difflib.SequenceMatcher(None, a, b).ratio()

def empreinte(qs):
    """Change dès qu'une question est ajoutée, retirée ou que son texte / sa matière / son année change."""
    cle = sorted((q['id'], q['y'], q.get('mat'), q['stem'], [i['t'] for i in q['items']], bool(q.get('forceImg'))) for q in qs)
    return hashlib.sha256(json.dumps(cle, ensure_ascii=False).encode()).hexdigest()[:16]

def charger(qs):
    """Renvoie {id: [ids]} à jour : relit le fichier si l'empreinte correspond, sinon recalcule et l'écrit."""
    h = empreinte(qs)
    try:
        d = json.load(open(OUT, encoding='utf-8'))
        if d.get('empreinte') == h:
            return d['q']
    except (OSError, ValueError, KeyError):
        pass
    print('Questions modifiées : recherche des questions retombées (~1 min)…')
    r = calculer(qs)
    json.dump({'empreinte': h, 'q': r}, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    print(len(r), 'questions retombées -> data/retombes.json')
    return r

def calculer(qs):
  qs = [dict(q) for q in qs if not q.get('forceImg')]
  for q in qs:
      q['_it'] = [x for x in (norm(i['t']) for i in q['items']) if len(x) >= 15]
      q['_st'] = norm(q['stem'])
  par_mat = collections.defaultdict(list)
  for q in qs:
      par_mat[q.get('mat')].append(q)
  lien = collections.defaultdict(set)
  for L in par_mat.values():
      for i, a in enumerate(L):
          for b in L[i + 1:]:
              if a['y'] == b['y']:
                  continue
              n = sum(1 for x in a['_it'] if any(abs(len(x) - len(y)) < .3 * len(x) and sim(x, y) >= .85 for y in b['_it']))
              if n >= 3 or (n == 2 and sim(a['_st'], b['_st']) >= .8):
                  lien[a['id']].add(b['id']); lien[b['id']].add(a['id'])
  return {k: sorted(v) for k, v in sorted(lien.items())}

if __name__ == '__main__':
    import sys; sys.path.insert(0, ROOT)
    FILES = ['data_S1.json', 'data_m2_23.json', 'data_new.json', 'data_las25.json', 'data_s2.json']
    tout = [q for f in FILES for q in json.load(open(os.path.join(ROOT, 'data', f), encoding='utf-8'))]
    try: os.remove(OUT)
    except OSError: pass
    charger(tout)
