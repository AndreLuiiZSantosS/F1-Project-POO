(function attachDomain(root) {
  const RACE_POINTS = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1];
  const SPRINT_POINTS = [8, 7, 6, 5, 4, 3, 2, 1];

  const RESULT_STATUSES = [
    { value: "CLASSIFIED", label: "Classificado" },
    { value: "DNF", label: "DNF" },
    { value: "DNS", label: "DNS" },
    { value: "DSQ", label: "Desclassificado" },
    { value: "RETIRED", label: "Retirado" },
  ];

  function toPositiveInt(value, fallback) {
    const parsed = Number.parseInt(value, 10);
    return Number.isFinite(parsed) && parsed > 0 ? parsed : fallback;
  }

  function clampCount(value, fallback, max) {
    return Math.min(Math.max(toPositiveInt(value, fallback), 1), max);
  }

  function sessionDefinitionsForEvent(event) {
    const practiceCount = clampCount(event.practiceSessionsCount, 3, 3);
    const qualifyingCount = clampCount(event.qualifyingSessionsCount, 3, 3);
    const sessions = [];

    for (let index = 1; index <= practiceCount; index += 1) {
      sessions.push({
        type: `FP${index}`,
        label: `Treino Livre ${index}`,
        shortLabel: `TL${index}`,
        group: "Treinos",
        pointsSession: false,
      });
    }

    for (let index = 1; index <= qualifyingCount; index += 1) {
      sessions.push({
        type: `Q${index}`,
        label: `Qualificacao Q${index}`,
        shortLabel: `Q${index}`,
        group: "Qualificacao",
        pointsSession: false,
      });
    }

    if (event.hasSprint) {
      sessions.push({
        type: "SPRINT_QUALIFYING",
        label: "Qualificacao Sprint",
        shortLabel: "SQ",
        group: "Sprint",
        pointsSession: false,
      });
      sessions.push({
        type: "SPRINT",
        label: "Corrida Sprint",
        shortLabel: "SPR",
        group: "Sprint",
        pointsSession: true,
      });
    }

    sessions.push({
      type: "RACE",
      label: "Corrida",
      shortLabel: "GP",
      group: "Corrida",
      pointsSession: true,
    });

    return sessions;
  }

  function pointsForResult(sessionType, position, status) {
    if (status && status !== "CLASSIFIED") {
      return 0;
    }

    const numericPosition = Number.parseInt(position, 10);
    if (!Number.isFinite(numericPosition) || numericPosition < 1) {
      return 0;
    }

    if (sessionType === "SPRINT") {
      return SPRINT_POINTS[numericPosition - 1] || 0;
    }

    if (sessionType === "RACE") {
      return RACE_POINTS[numericPosition - 1] || 0;
    }

    return 0;
  }

  function normalizeSessionType(value) {
    return String(value || "").trim().toUpperCase();
  }

  const api = {
    RACE_POINTS,
    SPRINT_POINTS,
    RESULT_STATUSES,
    sessionDefinitionsForEvent,
    pointsForResult,
    normalizeSessionType,
    clampCount,
  };

  if (typeof module !== "undefined" && module.exports) {
    module.exports = api;
  }

  root.F1Domain = api;
})(typeof globalThis !== "undefined" ? globalThis : window);
