const http = require("node:http");
const { URL } = require("node:url");

const {
  RESULT_STATUSES,
  pointsForResult,
  sessionDefinitionsForEvent,
} = require("../../shared/domain");
const {
  DATA_FILE,
  DEFAULT_ADMIN_EMAIL,
  DEFAULT_ADMIN_PASSWORD,
  PORT,
} = require("./config");
const {
  createToken,
  hashPassword,
  normalizeEmail,
  nowIso,
  sanitizeUser,
  userFromRequest,
  verifyPassword,
} = require("./auth");
const { mutateDatabase, nextId, readDatabase } = require("./store");

const STATUS_VALUES = new Set(RESULT_STATUSES.map((status) => status.value));

class HttpError extends Error {
  constructor(status, message) {
    super(message);
    this.status = status;
  }
}

function corsHeaders() {
  return {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type,Authorization",
    "Access-Control-Max-Age": "86400",
  };
}

function sendJson(response, status, payload) {
  response.writeHead(status, {
    "Content-Type": "application/json; charset=utf-8",
    ...corsHeaders(),
  });
  response.end(JSON.stringify(payload, null, 2));
}

function readJsonBody(request) {
  return new Promise((resolve, reject) => {
    let body = "";
    request.on("data", (chunk) => {
      body += chunk;
      if (body.length > 1_000_000) {
        request.destroy();
        reject(new HttpError(413, "Payload muito grande"));
      }
    });
    request.on("end", () => {
      if (!body.trim()) {
        resolve({});
        return;
      }

      try {
        resolve(JSON.parse(body));
      } catch {
        reject(new HttpError(400, "JSON invalido"));
      }
    });
    request.on("error", reject);
  });
}

function cleanString(value, fallback = "") {
  if (value === null || value === undefined) {
    return fallback;
  }

  return String(value).trim();
}

function cleanOptionalUrl(value) {
  const url = cleanString(value);
  if (!url) {
    return "";
  }

  try {
    const parsed = new URL(url);
    return ["http:", "https:", "data:"].includes(parsed.protocol) ? url : "";
  } catch {
    return "";
  }
}

function cleanColor(value, fallback = "#e10600") {
  const color = cleanString(value, fallback);
  return /^#[0-9a-f]{6}$/i.test(color) ? color.toUpperCase() : fallback;
}

function toPositiveInt(value, fallback = null) {
  const parsed = Number.parseInt(value, 10);
  return Number.isFinite(parsed) && parsed > 0 ? parsed : fallback;
}

function toBool(value) {
  return value === true || value === "true" || value === "on" || value === 1 || value === "1";
}

function findById(items, id) {
  const numericId = Number.parseInt(id, 10);
  return items.find((item) => Number(item.id) === numericId) || null;
}

function bearerToken(request) {
  const authorization = request.headers.authorization || "";
  const match = authorization.match(/^Bearer\s+(.+)$/i);
  return match ? match[1].trim() : "";
}

function requireUser(request, database) {
  const user = userFromRequest(request, database);
  if (!user) {
    throw new HttpError(401, "Login necessario");
  }
  return user;
}

function requireAdminUser(request, database) {
  const user = requireUser(request, database);
  if (user.role !== "admin") {
    throw new HttpError(403, "Acesso restrito ao admin");
  }
  return user;
}

function publicUser(user) {
  return {
    id: user.id,
    name: user.name,
    role: user.role || "user",
  };
}

function cleanExpiredTokens(database) {
  const now = Date.now();
  database.authTokens = database.authTokens.filter((token) => Date.parse(token.expiresAt) >= now);
}

async function ensureDefaultAdmin(database) {
  const email = normalizeEmail(DEFAULT_ADMIN_EMAIL);
  let user = database.users.find((item) => item.email === email);

  if (!user) {
    user = {
      id: nextId(database, "user"),
      name: "Admin F1",
      email,
      role: "admin",
      passwordHash: await hashPassword(DEFAULT_ADMIN_PASSWORD),
      createdAt: nowIso(),
    };
    database.users.push(user);
    return user;
  }

  user.role = "admin";
  if (!user.passwordHash) {
    user.passwordHash = await hashPassword(DEFAULT_ADMIN_PASSWORD);
  }
  return user;
}

function sortByPosition(left, right) {
  const leftPosition = Number(left.position || 999);
  const rightPosition = Number(right.position || 999);
  if (leftPosition !== rightPosition) {
    return leftPosition - rightPosition;
  }

  return String(left.time || "").localeCompare(String(right.time || ""));
}

function serializeTeam(team) {
  return {
    id: team.id,
    name: team.name,
    shortName: team.shortName || team.name,
    fullName: team.fullName || team.name,
    base: team.base || "",
    country: team.country || "",
    powerUnit: team.powerUnit || "",
    chief: team.chief || "",
    color: team.color || "#e10600",
    emblemUrl: team.emblemUrl || "",
  };
}

function serializeDriver(driver, teams) {
  const team = findById(teams, driver.teamId);
  return {
    id: driver.id,
    name: driver.name,
    code: driver.code || "",
    number: driver.number,
    country: driver.country || "",
    active: driver.active !== false,
    photoUrl: driver.photoUrl || "",
    teamId: driver.teamId,
    team: team ? serializeTeam(team) : null,
  };
}

function serializeResult(result, database) {
  const driver = findById(database.drivers, result.driverId);
  return {
    id: result.id,
    eventId: result.eventId,
    sessionType: result.sessionType,
    driverId: result.driverId,
    driver: driver ? serializeDriver(driver, database.teams) : null,
    position: result.position,
    time: result.time || "",
    gap: result.gap || "",
    laps: result.laps || "",
    status: result.status || "CLASSIFIED",
    points: result.points || 0,
    notes: result.notes || "",
  };
}

function serializeEventBrief(event) {
  return {
    id: event.id,
    round: event.round,
    name: event.name,
    date: event.date || "",
    hasSprint: Boolean(event.hasSprint),
  };
}

function serializeEvent(event, database) {
  const definitions = sessionDefinitionsForEvent(event);
  const sessions = definitions.map((definition) => {
    const results = database.results
      .filter((result) => Number(result.eventId) === Number(event.id) && result.sessionType === definition.type)
      .sort(sortByPosition)
      .map((result) => serializeResult(result, database));

    return {
      ...definition,
      results,
    };
  });

  return {
    id: event.id,
    round: event.round,
    name: event.name,
    circuit: event.circuit || "",
    city: event.city || "",
    country: event.country || "",
    date: event.date || "",
    hasSprint: Boolean(event.hasSprint),
    practiceSessionsCount: event.practiceSessionsCount || 3,
    qualifyingSessionsCount: event.qualifyingSessionsCount || 3,
    notes: event.notes || "",
    sessions,
  };
}

function serializeDatabase(database) {
  return {
    meta: {
      version: database.meta.version,
      updatedAt: database.meta.updatedAt,
      source: database.meta.source || "",
      sourceUpdatedAt: database.meta.sourceUpdatedAt || "",
    },
    teams: database.teams.map(serializeTeam),
    drivers: database.drivers.map((driver) => serializeDriver(driver, database.teams)),
    events: database.events
      .slice()
      .sort((left, right) => Number(left.round) - Number(right.round))
      .map((event) => serializeEvent(event, database)),
  };
}

function buildStandings(database) {
  const driverRows = database.drivers.map((driver) => ({
    driver: serializeDriver(driver, database.teams),
    points: 0,
    wins: 0,
    podiums: 0,
    sprintPoints: 0,
    racePoints: 0,
  }));

  const driverRowsById = new Map(driverRows.map((row) => [Number(row.driver.id), row]));

  for (const result of database.results) {
    const row = driverRowsById.get(Number(result.driverId));
    if (!row || !result.points) {
      continue;
    }

    row.points += result.points;
    if (result.sessionType === "SPRINT") {
      row.sprintPoints += result.points;
    }
    if (result.sessionType === "RACE") {
      row.racePoints += result.points;
      if (Number(result.position) === 1) {
        row.wins += 1;
      }
      if (Number(result.position) >= 1 && Number(result.position) <= 3) {
        row.podiums += 1;
      }
    }
  }

  driverRows.sort((left, right) => {
    if (right.points !== left.points) return right.points - left.points;
    if (right.wins !== left.wins) return right.wins - left.wins;
    return left.driver.name.localeCompare(right.driver.name);
  });

  const teamRowsById = new Map();
  for (const row of driverRows) {
    if (!row.driver.team) {
      continue;
    }

    const teamId = Number(row.driver.team.id);
    if (!teamRowsById.has(teamId)) {
      teamRowsById.set(teamId, {
        team: row.driver.team,
        points: 0,
        wins: 0,
        podiums: 0,
      });
    }

    const teamRow = teamRowsById.get(teamId);
    teamRow.points += row.points;
    teamRow.wins += row.wins;
    teamRow.podiums += row.podiums;
  }

  const teamRows = Array.from(teamRowsById.values()).sort((left, right) => {
    if (right.points !== left.points) return right.points - left.points;
    if (right.wins !== left.wins) return right.wins - left.wins;
    return left.team.name.localeCompare(right.team.name);
  });

  return {
    drivers: driverRows,
    teams: teamRows,
  };
}

function scorePrediction(prediction, database) {
  const actualResults = database.results.filter(
    (result) =>
      Number(result.eventId) === Number(prediction.eventId) &&
      result.sessionType === prediction.sessionType
  );

  if (!actualResults.length) {
    return { points: 0, correctPicks: 0, evaluated: false, possiblePicks: prediction.picks.length };
  }

  let points = 0;
  let correctPicks = 0;
  for (const pick of prediction.picks) {
    const actual = actualResults.find((result) => Number(result.driverId) === Number(pick.driverId));
    if (actual && Number(actual.position) === Number(pick.position)) {
      points += Number(actual.points || 0);
      correctPicks += 1;
    }
  }

  return { points, correctPicks, evaluated: true, possiblePicks: prediction.picks.length };
}

function serializePrediction(prediction, database) {
  const event = findById(database.events, prediction.eventId);
  const session = event
    ? sessionDefinitionsForEvent(event).find((definition) => definition.type === prediction.sessionType)
    : null;

  return {
    id: prediction.id,
    userId: prediction.userId,
    event: event ? serializeEventBrief(event) : null,
    eventId: prediction.eventId,
    sessionType: prediction.sessionType,
    sessionLabel: session?.label || prediction.sessionType,
    picks: prediction.picks.map((pick) => {
      const driver = findById(database.drivers, pick.driverId);
      return {
        position: pick.position,
        driverId: pick.driverId,
        driver: driver ? serializeDriver(driver, database.teams) : null,
      };
    }),
    score: scorePrediction(prediction, database),
    createdAt: prediction.createdAt,
    updatedAt: prediction.updatedAt,
  };
}

function buildPredictionLeaderboard(database) {
  const rowsByUserId = new Map();

  for (const prediction of database.predictions) {
    const user = findById(database.users, prediction.userId);
    if (!user) {
      continue;
    }

    const score = scorePrediction(prediction, database);
    const userId = Number(user.id);
    if (!rowsByUserId.has(userId)) {
      rowsByUserId.set(userId, {
        user: publicUser(user),
        points: 0,
        correctPicks: 0,
        predictionsCount: 0,
        evaluatedCount: 0,
        lastPredictionAt: "",
      });
    }

    const row = rowsByUserId.get(userId);
    row.points += score.points;
    row.correctPicks += score.correctPicks;
    row.predictionsCount += 1;
    if (score.evaluated) {
      row.evaluatedCount += 1;
    }
    row.lastPredictionAt = [row.lastPredictionAt, prediction.updatedAt || prediction.createdAt || ""]
      .filter(Boolean)
      .sort()
      .at(-1) || "";
  }

  return Array.from(rowsByUserId.values()).sort((left, right) => {
    if (right.points !== left.points) return right.points - left.points;
    if (right.correctPicks !== left.correctPicks) return right.correctPicks - left.correctPicks;
    return left.user.name.localeCompare(right.user.name);
  });
}

function normalizeTeamPayload(payload, existing = {}) {
  const name = cleanString(payload.name, existing.name);
  if (!name) {
    throw new HttpError(400, "Nome da equipe e obrigatorio");
  }

  return {
    ...existing,
    name,
    shortName: cleanString(payload.shortName, existing.shortName || name),
    fullName: cleanString(payload.fullName, existing.fullName || name),
    base: cleanString(payload.base, existing.base),
    country: cleanString(payload.country, existing.country),
    powerUnit: cleanString(payload.powerUnit, existing.powerUnit),
    chief: cleanString(payload.chief, existing.chief),
    color: cleanColor(payload.color, existing.color || "#e10600"),
    emblemUrl: cleanOptionalUrl(payload.emblemUrl ?? existing.emblemUrl),
  };
}

function normalizeDriverPayload(payload, database, existing = {}) {
  const name = cleanString(payload.name, existing.name);
  const number = toPositiveInt(payload.number, existing.number);
  const teamId = toPositiveInt(payload.teamId, existing.teamId);

  if (!name) {
    throw new HttpError(400, "Nome do piloto e obrigatorio");
  }
  if (!number) {
    throw new HttpError(400, "Numero do piloto e obrigatorio");
  }
  if (!findById(database.teams, teamId)) {
    throw new HttpError(400, "Equipe nao encontrada");
  }

  return {
    ...existing,
    name,
    number,
    teamId,
    code: cleanString(payload.code, existing.code).toUpperCase().slice(0, 4),
    country: cleanString(payload.country, existing.country),
    active: payload.active === undefined ? existing.active !== false : toBool(payload.active),
    photoUrl: cleanOptionalUrl(payload.photoUrl ?? existing.photoUrl),
  };
}

function normalizeEventPayload(payload, existing = {}) {
  const round = toPositiveInt(payload.round, existing.round);
  const name = cleanString(payload.name, existing.name);

  if (!round) {
    throw new HttpError(400, "Numero da etapa e obrigatorio");
  }
  if (!name) {
    throw new HttpError(400, "Nome da etapa e obrigatorio");
  }

  return {
    ...existing,
    round,
    name,
    circuit: cleanString(payload.circuit, existing.circuit),
    city: cleanString(payload.city, existing.city),
    country: cleanString(payload.country, existing.country),
    date: cleanString(payload.date, existing.date),
    hasSprint: payload.hasSprint === undefined ? Boolean(existing.hasSprint) : toBool(payload.hasSprint),
    practiceSessionsCount: Math.min(Math.max(toPositiveInt(payload.practiceSessionsCount, existing.practiceSessionsCount || 3), 1), 3),
    qualifyingSessionsCount: Math.min(Math.max(toPositiveInt(payload.qualifyingSessionsCount, existing.qualifyingSessionsCount || 3), 1), 3),
    notes: cleanString(payload.notes, existing.notes),
  };
}

function normalizeResultPayload(payload, database, existing = {}) {
  const eventId = toPositiveInt(payload.eventId, existing.eventId);
  const driverId = toPositiveInt(payload.driverId, existing.driverId);
  const event = findById(database.events, eventId);
  const driver = findById(database.drivers, driverId);
  const sessionType = cleanString(payload.sessionType, existing.sessionType).toUpperCase();
  const status = cleanString(payload.status, existing.status || "CLASSIFIED").toUpperCase();
  const position = payload.position === "" || payload.position === null
    ? null
    : toPositiveInt(payload.position, existing.position);

  if (!event) {
    throw new HttpError(400, "Etapa nao encontrada");
  }
  if (!driver) {
    throw new HttpError(400, "Piloto nao encontrado");
  }
  if (!STATUS_VALUES.has(status)) {
    throw new HttpError(400, "Status invalido");
  }

  const allowedSessionTypes = new Set(sessionDefinitionsForEvent(event).map((session) => session.type));
  if (!allowedSessionTypes.has(sessionType)) {
    throw new HttpError(400, "Sessao nao existe para esta etapa");
  }

  return {
    ...existing,
    eventId,
    driverId,
    sessionType,
    position,
    time: cleanString(payload.time, existing.time),
    gap: cleanString(payload.gap, existing.gap),
    laps: cleanString(payload.laps, existing.laps),
    status,
    points: pointsForResult(sessionType, position, status),
    notes: cleanString(payload.notes, existing.notes),
  };
}

function normalizePredictionPayload(payload, database) {
  const eventId = toPositiveInt(payload.eventId);
  const event = findById(database.events, eventId);
  const sessionType = cleanString(payload.sessionType, "RACE").toUpperCase();

  if (!event) {
    throw new HttpError(400, "Etapa nao encontrada");
  }

  const session = sessionDefinitionsForEvent(event).find((definition) => definition.type === sessionType);
  if (!session || !session.pointsSession) {
    throw new HttpError(400, "Previsoes so estao liberadas para corrida e sprint");
  }

  const actualResults = database.results.filter(
    (result) => Number(result.eventId) === Number(eventId) && result.sessionType === sessionType
  );
  if (actualResults.length) {
    throw new HttpError(409, "Previsoes bloqueadas para sessao ja finalizada");
  }

  const picks = Array.isArray(payload.picks) ? payload.picks : [];
  if (!picks.length) {
    throw new HttpError(400, "Informe ao menos uma previsao");
  }

  const seenDrivers = new Set();
  const seenPositions = new Set();
  const normalizedPicks = picks.map((pick) => {
    const driverId = toPositiveInt(pick.driverId);
    const position = toPositiveInt(pick.position);

    if (!findById(database.drivers, driverId)) {
      throw new HttpError(400, "Piloto da previsao nao encontrado");
    }
    if (!position) {
      throw new HttpError(400, "Posicao da previsao invalida");
    }
    if (seenDrivers.has(driverId)) {
      throw new HttpError(400, "Piloto repetido na previsao");
    }
    if (seenPositions.has(position)) {
      throw new HttpError(400, "Posicao repetida na previsao");
    }

    seenDrivers.add(driverId);
    seenPositions.add(position);
    return { driverId, position };
  });

  normalizedPicks.sort((left, right) => left.position - right.position);
  return { eventId, sessionType, picks: normalizedPicks };
}

function parseRoute(pathname) {
  const parts = pathname.split("/").filter(Boolean);
  if (parts[0] !== "api") {
    return null;
  }

  return {
    resource: parts[1] || "",
    id: parts[2] || "",
    action: parts[3] || "",
    parts,
  };
}

async function handleAuthGet(request, route, response) {
  if (route.id !== "me") {
    sendJson(response, 404, { error: "Endpoint nao encontrado" });
    return;
  }

  const database = await readDatabase();
  const user = userFromRequest(request, database);
  sendJson(response, 200, { user: sanitizeUser(user) });
}

async function handleAuthWrite(request, route, response) {
  const payload = await readJsonBody(request);

  if (request.method === "POST" && route.id === "register") {
    const result = await mutateDatabase(async (database) => {
      cleanExpiredTokens(database);
      const name = cleanString(payload.name);
      const email = normalizeEmail(payload.email);
      const password = cleanString(payload.password);

      if (!name) {
        throw new HttpError(400, "Nome e obrigatorio");
      }
      if (!email || !email.includes("@")) {
        throw new HttpError(400, "Email invalido");
      }
      if (password.length < 6) {
        throw new HttpError(400, "Senha precisa ter pelo menos 6 caracteres");
      }
      if (database.users.some((user) => user.email === email)) {
        throw new HttpError(409, "Email ja cadastrado");
      }

      const user = {
        id: nextId(database, "user"),
        name,
        email,
        role: "user",
        passwordHash: await hashPassword(password),
        createdAt: nowIso(),
      };
      const token = createToken(user.id);
      database.users.push(user);
      database.authTokens.push(token);
      return { user: sanitizeUser(user), token: token.token };
    });

    sendJson(response, 201, result);
    return;
  }

  if (request.method === "POST" && route.id === "login") {
    const result = await mutateDatabase(async (database) => {
      cleanExpiredTokens(database);
      const email = normalizeEmail(payload.email);
      const password = cleanString(payload.password);
      let user = database.users.find((item) => item.email === email);

      if (!user && email === normalizeEmail(DEFAULT_ADMIN_EMAIL)) {
        if (password !== DEFAULT_ADMIN_PASSWORD) {
          throw new HttpError(401, "Credenciais invalidas");
        }
        user = await ensureDefaultAdmin(database);
      }

      if (!user || !(await verifyPassword(password, user.passwordHash))) {
        throw new HttpError(401, "Credenciais invalidas");
      }

      const token = createToken(user.id);
      database.authTokens.push(token);
      return { user: sanitizeUser(user), token: token.token };
    });

    sendJson(response, 200, result);
    return;
  }

  if (request.method === "POST" && route.id === "logout") {
    const tokenValue = bearerToken(request);
    await mutateDatabase((database) => {
      database.authTokens = database.authTokens.filter((token) => token.token !== tokenValue);
      return null;
    });
    sendJson(response, 200, { ok: true });
    return;
  }

  sendJson(response, 404, { error: "Endpoint nao encontrado" });
}

async function handlePredictionGet(request, route, response) {
  const database = await readDatabase();

  if (route.id === "leaderboard") {
    sendJson(response, 200, { leaderboard: buildPredictionLeaderboard(database) });
    return;
  }

  if (route.id === "me") {
    const user = requireUser(request, database);
    const predictions = database.predictions
      .filter((prediction) => Number(prediction.userId) === Number(user.id))
      .sort((left, right) => String(right.updatedAt || right.createdAt).localeCompare(String(left.updatedAt || left.createdAt)))
      .map((prediction) => serializePrediction(prediction, database));
    sendJson(response, 200, { predictions });
    return;
  }

  sendJson(response, 404, { error: "Endpoint nao encontrado" });
}

async function handlePredictionWrite(request, route, response) {
  const payload = await readJsonBody(request);

  if (request.method === "POST" && route.resource === "predictions" && !route.id) {
    const databaseForAuth = await readDatabase();
    const user = requireUser(request, databaseForAuth);

    const prediction = await mutateDatabase((database) => {
      const normalized = normalizePredictionPayload(payload, database);
      const existing = database.predictions.find(
        (item) =>
          Number(item.userId) === Number(user.id) &&
          Number(item.eventId) === Number(normalized.eventId) &&
          item.sessionType === normalized.sessionType
      );

      if (existing) {
        Object.assign(existing, normalized, { updatedAt: nowIso() });
        return serializePrediction(existing, database);
      }

      const created = {
        id: nextId(database, "prediction"),
        userId: user.id,
        ...normalized,
        createdAt: nowIso(),
        updatedAt: nowIso(),
      };
      database.predictions.push(created);
      return serializePrediction(created, database);
    });

    sendJson(response, 201, { prediction });
    return;
  }

  if (request.method === "DELETE" && route.resource === "predictions" && route.id) {
    const databaseForAuth = await readDatabase();
    const user = requireUser(request, databaseForAuth);

    const deleted = await mutateDatabase((database) => {
      const index = database.predictions.findIndex((prediction) => Number(prediction.id) === Number(route.id));
      if (index < 0) {
        throw new HttpError(404, "Previsao nao encontrada");
      }

      const prediction = database.predictions[index];
      if (Number(prediction.userId) !== Number(user.id) && user.role !== "admin") {
        throw new HttpError(403, "Sem permissao para excluir esta previsao");
      }

      const [removed] = database.predictions.splice(index, 1);
      return serializePrediction(removed, database);
    });

    sendJson(response, 200, { deleted });
    return;
  }

  sendJson(response, 404, { error: "Endpoint nao encontrado" });
}

async function handlePublicGet(request, route, response) {
  if (route.resource === "auth") {
    await handleAuthGet(request, route, response);
    return;
  }

  if (route.resource === "predictions") {
    await handlePredictionGet(request, route, response);
    return;
  }

  const database = await readDatabase();

  if (route.resource === "health") {
    sendJson(response, 200, {
      ok: true,
      dataFile: DATA_FILE,
      updatedAt: database.meta.updatedAt,
    });
    return;
  }

  if (route.resource === "meta") {
    sendJson(response, 200, {
      statuses: RESULT_STATUSES,
      auth: {
        adminEmail: DEFAULT_ADMIN_EMAIL,
      },
    });
    return;
  }

  if (route.resource === "teams") {
    sendJson(response, 200, { teams: database.teams.map(serializeTeam) });
    return;
  }

  if (route.resource === "drivers") {
    sendJson(response, 200, { drivers: database.drivers.map((driver) => serializeDriver(driver, database.teams)) });
    return;
  }

  if (route.resource === "events") {
    const events = database.events
      .slice()
      .sort((left, right) => Number(left.round) - Number(right.round))
      .map((event) => serializeEvent(event, database));
    sendJson(response, 200, { events });
    return;
  }

  if (route.resource === "standings") {
    sendJson(response, 200, { standings: buildStandings(database) });
    return;
  }

  if (route.resource === "snapshot") {
    sendJson(response, 200, serializeDatabase(database));
    return;
  }

  sendJson(response, 404, { error: "Endpoint nao encontrado" });
}

async function handleAdminWrite(request, route, response) {
  const databaseForAuth = await readDatabase();
  requireAdminUser(request, databaseForAuth);
  const payload = await readJsonBody(request);

  if (request.method === "POST" && route.resource === "teams") {
    const team = await mutateDatabase((database) => {
      const normalized = normalizeTeamPayload(payload);
      const duplicated = database.teams.some(
        (item) => item.name.toLowerCase() === normalized.name.toLowerCase()
      );
      if (duplicated) {
        throw new HttpError(409, "Equipe ja cadastrada");
      }

      const created = { id: nextId(database, "team"), ...normalized };
      database.teams.push(created);
      return serializeTeam(created);
    });
    sendJson(response, 201, { team });
    return;
  }

  if (request.method === "PUT" && route.resource === "teams") {
    const team = await mutateDatabase((database) => {
      const existing = findById(database.teams, route.id);
      if (!existing) {
        throw new HttpError(404, "Equipe nao encontrada");
      }
      Object.assign(existing, normalizeTeamPayload(payload, existing));
      return serializeTeam(existing);
    });
    sendJson(response, 200, { team });
    return;
  }

  if (request.method === "POST" && route.resource === "drivers") {
    const driver = await mutateDatabase((database) => {
      const normalized = normalizeDriverPayload(payload, database);
      const duplicatedNumber = database.drivers.some((item) => Number(item.number) === Number(normalized.number));
      if (duplicatedNumber) {
        throw new HttpError(409, "Numero de piloto ja cadastrado");
      }

      const created = { id: nextId(database, "driver"), ...normalized };
      database.drivers.push(created);
      return serializeDriver(created, database.teams);
    });
    sendJson(response, 201, { driver });
    return;
  }

  if (request.method === "PUT" && route.resource === "drivers") {
    const driver = await mutateDatabase((database) => {
      const existing = findById(database.drivers, route.id);
      if (!existing) {
        throw new HttpError(404, "Piloto nao encontrado");
      }
      const normalized = normalizeDriverPayload(payload, database, existing);
      const duplicatedNumber = database.drivers.some(
        (item) => Number(item.id) !== Number(existing.id) && Number(item.number) === Number(normalized.number)
      );
      if (duplicatedNumber) {
        throw new HttpError(409, "Numero de piloto ja cadastrado");
      }
      Object.assign(existing, normalized);
      return serializeDriver(existing, database.teams);
    });
    sendJson(response, 200, { driver });
    return;
  }

  if (request.method === "POST" && route.resource === "events") {
    const event = await mutateDatabase((database) => {
      const normalized = normalizeEventPayload(payload);
      const duplicatedRound = database.events.some((item) => Number(item.round) === Number(normalized.round));
      if (duplicatedRound) {
        throw new HttpError(409, "Numero da etapa ja cadastrado");
      }

      const created = { id: nextId(database, "event"), ...normalized };
      database.events.push(created);
      return serializeEvent(created, database);
    });
    sendJson(response, 201, { event });
    return;
  }

  if (request.method === "PUT" && route.resource === "events") {
    const event = await mutateDatabase((database) => {
      const existing = findById(database.events, route.id);
      if (!existing) {
        throw new HttpError(404, "Etapa nao encontrada");
      }
      const normalized = normalizeEventPayload(payload, existing);
      const duplicatedRound = database.events.some(
        (item) => Number(item.id) !== Number(existing.id) && Number(item.round) === Number(normalized.round)
      );
      if (duplicatedRound) {
        throw new HttpError(409, "Numero da etapa ja cadastrado");
      }
      Object.assign(existing, normalized);
      return serializeEvent(existing, database);
    });
    sendJson(response, 200, { event });
    return;
  }

  if (request.method === "POST" && route.resource === "results") {
    const result = await mutateDatabase((database) => {
      const normalized = normalizeResultPayload(payload, database);
      const existing = database.results.find(
        (item) =>
          Number(item.eventId) === Number(normalized.eventId) &&
          item.sessionType === normalized.sessionType &&
          Number(item.driverId) === Number(normalized.driverId)
      );

      if (existing) {
        Object.assign(existing, normalized);
        return serializeResult(existing, database);
      }

      const created = { id: nextId(database, "result"), ...normalized };
      database.results.push(created);
      return serializeResult(created, database);
    });
    sendJson(response, 201, { result });
    return;
  }

  if (request.method === "DELETE" && route.resource === "results") {
    const deleted = await mutateDatabase((database) => {
      const index = database.results.findIndex((item) => Number(item.id) === Number(route.id));
      if (index < 0) {
        throw new HttpError(404, "Resultado nao encontrado");
      }

      const [removed] = database.results.splice(index, 1);
      return serializeResult(removed, database);
    });
    sendJson(response, 200, { deleted });
    return;
  }

  sendJson(response, 404, { error: "Endpoint nao encontrado" });
}

async function handleWrite(request, route, response) {
  if (route.resource === "auth") {
    await handleAuthWrite(request, route, response);
    return;
  }

  if (route.resource === "predictions") {
    await handlePredictionWrite(request, route, response);
    return;
  }

  await handleAdminWrite(request, route, response);
}

async function requestHandler(request, response) {
  const { pathname } = new URL(request.url, `http://${request.headers.host || "localhost"}`);
  const route = parseRoute(pathname);

  if (request.method === "OPTIONS") {
    response.writeHead(204, corsHeaders());
    response.end();
    return;
  }

  if (pathname === "/" || pathname === "") {
    sendJson(response, 200, {
      name: "F1 Results API",
      message: "API online. Abra o frontend em http://127.0.0.1:5173 ou use endpoints iniciando por /api.",
      health: "/api/health",
      snapshot: "/api/snapshot",
      standings: "/api/standings",
      auth: "/api/auth/login",
      predictions: "/api/predictions/me",
    });
    return;
  }

  if (!route) {
    sendJson(response, 404, { error: "Use endpoints iniciando por /api" });
    return;
  }

  try {
    if (request.method === "GET") {
      await handlePublicGet(request, route, response);
      return;
    }

    if (["POST", "PUT", "DELETE"].includes(request.method)) {
      await handleWrite(request, route, response);
      return;
    }

    sendJson(response, 405, { error: "Metodo nao permitido" });
  } catch (error) {
    sendJson(response, error.status || 400, { error: error.message || "Erro inesperado" });
  }
}

if (require.main === module) {
  const server = http.createServer(requestHandler);
  server.listen(PORT, () => {
    console.log(`F1 Results API em http://127.0.0.1:${PORT}`);
    console.log(`Banco: ${DATA_FILE}`);
  });
}

module.exports = {
  requestHandler,
  serializeEvent,
  buildPredictionLeaderboard,
  buildStandings,
  scorePrediction,
};
