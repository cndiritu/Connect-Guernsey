const { getSupabase, headers, ok, err } = require("./utils");

exports.handler = async (event) => {
  if (event.httpMethod === "OPTIONS") {
    return { statusCode: 204, headers };
  }
  try {
    const db = getSupabase();
    const { data: albums, error } = await db
      .from("gallery_albums")
      .select("*")
      .eq("is_published", true)
      .order("created_at", { ascending: false });
    if (error) return err(500, error.message);

    for (const album of albums || []) {
      const { data: photos } = await db
        .from("gallery_photos")
        .select("*")
        .eq("album_id", album.id)
        .order("display_order");
      album.photos = photos || [];
    }

    return ok({ albums: albums || [] });
  } catch (e) {
    return err(500, e.message);
  }
};
