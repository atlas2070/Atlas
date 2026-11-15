/* ================= Réglages d'Atlas : tout se change ici =================
   Inséré par build.py dans dist/index.html et dist/confidentialite.html (marqueur __CONFIG__).
   Ne jamais écrire de balise fermante « script » dans ce fichier. */
const CONFIG={
  // Nom de l'association affiché sur le site (sous-titre, mentions). Vide = aucun nom affiché.
  ORG_NAME:'',
  // Adresse e-mail de contact d'Atlas (demandes de suppression, erreurs). Vide = « écris à l'équipe Atlas », sans adresse.
  CONTACT_EMAIL:'atlassante2070@gmail.com',
  // Projet Supabase : valeurs publiques par nature (les droits viennent des règles RLS).
  // Ne jamais mettre ici la clé « service_role ».
  SUPABASE_URL:'https://vwgeqjgdirasfdewukqn.supabase.co',
  SUPABASE_ANON_KEY:'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZ3Z2VxamdkaXJhc2ZkZXd1a3FuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTM2MTUyNjAsImV4cCI6MjEwOTE5MTI2MH0.yIF75nCA_uEnNAFkNLiG9X9lvx9zJVRBjtebr9l_R8k',
  // Hors ligne, le site reste ouvert ce nombre de jours après la dernière vérification de l'accès.
  OFFLINE_DAYS:30
};
