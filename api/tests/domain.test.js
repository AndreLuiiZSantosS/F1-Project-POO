const assert = require("node:assert/strict");
const test = require("node:test");

const {
  pointsForResult,
  sessionDefinitionsForEvent,
} = require("../../shared/domain");

test("gera sessoes de etapa normal com tres TLs, Q1-Q3 e corrida", () => {
  const sessions = sessionDefinitionsForEvent({
    practiceSessionsCount: 3,
    qualifyingSessionsCount: 3,
    hasSprint: false,
  });

  assert.deepEqual(
    sessions.map((session) => session.type),
    ["FP1", "FP2", "FP3", "Q1", "Q2", "Q3", "RACE"]
  );
});

test("gera sessoes sprint com treino reduzido, sprint quali e corrida sprint", () => {
  const sessions = sessionDefinitionsForEvent({
    practiceSessionsCount: 1,
    qualifyingSessionsCount: 3,
    hasSprint: true,
  });

  assert.deepEqual(
    sessions.map((session) => session.type),
    ["FP1", "Q1", "Q2", "Q3", "SPRINT_QUALIFYING", "SPRINT", "RACE"]
  );
});

test("calcula pontos de corrida e sprint sem pontuar treinos ou quali", () => {
  assert.equal(pointsForResult("RACE", 1, "CLASSIFIED"), 25);
  assert.equal(pointsForResult("RACE", 10, "CLASSIFIED"), 1);
  assert.equal(pointsForResult("SPRINT", 1, "CLASSIFIED"), 8);
  assert.equal(pointsForResult("SPRINT", 8, "CLASSIFIED"), 1);
  assert.equal(pointsForResult("Q3", 1, "CLASSIFIED"), 0);
  assert.equal(pointsForResult("RACE", 1, "DNF"), 0);
});
