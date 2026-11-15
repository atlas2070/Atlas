-- Atlas : corrections modifiées depuis le site par les administrateurs.
-- À exécuter UNE FOIS dans Supabase → SQL Editor → New query → coller → Run.
-- Les membres lisent les corrections ; seuls les admins écrivent. Chaque changement est gardé dans corrections_log.

create table if not exists public.corrections(
  question_id text primary key check (length(question_id) <= 100),
  ans         text not null check (ans ~ '^[A-E]{0,5}$'),
  ex          jsonb not null default '{}'::jsonb check (length(ex::text) <= 20000),
  note        text check (length(note) <= 2000),
  updated_by  text,
  updated_at  timestamptz not null default now());
alter table public.corrections enable row level security;
revoke all on table public.corrections from anon, authenticated;
grant select, insert, update, delete on table public.corrections to authenticated;

drop policy if exists "correction : lecture membre" on public.corrections;
drop policy if exists "correction : ajout admin"    on public.corrections;
drop policy if exists "correction : modif admin"    on public.corrections;
drop policy if exists "correction : retrait admin"  on public.corrections;
create policy "correction : lecture membre" on public.corrections for select to authenticated using (public.is_member());
create policy "correction : ajout admin"    on public.corrections for insert to authenticated with check (public.is_admin());
create policy "correction : modif admin"    on public.corrections for update to authenticated using (public.is_admin()) with check (public.is_admin());
create policy "correction : retrait admin"  on public.corrections for delete to authenticated using (public.is_admin());

-- Historique : qui a changé quoi, et quand (lisible par les admins seulement)
create table if not exists public.corrections_log(
  id          bigserial primary key,
  question_id text not null,
  avant       jsonb,
  apres       jsonb,
  par         text,
  le          timestamptz not null default now());
alter table public.corrections_log enable row level security;
revoke all on table public.corrections_log from anon, authenticated;
grant select on table public.corrections_log to authenticated;
drop policy if exists "historique : lecture admin" on public.corrections_log;
create policy "historique : lecture admin" on public.corrections_log for select to authenticated using (public.is_admin());

create or replace function public.log_correction() returns trigger
language plpgsql security definer set search_path = public as $$
begin
  insert into public.corrections_log(question_id, avant, apres, par)
  values (coalesce(new.question_id, old.question_id),
          case when tg_op = 'INSERT' then null else to_jsonb(old) end,
          case when tg_op = 'DELETE' then null else to_jsonb(new) end,
          auth.jwt() ->> 'email');
  return coalesce(new, old);
end $$;
drop trigger if exists corrections_log_trg on public.corrections;
create trigger corrections_log_trg after insert or update or delete on public.corrections
  for each row execute function public.log_correction();
