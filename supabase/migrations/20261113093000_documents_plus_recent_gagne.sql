-- Le plus récent l'emporte : une écriture plus ancienne que la version du serveur est ignorée.
create or replace function public.documents_horodater() returns trigger
language plpgsql set search_path = '' as $$
begin
  if tg_op = 'UPDATE' and new.modifie_le < old.modifie_le then
    return old;
  end if;
  new.maj_serveur := now();
  return new;
end $$;
