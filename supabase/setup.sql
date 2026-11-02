-- Atlas : tables, fonctions et règles d'accès.
-- À coller dans Supabase → SQL Editor → New query → Run. Le script peut être relancé sans danger.
-- Ensuite, dans une requête à part, ajoute-toi en administrateur (voir docs/DEPLOIEMENT.md) :
--   insert into public.members(email, role) values ('ton.adresse@exemple.fr', 'admin');

-- =========================================================================
-- 1. Membres (adresses autorisées à se connecter)
-- =========================================================================
create table if not exists public.members(
  email    text primary key check (email = lower(email) and email = trim(email)),
  role     text not null default 'member' check (role in ('member','admin')),
  note     text,
  added_at timestamptz not null default now());
alter table public.members enable row level security;

-- Vrai si la personne connectée est administratrice.
create or replace function public.is_admin() returns boolean
  language sql stable security definer set search_path = public as $$
  select exists(select 1 from public.members
    where email = lower(auth.jwt()->>'email') and role = 'admin') $$;

-- Vrai si la personne connectée est sur la liste des membres.
create or replace function public.is_member() returns boolean
  language sql stable security definer set search_path = public as $$
  select exists(select 1 from public.members
    where email = lower(auth.jwt()->>'email')) $$;

-- Avant l'envoi du code : l'adresse est-elle sur la liste ? (appelée sans être connecté)
create or replace function public.can_join(e text) returns boolean
  language sql stable security definer set search_path = public as $$
  select exists(select 1 from public.members where email = lower(trim(e))) $$;

revoke all on function public.is_admin()      from public;
revoke all on function public.is_member()     from public;
revoke all on function public.can_join(text)  from public;
grant execute on function public.is_admin()     to authenticated;
grant execute on function public.is_member()    to authenticated;
grant execute on function public.can_join(text) to anon, authenticated;

revoke all on table public.members from anon, authenticated;
grant select, insert, update, delete on table public.members to authenticated;

drop policy if exists "lecture"       on public.members;
drop policy if exists "ajout admin"   on public.members;
drop policy if exists "modif admin"   on public.members;
drop policy if exists "retrait admin" on public.members;
-- Chacun voit sa propre ligne ; un admin voit toute la liste.
create policy "lecture" on public.members for select to authenticated
  using (email = lower(auth.jwt()->>'email') or public.is_admin());
create policy "ajout admin" on public.members for insert to authenticated
  with check (public.is_admin());
create policy "modif admin" on public.members for update to authenticated
  using (public.is_admin()) with check (public.is_admin());
create policy "retrait admin" on public.members for delete to authenticated
  using (public.is_admin());

-- =========================================================================
-- 2. Progression (une ligne par élève)
-- =========================================================================
create table if not exists public.progress(
  user_id    uuid primary key references auth.users(id) on delete cascade,
  state      jsonb not null default '{}'::jsonb,
  updated_at timestamptz not null default now());
alter table public.progress enable row level security;

-- La version la plus récente gagne : une écriture plus ancienne que la ligne enregistrée
-- (autre appareil resté hors ligne) est ignorée. Une date dans le futur (horloge déréglée)
-- est ramenée à l'heure du serveur.
create or replace function public.progress_newer_wins() returns trigger
  language plpgsql set search_path = public as $$
begin
  if new.updated_at is null or new.updated_at > now() + interval '1 minute' then
    new.updated_at := now();
  end if;
  if tg_op = 'UPDATE' and new.updated_at < old.updated_at then
    return null;
  end if;
  return new;
end $$;
revoke all on function public.progress_newer_wins() from public;
drop trigger if exists progress_newer_wins on public.progress;
create trigger progress_newer_wins before insert or update on public.progress
  for each row execute function public.progress_newer_wins();

revoke all on table public.progress from anon, authenticated;
grant select, insert, update on table public.progress to authenticated;

drop policy if exists "progression : lecture" on public.progress;
drop policy if exists "progression : ajout"   on public.progress;
drop policy if exists "progression : modif"   on public.progress;
create policy "progression : lecture" on public.progress for select to authenticated
  using (user_id = auth.uid() and public.is_member());
create policy "progression : ajout" on public.progress for insert to authenticated
  with check (user_id = auth.uid() and public.is_member());
create policy "progression : modif" on public.progress for update to authenticated
  using (user_id = auth.uid() and public.is_member())
  with check (user_id = auth.uid() and public.is_member());

-- =========================================================================
-- 3. Signalements d'erreur (ne modifient jamais une correction)
-- =========================================================================
create table if not exists public.reports(
  id          uuid primary key default gen_random_uuid(),
  user_id     uuid default auth.uid() references auth.users(id) on delete set null,
  question_id text not null check (length(question_id) <= 100),
  message     text not null check (length(message) between 1 and 2000),
  created_at  timestamptz not null default now(),
  done        boolean not null default false);
alter table public.reports enable row level security;
create index if not exists reports_created_at on public.reports(created_at desc);

revoke all on table public.reports from anon, authenticated;
grant insert, select on table public.reports to authenticated;
grant update (done) on table public.reports to authenticated;  -- un admin ne peut changer que « traité »

drop policy if exists "signalement : ajout membre" on public.reports;
drop policy if exists "signalement : lecture admin" on public.reports;
drop policy if exists "signalement : modif admin"  on public.reports;
create policy "signalement : ajout membre" on public.reports for insert to authenticated
  with check (user_id = auth.uid() and done = false and public.is_member());
create policy "signalement : lecture admin" on public.reports for select to authenticated
  using (public.is_admin());
create policy "signalement : modif admin" on public.reports for update to authenticated
  using (public.is_admin()) with check (public.is_admin());
