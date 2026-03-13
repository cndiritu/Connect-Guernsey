const { getSupabase, headers, ok, err } = require("./utils");

exports.handler = async (event) => {
  if (event.httpMethod === "OPTIONS") {
    return { statusCode: 204, headers };
  }
  try {
    const db = getSupabase();
    const { data, error } = await db
      .from("team_members")
      .select("*")
      .eq("is_active", true)
      .order("display_order");
    if (error) return err(500, error.message);
    return ok({ team: data || [] });
  } catch (e) {
    return err(500, e.message);
  }
};
