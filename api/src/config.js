const path = require("node:path");

const ROOT_DIR = path.resolve(__dirname, "..", "..");

function requiredAdminCredentials (environment = process.env) {
  const email = String(environment.ADMIN_EMAIL || "").trim();
  const password = environment.ADMIN_PASSWORD;

  if (!email || typeof password !== "string" || !password.trim()) {
    throw new Error("ADMIN_EMAIL and ADMIN_PASSWORD must be set before starting the API");
  }

  return { email, password: password.trim() };
}

module.exports = {
  ROOT_DIR,
  PORT: Number.parseInt(process.env.PORT || "8000", 10),
  DATA_FILE: process.env.DATA_FILE || path.join(ROOT_DIR, "api", "data", "database.json"),
  requiredAdminCredentials,
};
