// Rappels sans compte : l'app désigne l'appareil par un identifiant aléatoire qu'elle garde, et confie ici
// son abonnement push et ses rappels à venir. Écrit avec le rôle service (pas d'accès public aux tables).
// Déployée sans vérification JWT.
import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "npm:@supabase/supabase-js@2.45.4";

const db = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);
const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
  "Access-Control-Allow-Headers": "content-type, authorization, apikey, x-client-info",
};
const rep = (corps: unknown, status = 200) =>
  new Response(JSON.stringify(corps), { status, headers: { ...CORS, "Content-Type": "application/json" } });
const court = (s: unknown, n: number) => String(s ?? "").slice(0, n);

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") return new Response(null, { headers: CORS });
  if (req.method !== "POST") return rep({ erreur: "méthode" }, 405);
  let m: Record<string, any>;
  try { m = await req.json(); } catch { return rep({ erreur: "json" }, 400); }
  const appareil = String(m.appareil ?? "");
  if (!/^[A-Za-z0-9_-]{22,64}$/.test(appareil)) return rep({ erreur: "appareil" }, 400);

  switch (m.action) {
    case "abonner": {
      const a = m.abonnement ?? {};
      if (!/^https:\/\//.test(a.endpoint ?? "") || !a.keys?.p256dh || !a.keys?.auth) return rep({ erreur: "abonnement" }, 400);
      const { error } = await db.from("abonnements_push").upsert(
        { endpoint: court(a.endpoint, 1000), p256dh: court(a.keys.p256dh, 200), auth: court(a.keys.auth, 100), appareil, user_id: null },
        { onConflict: "endpoint" },
      );
      return error ? rep({ erreur: error.message }, 500) : rep({ ok: true });
    }
    case "desabonner": {
      await db.from("abonnements_push").delete().eq("appareil", appareil);
      await db.from("rappels_prevus").delete().eq("appareil", appareil).is("envoye_le", null);
      return rep({ ok: true });
    }
    case "planifier": {
      const liste = Array.isArray(m.rappels) ? m.rappels.slice(0, 1000) : [];
      const maintenant = new Date().toISOString();
      await db.from("rappels_prevus").delete().eq("appareil", appareil).is("envoye_le", null).gte("quand", maintenant);
      const lignes = liste
        .filter((r: any) => !Number.isNaN(Date.parse(r.quand)))
        .map((r: any) => ({ appareil, quand: new Date(r.quand).toISOString(), titre: court(r.titre, 120), corps: court(r.corps, 400), url: court(r.url, 300) || "/" }));
      for (let i = 0; i < lignes.length; i += 300) {
        const { error } = await db.from("rappels_prevus").insert(lignes.slice(i, i + 300));
        if (error) return rep({ erreur: error.message }, 500);
      }
      return rep({ ok: true, rappels: lignes.length });
    }
    case "essai": {
      const { error } = await db.from("rappels_prevus").insert({
        appareil, quand: new Date().toISOString(), titre: "Hortus Sacrum", corps: "Les rappels fonctionnent sur cet appareil.", url: "/",
      });
      return error ? rep({ erreur: error.message }, 500) : rep({ ok: true });
    }
    default:
      return rep({ erreur: "action" }, 400);
  }
});
