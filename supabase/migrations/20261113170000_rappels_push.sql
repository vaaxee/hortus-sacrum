-- Rappels (notifications push) : abonnements des appareils et rappels planifiés par l'app.
create extension if not exists pg_cron;
create extension if not exists pg_net schema extensions;

create table public.abonnements_push (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null default auth.uid() references auth.users on delete cascade,
  endpoint text not null unique,
  p256dh text not null,
  auth text not null,
  cree_le timestamptz not null default now()
);
alter table public.abonnements_push enable row level security;
create policy "abonnements : les siens" on public.abonnements_push
  for all to authenticated using ((select auth.uid()) = user_id) with check ((select auth.uid()) = user_id);
create index abonnements_push_user on public.abonnements_push (user_id);

create table public.rappels_prevus (
  id bigint generated always as identity primary key,
  user_id uuid not null default auth.uid() references auth.users on delete cascade,
  quand timestamptz not null,
  titre text not null,
  corps text not null default '',
  url text not null default '/',
  envoye_le timestamptz
);
alter table public.rappels_prevus enable row level security;
create policy "rappels : les siens" on public.rappels_prevus
  for all to authenticated using ((select auth.uid()) = user_id) with check ((select auth.uid()) = user_id);
create index rappels_prevus_a_envoyer on public.rappels_prevus (quand) where envoye_le is null;
create index rappels_prevus_user on public.rappels_prevus (user_id);

-- Secrets (créés à part, jamais versionnés) : vault « vapid_prive », « vapid_public », « cle_cron ».
create or replace function public.secrets_rappels()
returns table (nom text, valeur text)
language sql security definer set search_path = ''
as $$ select name, decrypted_secret from vault.decrypted_secrets where name in ('vapid_prive', 'vapid_public', 'cle_cron') $$;
revoke all on function public.secrets_rappels() from public, anon, authenticated;
grant execute on function public.secrets_rappels() to service_role;

-- Tâche planifiée : chaque minute, appeler la fonction d'envoi.
select cron.schedule('envoyer-rappels', '* * * * *', $$ select net.http_post(
  url := 'https://jlbcpkmysmdehjocqzmb.supabase.co/functions/v1/envoyer-rappels',
  headers := jsonb_build_object('Content-Type', 'application/json',
             'x-cle', (select decrypted_secret from vault.decrypted_secrets where name = 'cle_cron')),
  body := '{}'::jsonb, timeout_milliseconds := 20000) $$);
