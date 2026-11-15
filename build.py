#!/usr/bin/env python3
"""Construit le site dans dist/ : dist/index.html (une seule page, avec src/config.js et src/compte.js intégrés)
+ dist/confidentialite.html + dist/pages/*.jpg.
Usage : python3 build.py"""
import json, os, shutil
ROOT = os.path.dirname(os.path.abspath(__file__))
D = lambda *p: os.path.join(ROOT, *p)
FILES = ['data_S1.json', 'data_m2_23.json', 'data_new.json', 'data_las25.json']
qs = []
for f in FILES:
    qs += json.load(open(D('data', f), encoding='utf-8'))
ids = [q['id'] for q in qs]
assert len(ids) == len(set(ids)), 'identifiants de questions en double'
tpl = open(D('src', 'app_template.html'), encoding='utf-8').read()
compte = open(D('src', 'compte.js'), encoding='utf-8').read()
config = open(D('src', 'config.js'), encoding='utf-8').read()
for nom, txt in (('compte.js', compte), ('config.js', config)):
    assert '</script' not in txt.lower(), nom + ' ne doit pas contenir de balise fermante script'
tpl = tpl.replace('__CONFIG__', config).replace('__COMPTE__', compte)
html = (tpl.replace('__DATA__', json.dumps(qs, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/'))
           .replace('__LASS__', open(D('data', 'lass.json'), encoding='utf-8').read())
           .replace('__HB__', open(D('data', 'hb.json'), encoding='utf-8').read()))
out = D('dist')
shutil.rmtree(out, ignore_errors=True)
os.makedirs(out)
# la page publiée sur claude.ai recevait automatiquement l'en-tête <html>/<meta charset> ; ici on l'ajoute
head = '<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"></head><body>'
open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(head + html + '</body></html>')
shutil.copytree(D('public', 'pages'), os.path.join(out, 'pages'))
conf = open(D('src', 'confidentialite.html'), encoding='utf-8').read().replace('__CONFIG__', config)
open(os.path.join(out, 'confidentialite.html'), 'w', encoding='utf-8').write(conf)
print(f'{len(qs)} questions -> dist/index.html ({os.path.getsize(os.path.join(out, "index.html"))//1024} Ko) + {len(os.listdir(os.path.join(out, "pages")))} images')
