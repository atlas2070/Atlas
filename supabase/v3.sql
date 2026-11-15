-- Atlas v3 : les admins peuvent aussi changer le chapitre et le type (QCM / QCS) d'une question.
-- À coller UNE FOIS dans Supabase → SQL Editor → New query → Run (après corrections.sql). Peut être relancé sans danger.
alter table public.corrections add column if not exists ch   text check (length(ch) <= 200);
alter table public.corrections add column if not exists type text check (type in ('QCM','QCS','QRM','QRU'));
