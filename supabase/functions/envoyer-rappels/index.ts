// Envoie les rappels arrivés à échéance (table rappels_prevus) à tous les appareils abonnés de leur utilisateur.
// Appelée chaque minute par pg_cron, avec l'en-tête x-cle (secret « cle_cron » du coffre). Déployée sans vérification JWT.
import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "npm:@supabase/supabase-js@2.45.4";
import webpush from "npm:web-push@3.6.7";

const db = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);
let secrets: Record<string, string> | null = null;

async function lireSecrets() {
  if (secrets) return secrets;
  const { data, error } = await db.rpc("secrets_rappels");
  if (error) throw error;
  secrets = Object.fromEntries((data as { nom: string; valeur: string }[]).map((s) => [s.nom, s.valeur]));
  webpush.setVapidDetails("https://hortus-sacrum.vercel.app", secrets.vapid_public, secrets.vapid_prive);
  return secrets;
}

Deno.serve(async (req: Request) => {
  const s = await lireSecrets();
  if (req.headers.get("x-cle") !== s.cle_cron) return new Response("interdit", { status: 401 });

  // rappels dus depuis moins de deux heures (au-delà, ils n'ont plus de sens)
  const maintenant = new Date();
  const { data: dus, error } = await db
    .from("rappels_prevus")
    .select("id, user_id, titre, corps, url, quand")
    .is("envoye_le", null)
    .lte("quand", maintenant.toISOString())
    .gte("quand", new Date(maintenant.getTime() - 2 * 3600e3).toISOString())
    .limit(500);
  if (error) return new Response(error.message, { status: 500 });
  if (!dus?.length) return new Response("rien", { status: 200 });

  const users = [...new Set(dus.map((r) => r.user_id))];
  const { data: abos } = await db.from("abonnements_push").select("id, user_id, endpoint, p256dh, auth").in("user_id", users);
  let envoyes = 0;
  const morts: string[] = [];
  for (const r of dus) {
    for (const a of (abos ?? []).filter((x) => x.user_id === r.user_id)) {
      try {
        await webpush.sendNotification(
          { endpoint: a.endpoint, keys: { p256dh: a.p256dh, auth: a.auth } },
          JSON.stringify({ titre: r.titre, corps: r.corps, url: r.url, tag: `rappel-${r.id}` }),
          { TTL: 3600, urgency: "high" },
        );
        envoyes++;
      } catch (e) {
        const code = (e as { statusCode?: number }).statusCode;
        if (code === 404 || code === 410) morts.push(a.id); // abonnement expiré
        else console.error("échec d'envoi", code, (e as Error).message);
      }
    }
  }
  await db.from("rappels_prevus").update({ envoye_le: maintenant.toISOString() }).in("id", dus.map((r) => r.id));
  if (morts.length) await db.from("abonnements_push").delete().in("id", morts);
  // ménage : rappels envoyés depuis plus de trois jours
  await db.from("rappels_prevus").delete().lt("quand", new Date(maintenant.getTime() - 3 * 864e5).toISOString());
  return new Response(JSON.stringify({ rappels: dus.length, envoyes }), { headers: { "Content-Type": "application/json" } });
});
