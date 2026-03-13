const { getSupabase, headers, ok, err } = require("./utils");

exports.handler = async (event) => {
  if (event.httpMethod === "OPTIONS") {
    return { statusCode: 204, headers };
  }
  try {
    const db = getSupabase();
    const { data, error } = await db
      .from("content_blocks")
      .select("key,value");
    if (error) return err(500, error.message);
    const content = {};
    for (const row of data || []) {
      content[row.key] = row.value;
    }
    return ok(content);
  } catch (e) {
    return err(500, e.message);
  }
};
