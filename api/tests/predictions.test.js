const assert = require("node:assert/strict");
const test = require("node:test");

const {
  buildPredictionLeaderboard,
  scorePrediction,
} = require("../src/server");

const database = {
  teams: [{ id: 1, name: "McLaren", color: "#FF8000" }],
  drivers: [
    { id: 1, name: "Lando Norris", code: "NOR", number: 1, teamId: 1 },
    { id: 2, name: "Oscar Piastri", code: "PIA", number: 81, teamId: 1 },
  ],
  events: [
    { id: 1, round: 1, name: "Teste GP", hasSprint: false, practiceSessionsCount: 3, qualifyingSessionsCount: 3 },
  ],
  results: [
    { id: 1, eventId: 1, sessionType: "RACE", driverId: 1, position: 1, status: "CLASSIFIED", points: 25 },
    { id: 2, eventId: 1, sessionType: "RACE", driverId: 2, position: 2, status: "CLASSIFIED", points: 18 },
  ],
  users: [
    { id: 1, name: "Admin F1", email: "admin@f1.local", role: "admin" },
    { id: 2, name: "Player", email: "player@f1.local", role: "user" },
  ],
  predictions: [
    {
      id: 1,
      userId: 2,
      eventId: 1,
      sessionType: "RACE",
      picks: [
        { driverId: 1, position: 1 },
        { driverId: 2, position: 1 },
      ],
      createdAt: "2026-08-23T00:00:00.000Z",
      updatedAt: "2026-08-23T00:00:00.000Z",
    },
  ],
};

test("previsao pontua apenas piloto na posicao exata", () => {
  const score = scorePrediction(database.predictions[0], database);

  assert.deepEqual(score, {
    points: 25,
    correctPicks: 1,
    evaluated: true,
    possiblePicks: 2,
  });
});

test("ranking soma pontuacao das previsoes avaliadas", () => {
  const [row] = buildPredictionLeaderboard(database);

  assert.equal(row.user.name, "Player");
  assert.equal(row.points, 25);
  assert.equal(row.correctPicks, 1);
  assert.equal(row.evaluatedCount, 1);
});
