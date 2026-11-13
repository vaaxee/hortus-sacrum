-- Hortus Sacrum : un magasin de documents par utilisateur, synchronisé avec la base locale (IndexedDB) de chaque appareil.
-- Appliquée au projet Supabase « hortus-sacrum » (jlbcpkmysmdehjocqzmb) le 13 novembre 2026.
create table public.documents (
  user_id uuid not null default auth.uid() references auth.users (id) on delete cascade,
  collection text not null check (collection in ('textes','pratiques','liste','recueils','meditations','fetes','notes','coches','faits','versions')),
  id text not null check (char_length(id) between 1 and 300),
  contenu jsonb not null,
  modifie_le timestamptz not null,
  efface boolean not null default false,
  maj_serveur timestamptz not null default now(),
  primary key (user_id, collection, id)
);

comment on table public.documents is 'Données de l''utilisateur (prières, pratiques, liste, coches…), une ligne par objet ; efface = suppression à propager aux autres appareils.';

create index documents_user_maj on public.documents (user_id, maj_serveur);

-- l'horodatage serveur sert de curseur de synchronisation : toujours fixé par le serveur
create or replace function public.documents_horodater() returns trigger
language plpgsql set search_path = '' as $$
begin
  new.maj_serveur := now();
  return new;
end $$;

create trigger documents_horodater before insert or update on public.documents
for each row execute function public.documents_horodater();

alter table public.documents enable row level security;

create policy "lire ses documents" on public.documents for select to authenticated
  using ((select auth.uid()) = user_id);
create policy "ajouter ses documents" on public.documents for insert to authenticated
  with check ((select auth.uid()) = user_id);
create policy "modifier ses documents" on public.documents for update to authenticated
  using ((select auth.uid()) = user_id) with check ((select auth.uid()) = user_id);
create policy "supprimer ses documents" on public.documents for delete to authenticated
  using ((select auth.uid()) = user_id);

revoke all on public.documents from anon;
grant select, insert, update, delete on public.documents to authenticated;
