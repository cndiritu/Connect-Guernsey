const { getSupabase, headers, ok, err } = require("./utils");

exports.handler = async (event) => {
  if (event.httpMethod === "OPTIONS") {
    return { statusCode: 204, headers };
  }
  try {
    const db = getSupabase();
    const { data, error } = await db
      .from("site_settings")
      .select("key,value");
    if (error) return err(500, error.message);
    const settings = {};
    for (const row of data || []) {
      settings[row.key] = row.value;
    }
    return ok(settings);
  } catch (e) {
    return err(500, e.message);
  }
};
