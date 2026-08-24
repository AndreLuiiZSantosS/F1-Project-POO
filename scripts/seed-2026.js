const { pointsForResult } = require("../shared/domain");
const { DEFAULT_ADMIN_EMAIL, DEFAULT_ADMIN_PASSWORD } = require("../api/src/config");
const { hashPassword, normalizeEmail, nowIso } = require("../api/src/auth");
const { writeDatabase } = require("../api/src/store");

const mediaBase = "https://media.formula1.com/image/upload";
const teamLogoBase = `${mediaBase}/f_auto,c_limit,w_96,q_auto/f_auto/q_auto/fom-website/2026-redesign-assets/team%20logos`;
const driverPhotoBase = `${mediaBase}/f_auto,c_limit,w_384,q_auto/f_auto/q_auto/fom-website/drivers/2026Drivers`;

function teamLogo(slug) {
  return `${teamLogoBase}/${encodeURIComponent(slug).replaceAll("%20", "%20")}`;
}

function driverPhoto(slug) {
  return `${driverPhotoBase}/${slug}`;
}

const teams = [
  {
    id: 1,
    name: "Mercedes",
    shortName: "Mercedes",
    fullName: "Mercedes-AMG Petronas Formula One Team",
    base: "Brackley",
    country: "Reino Unido",
    powerUnit: "Mercedes",
    chief: "Toto Wolff",
    color: "#27F4D2",
    emblemUrl: teamLogo("mercedes"),
  },
  {
    id: 2,
    name: "Ferrari",
    shortName: "Ferrari",
    fullName: "Scuderia Ferrari HP",
    base: "Maranello",
    country: "Italia",
    powerUnit: "Ferrari",
    chief: "Frederic Vasseur",
    color: "#E8002D",
    emblemUrl: teamLogo("ferrari"),
  },
  {
    id: 3,
    name: "McLaren",
    shortName: "McLaren",
    fullName: "McLaren Formula 1 Team",
    base: "Woking",
    country: "Reino Unido",
    powerUnit: "Mercedes",
    chief: "Andrea Stella",
    color: "#FF8000",
    emblemUrl: teamLogo("mclaren"),
  },
  {
    id: 4,
    name: "Red Bull Racing",
    shortName: "Red Bull",
    fullName: "Oracle Red Bull Racing",
    base: "Milton Keynes",
    country: "Reino Unido",
    powerUnit: "Honda RBPT",
    chief: "Laurent Mekies",
    color: "#3671C6",
    emblemUrl: teamLogo("red bull racing"),
  },
  {
    id: 5,
    name: "Racing Bulls",
    shortName: "Racing Bulls",
    fullName: "Visa Cash App Racing Bulls Formula One Team",
    base: "Faenza",
    country: "Italia",
    powerUnit: "Honda RBPT",
    chief: "Alan Permane",
    color: "#6692FF",
    emblemUrl: teamLogo("racing bulls"),
  },
  {
    id: 6,
    name: "Alpine",
    shortName: "Alpine",
    fullName: "BWT Alpine Formula One Team",
    base: "Enstone",
    country: "Reino Unido",
    powerUnit: "Mercedes",
    chief: "Steve Nielsen",
    color: "#0093CC",
    emblemUrl: teamLogo("alpine"),
  },
  {
    id: 7,
    name: "Haas F1 Team",
    shortName: "Haas",
    fullName: "MoneyGram Haas F1 Team",
    base: "Kannapolis",
    country: "Estados Unidos",
    powerUnit: "Ferrari",
    chief: "Ayao Komatsu",
    color: "#B6BABD",
    emblemUrl: teamLogo("haas"),
  },
  {
    id: 8,
    name: "Audi",
    shortName: "Audi",
    fullName: "Audi F1 Team",
    base: "Hinwil",
    country: "Suica",
    powerUnit: "Audi",
    chief: "Jonathan Wheatley",
    color: "#00E701",
    emblemUrl: teamLogo("audi"),
  },
  {
    id: 9,
    name: "Williams",
    shortName: "Williams",
    fullName: "Atlassian Williams Racing",
    base: "Grove",
    country: "Reino Unido",
    powerUnit: "Mercedes",
    chief: "James Vowles",
    color: "#64C4FF",
    emblemUrl: teamLogo("williams"),
  },
  {
    id: 10,
    name: "Aston Martin",
    shortName: "Aston Martin",
    fullName: "Aston Martin Aramco Formula One Team",
    base: "Silverstone",
    country: "Reino Unido",
    powerUnit: "Honda",
    chief: "Andy Cowell",
    color: "#229971",
    emblemUrl: teamLogo("aston martin"),
  },
  {
    id: 11,
    name: "Cadillac",
    shortName: "Cadillac",
    fullName: "Cadillac Formula 1 Team",
    base: "Fishers",
    country: "Estados Unidos",
    powerUnit: "Ferrari",
    chief: "Graeme Lowdon",
    color: "#D7B46A",
    emblemUrl: teamLogo("cadillac"),
  },
];

const drivers = [
  { id: 1, name: "Kimi Antonelli", code: "ANT", number: 12, country: "Italia", teamId: 1, active: true, photoUrl: driverPhoto("antonelli") },
  { id: 2, name: "George Russell", code: "RUS", number: 63, country: "Reino Unido", teamId: 1, active: true, photoUrl: driverPhoto("russell") },
  { id: 3, name: "Lewis Hamilton", code: "HAM", number: 44, country: "Reino Unido", teamId: 2, active: true, photoUrl: driverPhoto("hamilton") },
  { id: 4, name: "Charles Leclerc", code: "LEC", number: 16, country: "Monaco", teamId: 2, active: true, photoUrl: driverPhoto("leclerc") },
  { id: 5, name: "Lando Norris", code: "NOR", number: 1, country: "Reino Unido", teamId: 3, active: true, photoUrl: driverPhoto("norris") },
  { id: 6, name: "Oscar Piastri", code: "PIA", number: 81, country: "Australia", teamId: 3, active: true, photoUrl: driverPhoto("piastri") },
  { id: 7, name: "Max Verstappen", code: "VER", number: 3, country: "Paises Baixos", teamId: 4, active: true, photoUrl: driverPhoto("verstappen") },
  { id: 8, name: "Liam Lawson", code: "LAW", number: 30, country: "Nova Zelandia", teamId: 4, active: true, photoUrl: driverPhoto("lawson") },
  { id: 9, name: "Isack Hadjar", code: "HAD", number: 6, country: "Franca", teamId: 4, active: true, photoUrl: driverPhoto("hadjar") },
  { id: 10, name: "Yuki Tsunoda", code: "TSU", number: 22, country: "Japao", teamId: 5, active: true, photoUrl: driverPhoto("tsunoda") },
  { id: 11, name: "Arvid Lindblad", code: "LIN", number: 41, country: "Reino Unido", teamId: 5, active: true, photoUrl: driverPhoto("lindblad") },
  { id: 12, name: "Pierre Gasly", code: "GAS", number: 10, country: "Franca", teamId: 6, active: true, photoUrl: driverPhoto("gasly") },
  { id: 13, name: "Franco Colapinto", code: "COL", number: 43, country: "Argentina", teamId: 6, active: true, photoUrl: driverPhoto("colapinto") },
  { id: 14, name: "Oliver Bearman", code: "BEA", number: 87, country: "Reino Unido", teamId: 7, active: true, photoUrl: driverPhoto("bearman") },
  { id: 15, name: "Esteban Ocon", code: "OCO", number: 31, country: "Franca", teamId: 7, active: true, photoUrl: driverPhoto("ocon") },
  { id: 16, name: "Gabriel Bortoleto", code: "BOR", number: 5, country: "Brasil", teamId: 8, active: true, photoUrl: driverPhoto("bortoleto") },
  { id: 17, name: "Nico Hulkenberg", code: "HUL", number: 27, country: "Alemanha", teamId: 8, active: true, photoUrl: driverPhoto("hulkenberg") },
  { id: 18, name: "Carlos Sainz", code: "SAI", number: 55, country: "Espanha", teamId: 9, active: true, photoUrl: driverPhoto("sainz") },
  { id: 19, name: "Alexander Albon", code: "ALB", number: 23, country: "Tailandia", teamId: 9, active: true, photoUrl: driverPhoto("albon") },
  { id: 20, name: "Fernando Alonso", code: "ALO", number: 14, country: "Espanha", teamId: 10, active: true, photoUrl: driverPhoto("alonso") },
  { id: 21, name: "Lance Stroll", code: "STR", number: 18, country: "Canada", teamId: 10, active: true, photoUrl: driverPhoto("stroll") },
  { id: 22, name: "Valtteri Bottas", code: "BOT", number: 77, country: "Finlandia", teamId: 11, active: true, photoUrl: driverPhoto("bottas") },
  { id: 23, name: "Sergio Perez", code: "PER", number: 11, country: "Mexico", teamId: 11, active: true, photoUrl: driverPhoto("perez") },
];

const events = [
  { id: 1, round: 1, name: "Australian Grand Prix", circuit: "Albert Park Grand Prix Circuit", city: "Melbourne", country: "Australia", date: "2026-03-08", hasSprint: false, practiceSessionsCount: 3, qualifyingSessionsCount: 3, notes: "" },
  { id: 2, round: 2, name: "Chinese Grand Prix", circuit: "Shanghai International Circuit", city: "Shanghai", country: "China", date: "2026-03-15", hasSprint: true, practiceSessionsCount: 1, qualifyingSessionsCount: 3, notes: "Fim de semana sprint." },
  { id: 3, round: 3, name: "Japanese Grand Prix", circuit: "Suzuka Circuit", city: "Suzuka", country: "Japao", date: "2026-03-29", hasSprint: false, practiceSessionsCount: 3, qualifyingSessionsCount: 3, notes: "" },
  { id: 4, round: 4, name: "Miami Grand Prix", circuit: "Miami International Autodrome", city: "Miami", country: "Estados Unidos", date: "2026-05-03", hasSprint: true, practiceSessionsCount: 1, qualifyingSessionsCount: 3, notes: "Fim de semana sprint." },
  { id: 5, round: 5, name: "Canadian Grand Prix", circuit: "Circuit Gilles-Villeneuve", city: "Montreal", country: "Canada", date: "2026-05-24", hasSprint: true, practiceSessionsCount: 1, qualifyingSessionsCount: 3, notes: "Fim de semana sprint." },
  { id: 6, round: 6, name: "Monaco Grand Prix", circuit: "Circuit de Monaco", city: "Monte Carlo", country: "Monaco", date: "2026-06-07", hasSprint: false, practiceSessionsCount: 3, qualifyingSessionsCount: 3, notes: "" },
  { id: 7, round: 7, name: "Spanish Grand Prix", circuit: "Circuit de Barcelona-Catalunya", city: "Barcelona", country: "Espanha", date: "2026-06-14", hasSprint: false, practiceSessionsCount: 3, qualifyingSessionsCount: 3, notes: "" },
  { id: 8, round: 8, name: "Austrian Grand Prix", circuit: "Red Bull Ring", city: "Spielberg", country: "Austria", date: "2026-06-28", hasSprint: false, practiceSessionsCount: 3, qualifyingSessionsCount: 3, notes: "" },
  { id: 9, round: 9, name: "British Grand Prix", circuit: "Silverstone Circuit", city: "Silverstone", country: "Reino Unido", date: "2026-07-05", hasSprint: true, practiceSessionsCount: 1, qualifyingSessionsCount: 3, notes: "Fim de semana sprint." },
  { id: 10, round: 10, name: "Belgian Grand Prix", circuit: "Circuit de Spa-Francorchamps", city: "Spa-Francorchamps", country: "Belgica", date: "2026-07-19", hasSprint: false, practiceSessionsCount: 3, qualifyingSessionsCount: 3, notes: "" },
  { id: 11, round: 11, name: "Hungarian Grand Prix", circuit: "Hungaroring", city: "Budapest", country: "Hungria", date: "2026-07-26", hasSprint: false, practiceSessionsCount: 3, qualifyingSessionsCount: 3, notes: "" },
  { id: 12, round: 12, name: "Dutch Grand Prix", circuit: "Circuit Zandvoort", city: "Zandvoort", country: "Paises Baixos", date: "2026-08-23", hasSprint: true, practiceSessionsCount: 1, qualifyingSessionsCount: 3, notes: "Fim de semana sprint." },
  { id: 13, round: 13, name: "Italian Grand Prix", circuit: "Autodromo Nazionale Monza", city: "Monza", country: "Italia", date: "2026-09-06", hasSprint: false, practiceSessionsCount: 3, qualifyingSessionsCount: 3, notes: "" },
  { id: 14, round: 14, name: "Spanish Grand Prix - Madrid", circuit: "Madring", city: "Madrid", country: "Espanha", date: "2026-09-13", hasSprint: false, practiceSessionsCount: 3, qualifyingSessionsCount: 3, notes: "" },
  { id: 15, round: 15, name: "Azerbaijan Grand Prix", circuit: "Baku City Circuit", city: "Baku", country: "Azerbaijao", date: "2026-09-26", hasSprint: false, practiceSessionsCount: 3, qualifyingSessionsCount: 3, notes: "" },
  { id: 16, round: 16, name: "Bahrain Grand Prix", circuit: "Sepang International Circuit", city: "Sepang", country: "Malasia", date: "2026-10-04", hasSprint: false, practiceSessionsCount: 3, qualifyingSessionsCount: 3, notes: "Calendario atual da F1 lista Bahrain Grand Prix in Malaysia." },
  { id: 17, round: 17, name: "Singapore Grand Prix", circuit: "Marina Bay Street Circuit", city: "Singapore", country: "Singapore", date: "2026-10-11", hasSprint: true, practiceSessionsCount: 1, qualifyingSessionsCount: 3, notes: "Fim de semana sprint." },
  { id: 18, round: 18, name: "United States Grand Prix", circuit: "Circuit of The Americas", city: "Austin", country: "Estados Unidos", date: "2026-10-25", hasSprint: false, practiceSessionsCount: 3, qualifyingSessionsCount: 3, notes: "" },
  { id: 19, round: 19, name: "Mexico City Grand Prix", circuit: "Autodromo Hermanos Rodriguez", city: "Mexico City", country: "Mexico", date: "2026-11-01", hasSprint: false, practiceSessionsCount: 3, qualifyingSessionsCount: 3, notes: "" },
  { id: 20, round: 20, name: "Sao Paulo Grand Prix", circuit: "Autodromo Jose Carlos Pace", city: "Sao Paulo", country: "Brasil", date: "2026-11-08", hasSprint: false, practiceSessionsCount: 3, qualifyingSessionsCount: 3, notes: "" },
  { id: 21, round: 21, name: "Las Vegas Grand Prix", circuit: "Las Vegas Strip Circuit", city: "Las Vegas", country: "Estados Unidos", date: "2026-11-21", hasSprint: false, practiceSessionsCount: 3, qualifyingSessionsCount: 3, notes: "" },
  { id: 22, round: 22, name: "Qatar Grand Prix", circuit: "Lusail International Circuit", city: "Lusail", country: "Qatar", date: "2026-11-29", hasSprint: false, practiceSessionsCount: 3, qualifyingSessionsCount: 3, notes: "" },
  { id: 23, round: 23, name: "Abu Dhabi Grand Prix", circuit: "Yas Marina Circuit", city: "Abu Dhabi", country: "Emirados Arabes Unidos", date: "2026-12-06", hasSprint: false, practiceSessionsCount: 3, qualifyingSessionsCount: 3, notes: "" },
];

const raceResults = [
  [1, ["RUS", "ANT", "LEC", "HAM", "NOR", "VER", "BEA", "LIN", "BOR", "GAS"]],
  [2, ["ANT", "RUS", "HAM", "LEC", "BEA", "GAS", "LAW", "HAD", "SAI", "COL"]],
  [3, ["ANT", "PIA", "LEC", "RUS", "NOR", "HAM", "GAS", "VER", "LAW", "OCO"]],
  [4, ["ANT", "NOR", "PIA", "RUS", "VER", "HAM", "COL", "LEC", "SAI", "ALB"]],
  [5, ["ANT", "HAM", "VER", "LEC", "HAD", "COL", "LAW", "GAS", "SAI", "BEA"]],
  [6, ["ANT", "HAM", "GAS", "HAD", "PIA", "LAW", "LIN", "ALB", "OCO", "ALO"]],
  [7, ["HAM", "RUS", "NOR", "VER", "PIA", "HAD", "GAS", "LAW", "LIN", "COL"]],
  [8, ["RUS", "VER", "ANT", "PIA", "HAM", "HAD", "NOR", "LEC", "LAW", "LIN"]],
  [9, ["LEC", "RUS", "HAM", "NOR", "HAD", "LAW", "LIN", "BOR", "COL", "GAS"]],
  [10, ["ANT", "LEC", "VER", "HAM", "PIA", "HAD", "NOR", "BOR", "LIN", "COL"]],
  [11, ["NOR", "VER", "ANT", "LEC", "HAM", "HAD", "RUS", "LAW", "HUL", "LIN"]],
  [12, ["NOR", "ANT", "RUS", "HAM", "LEC", "PIA", "LAW", "HUL", "ALO", "GAS"]],
];

const sprintResults = [
  [2, ["RUS", "LEC", "HAM", "NOR", "ANT", "PIA", "LAW", "BEA"]],
  [4, ["NOR", "PIA", "LEC", "RUS", "VER", "ANT", "HAM", "GAS"]],
  [5, ["RUS", "NOR", "ANT", "PIA", "LEC", "HAM", "VER", "LIN"]],
  [9, ["ANT", "HAM", "NOR", "RUS", "LEC", "VER", "PIA", "LAW"]],
  [12, ["RUS", "LEC", "NOR", "ANT", "PIA", "VER", "HAM", "GAS"]],
];

function buildResults() {
  const driverByCode = new Map(drivers.map((driver) => [driver.code, driver]));
  const results = [];
  let id = 1;

  for (const [eventId, codes] of raceResults) {
    codes.forEach((code, index) => {
      const position = index + 1;
      results.push({
        id: id++,
        eventId,
        driverId: driverByCode.get(code).id,
        sessionType: "RACE",
        position,
        time: "",
        gap: "",
        laps: "",
        status: "CLASSIFIED",
        points: pointsForResult("RACE", position, "CLASSIFIED"),
        notes: "Resultado oficial F1 2026 seedado manualmente.",
      });
    });
  }

  for (const [eventId, codes] of sprintResults) {
    codes.forEach((code, index) => {
      const position = index + 1;
      results.push({
        id: id++,
        eventId,
        driverId: driverByCode.get(code).id,
        sessionType: "SPRINT",
        position,
        time: "",
        gap: "",
        laps: "",
        status: "CLASSIFIED",
        points: pointsForResult("SPRINT", position, "CLASSIFIED"),
        notes: "Resultado sprint oficial F1 2026 seedado manualmente.",
      });
    });
  }

  return results;
}

async function main() {
  const admin = {
    id: 1,
    name: "Admin F1",
    email: normalizeEmail(DEFAULT_ADMIN_EMAIL),
    role: "admin",
    passwordHash: await hashPassword(DEFAULT_ADMIN_PASSWORD),
    createdAt: nowIso(),
  };
  const results = buildResults();
  const database = {
    meta: {
      version: 2,
      updatedAt: nowIso(),
      source: "Formula1.com results/standings and FIA/F1 2026 sprint calendar, manual seed.",
      sourceUpdatedAt: "2026-08-23",
      nextIds: {
        team: Math.max(...teams.map((team) => team.id)) + 1,
        driver: Math.max(...drivers.map((driver) => driver.id)) + 1,
        event: Math.max(...events.map((event) => event.id)) + 1,
        result: Math.max(...results.map((result) => result.id)) + 1,
        user: 2,
        prediction: 1,
      },
    },
    teams,
    drivers,
    events,
    results,
    users: [admin],
    authTokens: [],
    predictions: [],
  };

  await writeDatabase(database);
  console.log(`Seed 2026 aplicado: ${teams.length} equipes, ${drivers.length} pilotos, ${events.length} etapas, ${results.length} resultados.`);
  console.log(`Admin: ${DEFAULT_ADMIN_EMAIL} / ${DEFAULT_ADMIN_PASSWORD}`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
