const { getSupabase, headers, ok, err } = require("./utils");

exports.handler = async (event) => {
  if (event.httpMethod === "OPTIONS") {
    return { statusCode: 204, headers };
  }
  if (event.httpMethod !== "POST") {
    return err(405, "Method not allowed");
  }
  try {
    const db = getSupabase();
    const body = JSON.parse(event.body);

    if (!body.email || !body.first_name || !body.last_name) {
      return err(400, "Missing required fields");
    }

    const { data: existing } = await db
      .from("members")
      .select("id")
      .eq("email", body.email);
    if (existing && existing.length > 0) {
      return err(400, "Email already registered");
    }

    body.status = "pending";
    const { data, error } = await db.from("members").insert(body).select();
    if (error) return err(500, error.message);

    return {
      statusCode: 201,
      headers,
      body: JSON.stringify({
        message: "Registration received. We'll be in touch soon.",
        id: data[0].id,
      }),
    };
  } catch (e) {
    return err(500, e.message);
  }
};
