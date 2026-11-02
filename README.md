# Atlas

Annales corrigées du S1 de Tours (PASS, L.AS bio, L.AS hors-bio), par l'équipe Atlas. Réservé aux membres inscrits.

Site : https://atlas2070.github.io/Atlas/ (publié automatiquement à chaque push sur `main`).

```bash
python3 build.py                      # construit dist/
python3 -m http.server -d dist 8000   # puis ouvrir http://localhost:8000
```

En local, la connexion passe par le vrai projet Supabase : ton adresse doit être dans la table `members`.

- Mise en ligne et réglages Supabase (à faire une fois) : `docs/DEPLOIEMENT.md`
- Réglages (nom de l'association, e-mail de contact, Supabase) : `src/config.js`
- Base de données : `supabase/setup.sql`
- Consignes de travail et règles de contenu : `CLAUDE.md`
- Format des données : `docs/DONNEES.md`
- État du projet et suite : `docs/PASSATION.md`
