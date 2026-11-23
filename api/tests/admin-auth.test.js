const assert = require("node:assert/strict");
const fs = require("node:fs");
const http = require("node:http");
const os = require("node:os");
const path = require("node:path");
const test = require("node:test");

const tempDirectory = fs.mkdtempSync(path.join(os.tmpdir(), "f1-api-auth-"));
process.env.DATA_FILE = path.join(tempDirectory, "database.json");
process.env.ADMIN_EMAIL = "admin@example.test";
process.env.ADMIN_PASSWORD = "test-only-password";

const { requestHandler } = require("../src/server");

test("only the explicitly configured admin credentials can create an admin session", async () => {
  const server = http.createServer(requestHandler);
  await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
  const address = server.address();
  const endpoint = `http://127.0.0.1:${address.port}/api/auth/login`;

  async function login (email, password) {
    const response = await fetch(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });
    return { status: response.status, body: await response.json() };
  }

  try {
    assert.equal((await login("former-admin@example.test", "not-configured-password")).status, 401);
    assert.equal((await login("admin@example.test", "not-configured-password")).status, 401);

    const configuredLogin = await login("admin@example.test", "test-only-password");
    assert.equal(configuredLogin.status, 200);
    assert.equal(configuredLogin.body.user.role, "admin");
  } finally {
    await new Promise((resolve, reject) => {
      server.close((error) => (error ? reject(error) : resolve()));
    });
    fs.rmSync(tempDirectory, { recursive: true, force: true });
  }
});
