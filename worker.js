addEventListener("fetch", (event) => {
  event.respondWith(
    handleRequest(event.request).catch(
      (err) => new Response(err.stack, { status: 500 })
    )
  );
});

/**
 * Many more examples available at:
 *   https://developers.cloudflare.com/workers/examples
 * @param {Request} request
 * @returns {Promise<Response>}
 */
async function handleRequest(request) {
  const d = await fetch("https://api.github.com/repos/galenguyer/plostcard/releases/latest", {
      headers: {
            "User-Agent": "plostcard.galenguyer.workers.dev/worker <galen@galenguyer.com>"
      }
  });
  const j = await d.json();
  const data = await fetch(j.assets[0].browser_download_url);
  const response = new Response(data.body, data);
  response.headers.set("content-type", "application/pdf")
  response.headers.set("content-disposition", "inline; filename=plostcard.pdf");
  return response;
}
