const fs = require("node:fs/promises");
const path = require("node:path");

const { DATA_FILE } = require("./config");

function emptyDatabase() {
  return {
    meta: {
      version: 1,
      updatedAt: new Date().toISOString(),
      nextIds: {
        team: 1,
        driver: 1,
        event: 1,
        result: 1,
        user: 1,
        prediction: 1,
      },
    },
    teams: [],
    drivers: [],
    events: [],
    results: [],
    users: [],
    authTokens: [],
    predictions: [],
  };
}

function ensureShape(database) {
  const shaped = database && typeof database === "object" ? database : emptyDatabase();
  shaped.meta = shaped.meta && typeof shaped.meta === "object" ? shaped.meta : {};
  shaped.meta.version = shaped.meta.version || 1;
  shaped.meta.updatedAt = shaped.meta.updatedAt || new Date().toISOString();
  shaped.meta.nextIds = shaped.meta.nextIds || {};
  shaped.teams = Array.isArray(shaped.teams) ? shaped.teams : [];
  shaped.drivers = Array.isArray(shaped.drivers) ? shaped.drivers : [];
  shaped.events = Array.isArray(shaped.events) ? shaped.events : [];
  shaped.results = Array.isArray(shaped.results) ? shaped.results : [];
  shaped.users = Array.isArray(shaped.users) ? shaped.users : [];
  shaped.authTokens = Array.isArray(shaped.authTokens) ? shaped.authTokens : [];
  shaped.predictions = Array.isArray(shaped.predictions) ? shaped.predictions : [];

  shaped.meta.nextIds.team = Math.max(
    shaped.meta.nextIds.team || 1,
    ...shaped.teams.map((item) => Number(item.id) + 1),
    1
  );
  shaped.meta.nextIds.driver = Math.max(
    shaped.meta.nextIds.driver || 1,
    ...shaped.drivers.map((item) => Number(item.id) + 1),
    1
  );
  shaped.meta.nextIds.event = Math.max(
    shaped.meta.nextIds.event || 1,
    ...shaped.events.map((item) => Number(item.id) + 1),
    1
  );
  shaped.meta.nextIds.result = Math.max(
    shaped.meta.nextIds.result || 1,
    ...shaped.results.map((item) => Number(item.id) + 1),
    1
  );
  shaped.meta.nextIds.user = Math.max(
    shaped.meta.nextIds.user || 1,
    ...shaped.users.map((item) => Number(item.id) + 1),
    1
  );
  shaped.meta.nextIds.prediction = Math.max(
    shaped.meta.nextIds.prediction || 1,
    ...shaped.predictions.map((item) => Number(item.id) + 1),
    1
  );

  return shaped;
}

async function readDatabase() {
  try {
    const raw = await fs.readFile(DATA_FILE, "utf8");
    return ensureShape(JSON.parse(raw));
  } catch (error) {
    if (error.code !== "ENOENT") {
      throw error;
    }

    const database = emptyDatabase();
    await writeDatabase(database);
    return database;
  }
}

async function writeDatabase(database) {
  const shaped = ensureShape(database);
  shaped.meta.updatedAt = new Date().toISOString();
  await fs.mkdir(path.dirname(DATA_FILE), { recursive: true });
  const tempFile = `${DATA_FILE}.tmp`;
  await fs.writeFile(tempFile, `${JSON.stringify(shaped, null, 2)}\n`, "utf8");
  await fs.rename(tempFile, DATA_FILE);
  return shaped;
}

function nextId(database, collectionName) {
  const current = database.meta.nextIds[collectionName] || 1;
  database.meta.nextIds[collectionName] = current + 1;
  return current;
}

async function mutateDatabase(mutator) {
  const database = await readDatabase();
  const result = await mutator(database);
  await writeDatabase(database);
  return result;
}

module.exports = {
  readDatabase,
  writeDatabase,
  mutateDatabase,
  nextId,
};
