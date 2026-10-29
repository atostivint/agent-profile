/**
 * Optional content negotiation for a custom domain.
 *
 * GitHub Pages always serves index.html at "/", whatever the Accept header says.
 * This Worker makes the bare URL answer in Markdown when the caller asks for it,
 * which is what lauren.md does. It is NOT needed for the profile to work: the
 * page links /index.md, /llms.txt and /AGENTS.md, and those are already served
 * with content-type text/markdown by GitHub Pages.
 *
 * Deploy only after the custom domain resolves:
 *   route: profile.alexandre.tostivint.bzh/*  -> this Worker
 * Keep the origin as GitHub Pages so the HTML keeps working for humans.
 */

const MARKDOWN = "text/markdown; charset=utf-8";

export default {
  async fetch(request) {
    const url = new URL(request.url);
    const accept = (request.headers.get("accept") || "").toLowerCase();
    const asksMarkdown = accept.includes("text/markdown");
    const isHumanRoot = url.pathname === "/" || url.pathname === "/index.html";

    if (asksMarkdown && isHumanRoot) {
      const origin = new URL("/index.md", url);
      const md = await fetch(origin.toString(), { cf: { cacheTtl: 300 } });
      if (md.ok) {
        return new Response(await md.text(), {
          headers: {
            "content-type": MARKDOWN,
            vary: "Accept",
            "cache-control": "public, max-age=300",
            "x-agent-view": "index.md",
          },
        });
      }
    }

    const response = await fetch(request);
    const headers = new Headers(response.headers);
    headers.set("vary", "Accept");
    headers.append(
      "link",
      `<${new URL("/index.md", url)}>; rel="alternate"; type="text/markdown"`
    );
    return new Response(response.body, {
      status: response.status,
      statusText: response.statusText,
      headers,
    });
  },
};
