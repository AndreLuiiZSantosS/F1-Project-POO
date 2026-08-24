const fs = require("node:fs");
const http = require("node:http");
const path = require("node:path");

const PORT = Number.parseInt(process.env.FRONTEND_PORT || "5173", 10);
const FRONTEND_DIR = __dirname;
const ROOT_DIR = path.resolve(__dirname, "..");

const MIME_TYPES = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".svg": "image/svg+xml",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".webp": "image/webp",
};

function resolveRequestPath(urlPath) {
  if (urlPath === "/shared/domain.js") {
    return path.join(ROOT_DIR, "shared", "domain.js");
  }

  const normalized = urlPath === "/" ? "/index.html" : decodeURIComponent(urlPath);
  const target = path.normalize(path.join(FRONTEND_DIR, normalized));

  if (!target.startsWith(FRONTEND_DIR)) {
    return path.join(FRONTEND_DIR, "index.html");
  }

  return target;
}

function sendFile(response, filePath) {
  fs.readFile(filePath, (error, data) => {
    if (error) {
      fs.readFile(path.join(FRONTEND_DIR, "index.html"), (fallbackError, fallbackData) => {
        if (fallbackError) {
          response.writeHead(404, { "Content-Type": "text/plain; charset=utf-8" });
          response.end("Arquivo nao encontrado");
          return;
        }

        response.writeHead(200, { "Content-Type": MIME_TYPES[".html"] });
        response.end(fallbackData);
      });
      return;
    }

    const extension = path.extname(filePath).toLowerCase();
    response.writeHead(200, { "Content-Type": MIME_TYPES[extension] || "application/octet-stream" });
    response.end(data);
  });
}

const server = http.createServer((request, response) => {
  const url = new URL(request.url, `http://${request.headers.host || "localhost"}`);
  sendFile(response, resolveRequestPath(url.pathname));
});

server.listen(PORT, () => {
  console.log(`F1 Results Frontend em http://127.0.0.1:${PORT}`);
});
