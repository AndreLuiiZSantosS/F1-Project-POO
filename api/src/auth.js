const crypto = require("node:crypto");

const TOKEN_TTL_MS = 1000 * 60 * 60 * 24 * 7;

function nowIso() {
  return new Date().toISOString();
}

function hashPassword(password, salt = crypto.randomBytes(16).toString("hex")) {
  return new Promise((resolve, reject) => {
    crypto.scrypt(String(password), salt, 64, (error, derivedKey) => {
      if (error) {
        reject(error);
        return;
      }
      resolve(`scrypt:${salt}:${derivedKey.toString("hex")}`);
    });
  });
}

async function verifyPassword(password, storedHash) {
  const [algorithm, salt, expected] = String(storedHash || "").split(":");
  if (algorithm !== "scrypt" || !salt || !expected) {
    return false;
  }

  const computed = await hashPassword(password, salt);
  const computedHash = Buffer.from(computed.split(":")[2], "hex");
  const expectedHash = Buffer.from(expected, "hex");
  return computedHash.length === expectedHash.length && crypto.timingSafeEqual(computedHash, expectedHash);
}

function createToken(userId) {
  return {
    token: crypto.randomBytes(32).toString("hex"),
    userId,
    createdAt: nowIso(),
    expiresAt: new Date(Date.now() + TOKEN_TTL_MS).toISOString(),
  };
}

function normalizeEmail(email) {
  return String(email || "").trim().toLowerCase();
}

function sanitizeUser(user) {
  if (!user) return null;
  return {
    id: user.id,
    name: user.name,
    email: user.email,
    role: user.role || "user",
    createdAt: user.createdAt || "",
  };
}

function userFromRequest(request, database) {
  const authorization = request.headers.authorization || "";
  const match = authorization.match(/^Bearer\s+(.+)$/i);
  if (!match) return null;

  const tokenValue = match[1].trim();
  const token = database.authTokens.find((item) => item.token === tokenValue);
  if (!token || Date.parse(token.expiresAt) < Date.now()) {
    return null;
  }

  return database.users.find((user) => Number(user.id) === Number(token.userId)) || null;
}

module.exports = {
  createToken,
  hashPassword,
  normalizeEmail,
  nowIso,
  sanitizeUser,
  userFromRequest,
  verifyPassword,
};
