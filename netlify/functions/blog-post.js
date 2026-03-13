const { getSupabase, headers, ok, err } = require("./utils");

exports.handler = async (event) => {
  if (event.httpMethod === "OPTIONS") {
    return { statusCode: 204, headers };
  }
  try {
    // Slug comes from path: /api/blog/public/:slug → redirected with ?slug=:slug
    const slug = (event.queryStringParameters || {}).slug ||
                 (event.path || "").split("/").pop();
    if (!slug) return err(400, "Missing slug parameter");

    const db = getSupabase();
    const { data, error } = await db
      .from("blog_posts")
      .select("*")
      .eq("slug", slug)
      .eq("is_published", true);
    if (error) return err(500, error.message);
    if (!data || !data.length) return err(404, "Post not found");
    return ok(data[0]);
  } catch (e) {
    return err(500, e.message);
  }
};
