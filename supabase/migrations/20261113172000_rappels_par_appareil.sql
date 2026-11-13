-- Rappels sans compte : un appareil est désigné par un identifiant aléatoire (gardé sur l'appareil).
-- Les écritures passent par la fonction « rappels-appareil » (rôle service) ; aucune règle d'accès public n'est ajoutée.
alter table public.abonnements_push alter column user_id drop not null, alter column user_id drop default;
alter table public.abonnements_push add column appareil text;
create index abonnements_push_appareil on public.abonnements_push (appareil);
alter table public.rappels_prevus alter column user_id drop not null, alter column user_id drop default;
alter table public.rappels_prevus add column appareil text;
create index rappels_prevus_appareil on public.rappels_prevus (appareil);
alter table public.abonnements_push add constraint abonnement_proprietaire check (user_id is not null or appareil is not null);
alter table public.rappels_prevus add constraint rappel_proprietaire check (user_id is not null or appareil is not null);
