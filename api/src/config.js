const path = require("node:path");

const ROOT_DIR = path.resolve(__dirname, "..", "..");

module.exports = {
  ROOT_DIR,
  PORT: Number.parseInt(process.env.PORT || "8000", 10),
  ADMIN_KEY: process.env.ADMIN_KEY || "admin-f1",
  DEFAULT_ADMIN_EMAIL: process.env.ADMIN_EMAIL || "admin@f1.local",
  DEFAULT_ADMIN_PASSWORD: process.env.ADMIN_PASSWORD || "admin-f1-2026",
  DATA_FILE: process.env.DATA_FILE || path.join(ROOT_DIR, "api", "data", "database.json"),
};
