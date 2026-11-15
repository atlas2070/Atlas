-- Atlas v2 : avis, suivi des signalements, statistiques anonymes du projet.
-- À coller UNE FOIS dans Supabase → SQL Editor → New query → Run (après setup.sql). Peut être relancé sans danger.

-- =========================================================================
-- 1. Signalements : statut et réponse de l'équipe, visibles par leur auteur
-- =========================================================================
alter table public.reports add column if not exists status     text not null default 'nouveau';
alter table public.reports add column if not exists reponse    text;
alter table public.reports add column if not exists repondu_at timestamptz;
alter table public.reports drop constraint if exists reports_status_ok;
alter table public.reports add constraint reports_status_ok
  check (status in ('nouveau','en_cours','corrige','pas_erreur') and (reponse is null or length(reponse) <= 2000));
update public.reports set status = 'corrige' where done and status = 'nouveau';

grant update (done, status, reponse, repondu_at) on table public.reports to authenticated;
drop policy if exists "signalement : lecture auteur" on public.reports;
create policy "signalement : lecture auteur" on public.reports for select to authenticated
  using (user_id = auth.uid() and public.is_member());

-- =========================================================================
-- 2. Avis et idées d'amélioration
-- =========================================================================
create table if not exists public.feedback(
  id         uuid primary key default gen_random_uuid(),
  user_id    uuid default auth.uid() references auth.users(id) on delete set null,
  kind       text not null default 'avis' check (kind in ('avis','idee','bug')),
  note       smallint check (note between 1 and 5),
  message    text not null check (length(message) between 1 and 2000),
  created_at timestamptz not null default now(),
  status     text not null default 'nouveau' check (status in ('nouveau','en_cours','fait','pas_retenu')),
  reponse    text check (length(reponse) <= 2000),
  repondu_at timestamptz);
alter table public.feedback enable row level security;
create index if not exists feedback_created_at on public.feedback(created_at desc);

revoke all on table public.feedback from anon, authenticated;
grant select, insert on table public.feedback to authenticated;
grant update (status, reponse, repondu_at) on table public.feedback to authenticated;

drop policy if exists "avis : ajout membre"    on public.feedback;
drop policy if exists "avis : lecture auteur"  on public.feedback;
drop policy if exists "avis : lecture admin"   on public.feedback;
drop policy if exists "avis : modif admin"     on public.feedback;
create policy "avis : ajout membre" on public.feedback for insert to authenticated
  with check (user_id = auth.uid() and status = 'nouveau' and reponse is null and public.is_member());
create policy "avis : lecture auteur" on public.feedback for select to authenticated
  using (user_id = auth.uid() and public.is_member());
create policy "avis : lecture admin" on public.feedback for select to authenticated
  using (public.is_admin());
create policy "avis : modif admin" on public.feedback for update to authenticated
  using (public.is_admin()) with check (public.is_admin());

-- =========================================================================
-- 3. Statistiques du projet : chiffres globaux et anonymes, pour les admins
--    La fonction ne renvoie que des totaux : aucun e-mail, aucun identifiant, aucune ligne par élève.
--    Les élèves qui ont désactivé « statistiques anonymes » (state.noStats) ne sont pas comptés
--    dans les questions, la réussite ni le temps.
-- =========================================================================
create or replace function public.project_stats() returns jsonb
  language plpgsql stable security definer set search_path = public as $$
declare r jsonb;
begin
  if not public.is_admin() then raise exception 'réservé aux administrateurs'; end if;
  with p as (
    select state, updated_at from public.progress
    where coalesce((state->>'noStats')::boolean, false) = false),
  a as (select e.key as qid, (e.value->>'s')::numeric as s, coalesce((e.value->>'n')::int, 1) as n
        from p, jsonb_each(case when jsonb_typeof(p.state->'ans') = 'object' then p.state->'ans' else '{}'::jsonb end) e
        where jsonb_typeof(e.value) = 'object'),
  d as (select e.key::date as jour, sum((e.value)::text::numeric) as sec
        from p, jsonb_each(case when jsonb_typeof(p.state->'time'->'d') = 'object' then p.state->'time'->'d' else '{}'::jsonb end) e
        where e.key ~ '^\d{4}-\d{2}-\d{2}$' and jsonb_typeof(e.value) = 'number'
        group by 1)
  select jsonb_build_object(
    'membres',      (select count(*) from public.members),
    'connectes',    (select count(*) from auth.users u join public.members m on m.email = lower(u.email) where u.last_sign_in_at is not null),
    'actifs7',      (select count(*) from public.progress where updated_at > now() - interval '7 days'),
    'actifs30',     (select count(*) from public.progress where updated_at > now() - interval '30 days'),
    'partagent',    (select count(*) from p),
    'faites',       (select count(*) from a),
    'tentatives',   (select coalesce(sum(n), 0) from a),
    'reussite',     (select round(avg(s), 4) from a),
    'par_question', (select coalesce(jsonb_object_agg(qid, jsonb_build_array(c, m)), '{}'::jsonb)
                     from (select qid, count(*) c, round(avg(s), 3) m from a group by qid) x),
    'secondes',     (select coalesce(sum(coalesce((state->'time'->>'tot')::numeric, 0)), 0) from p
                     where jsonb_typeof(state->'time'->'tot') = 'number'),
    'par_jour',     (select coalesce(jsonb_object_agg(jour::text, sec), '{}'::jsonb) from d where jour > current_date - 90),
    'signalements', (select jsonb_build_object('total', count(*),
                       'nouveau', count(*) filter (where status = 'nouveau'),
                       'en_cours', count(*) filter (where status = 'en_cours'),
                       'traites', count(*) filter (where status in ('corrige','pas_erreur'))) from public.reports),
    'avis',         (select jsonb_build_object('total', count(*), 'note_moy', round(avg(note), 2),
                       'idees', count(*) filter (where kind = 'idee'), 'bugs', count(*) filter (where kind = 'bug'),
                       'nouveau', count(*) filter (where status = 'nouveau')) from public.feedback)
  ) into r;
  return r;
end $$;
revoke all on function public.project_stats() from public;
grant execute on function public.project_stats() to authenticated;
