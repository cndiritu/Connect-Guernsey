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

    if (!body.first_name || !body.last_name || !body.email) {
      return err(400, "Missing required fields");
    }

    body.status = "unread";
    const { error } = await db.from("enquiries").insert(body);
    if (error) return err(500, error.message);

    return {
      statusCode: 201,
      headers,
      body: JSON.stringify({
        message: "Thank you! We'll be in touch soon.",
      }),
    };
  } catch (e) {
    return err(500, e.message);
  }
};
