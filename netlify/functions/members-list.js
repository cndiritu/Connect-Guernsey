const { getSupabase, headers, ok, err } = require("./utils");

exports.handler = async (event) => {
  if (event.httpMethod === "OPTIONS") {
    return { statusCode: 204, headers };
  }
  try {
    const db = getSupabase();
    const params = event.queryStringParameters || {};
    const status = params.status || "approved";
    const limit = parseInt(params.limit) || 20;
    const offset = parseInt(params.offset) || 0;

    const { data, error } = await db
      .from("members")
      .select("first_name,last_name,company,job_title,industry,joined_date")
      .eq("status", status)
      .order("created_at", { ascending: false })
      .range(offset, offset + limit - 1);
    if (error) return err(500, error.message);
    return ok({ members: data || [], count: (data || []).length });
  } catch (e) {
    return err(500, e.message);
  }
};
