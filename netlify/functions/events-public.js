const { getSupabase, headers, ok, err } = require("./utils");

exports.handler = async (event) => {
  if (event.httpMethod === "OPTIONS") {
    return { statusCode: 204, headers };
  }
  try {
    const db = getSupabase();
    const { data, error } = await db
      .from("events")
      .select("*")
      .eq("is_published", true)
      .order("event_date");
    if (error) return err(500, error.message);
    return ok({ events: data || [] });
  } catch (e) {
    return err(500, e.message);
  }
};
