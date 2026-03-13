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

    if (!body.event_id || !body.email || !body.first_name) {
      return err(400, "Missing required fields");
    }

    const { data: eventData } = await db
      .from("events")
      .select("*")
      .eq("id", body.event_id)
      .eq("is_published", true);
    if (!eventData || !eventData.length) {
      return err(404, "Event not found");
    }

    const { data: existing } = await db
      .from("rsvps")
      .select("id")
      .eq("event_id", body.event_id)
      .eq("email", body.email);
    if (existing && existing.length > 0) {
      return err(400, "Already RSVP'd for this event");
    }

    const { error } = await db.from("rsvps").insert(body);
    if (error) return err(500, error.message);

    return {
      statusCode: 201,
      headers,
      body: JSON.stringify({
        message: "RSVP confirmed! We look forward to seeing you.",
      }),
    };
  } catch (e) {
    return err(500, e.message);
  }
};
