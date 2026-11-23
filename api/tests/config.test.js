const assert = require("node:assert/strict");
const test = require("node:test");

const { requiredAdminCredentials } = require("../src/config");

test("admin credentials must be provided explicitly", () => {
  assert.throws(
    () => requiredAdminCredentials({}),
    /ADMIN_EMAIL and ADMIN_PASSWORD must be set/,
  );
});

test("admin email is normalized while the configured password is preserved", () => {
  assert.deepEqual(
    requiredAdminCredentials({
      ADMIN_EMAIL: " admin@example.test ",
      ADMIN_PASSWORD: "a secure test password",
    }),
    {
      email: "admin@example.test",
      password: "a secure test password",
    },
  );
});
