const { getSupabase, headers, ok, err } = require("./utils");

exports.handler = async (event) => {
  if (event.httpMethod === "OPTIONS") {
    return { statusCode: 204, headers };
  }
  try {
    const db = getSupabase();
    const params = event.queryStringParameters || {};
    const limit = parseInt(params.limit) || 12;
    const offset = parseInt(params.offset) || 0;

    let query = db
      .from("blog_posts")
      .select("id,title,slug,excerpt,category,image_url,published_at,author")
      .eq("is_published", true)
      .order("published_at", { ascending: false })
      .range(offset, offset + limit - 1);

    if (params.category) {
      query = query.eq("category", params.category);
    }

    const { data, error } = await query;
    if (error) return err(500, error.message);
    return ok({ posts: data || [] });
  } catch (e) {
    return err(500, e.message);
  }
};
