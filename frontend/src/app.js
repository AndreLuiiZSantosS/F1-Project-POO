const API_BASE = localStorage.getItem("f1-api-base") || "http://127.0.0.1:8000/api";
const domain = window.F1Domain;

const SESSION_SLUGS = {
  FP1: "tl1",
  FP2: "tl2",
  FP3: "tl3",
  Q1: "q1",
  Q2: "q2",
  Q3: "q3",
  SPRINT_QUALIFYING: "sprint-quali",
  SPRINT: "sprint",
  RACE: "corrida",
};

const SLUG_TO_SESSION = Object.fromEntries(Object.entries(SESSION_SLUGS).map(([type, slug]) => [slug, type]));

const state = {
  teams: [],
  drivers: [],
  events: [],
  standings: { drivers: [], teams: [] },
  statuses: domain.RESULT_STATUSES,
  token: localStorage.getItem("f1-auth-token") || "",
  currentUser: null,
  myPredictions: [],
  leaderboard: [],
  selectedPredictionEventId: "",
  selectedPredictionSession: "RACE",
  adminEmail: "",
};

const elements = {
  pageRoot: document.querySelector("#page-root"),
  pageHero: document.querySelector("#page-hero"),
  summaryStats: document.querySelector("#summary-stats"),
  navLinks: Array.from(document.querySelectorAll("[data-nav]")),
  adminLinks: Array.from(document.querySelectorAll("[data-admin-link]")),
  authLink: document.querySelector("#auth-nav-link"),
};

const routes = [
  { pattern: /^\/$/, name: "Dashboard", render: renderDashboard },
  { pattern: /^\/login\/?$/, name: "Login", render: renderLogin },
  { pattern: /^\/registro\/?$/, name: "Registro", render: renderRegister },
  { pattern: /^\/previsoes\/?$/, name: "Previsoes", render: renderPredictions },
  { pattern: /^\/minhas-previsoes\/?$/, name: "Minhas previsoes", render: renderMyPredictions },
  { pattern: /^\/ranking-usuarios\/?$/, name: "Ranking de usuarios", render: renderUserLeaderboard },
  { pattern: /^\/resultados\/?$/, name: "Resultados", render: renderResults },
  { pattern: /^\/etapas\/?$/, name: "Etapas", render: renderEvents },
  { pattern: /^\/etapas\/(\d+)\/?$/, name: "Detalhe da etapa", render: ([eventId]) => renderEventDetail(Number(eventId)) },
  { pattern: /^\/etapas\/(\d+)\/(tl1|tl2|tl3|q1|q2|q3|sprint-quali|sprint|corrida)\/?$/, name: "Sessao da etapa", render: ([eventId, sessionSlug]) => renderEventSession(Number(eventId), sessionSlug) },
  { pattern: /^\/pilotos\/?$/, name: "Pilotos", render: renderDrivers },
  { pattern: /^\/pilotos\/(\d+)\/?$/, name: "Detalhe do piloto", render: ([driverId]) => renderDriverDetail(Number(driverId)) },
  { pattern: /^\/equipes\/?$/, name: "Equipes", render: renderTeams },
  { pattern: /^\/equipes\/(\d+)\/?$/, name: "Detalhe da equipe", render: ([teamId]) => renderTeamDetail(Number(teamId)) },
  { pattern: /^\/classificacao\/?$/, name: "Classificacao", render: renderStandingsOverview },
  { pattern: /^\/classificacao\/pilotos\/?$/, name: "Classificacao de pilotos", render: renderDriverStandingsPage },
  { pattern: /^\/classificacao\/equipes\/?$/, name: "Classificacao de equipes", render: renderTeamStandingsPage },
  { pattern: /^\/admin\/?$/, name: "Admin", render: renderAdminHome },
  { pattern: /^\/admin\/equipes\/?$/, name: "Admin equipes", render: renderAdminTeams },
  { pattern: /^\/admin\/pilotos\/?$/, name: "Admin pilotos", render: renderAdminDrivers },
  { pattern: /^\/admin\/etapas\/?$/, name: "Admin etapas", render: renderAdminEvents },
  { pattern: /^\/admin\/resultados\/?$/, name: "Admin resultados", render: renderAdminResults },
  { pattern: /^\/mapa\/?$/, name: "Mapa do app", render: renderSitemap },
];

const declaredPages = [
  ["/", "Dashboard"],
  ["/login", "Login e conta"],
  ["/registro", "Registro de usuario"],
  ["/previsoes", "Criar previsoes"],
  ["/minhas-previsoes", "Minhas previsoes"],
  ["/ranking-usuarios", "Ranking dos usuarios"],
  ["/resultados", "Resultados gerais"],
  ["/etapas", "Lista de etapas"],
  ["/etapas/:id", "Detalhe da etapa"],
  ["/etapas/:id/tl1", "Treino livre 1"],
  ["/etapas/:id/tl2", "Treino livre 2"],
  ["/etapas/:id/tl3", "Treino livre 3"],
  ["/etapas/:id/q1", "Qualificacao Q1"],
  ["/etapas/:id/q2", "Qualificacao Q2"],
  ["/etapas/:id/q3", "Qualificacao Q3"],
  ["/etapas/:id/sprint-quali", "Qualificacao sprint"],
  ["/etapas/:id/sprint", "Corrida sprint"],
  ["/etapas/:id/corrida", "Corrida"],
  ["/pilotos", "Lista de pilotos"],
  ["/pilotos/:id", "Detalhe do piloto"],
  ["/equipes", "Lista de equipes"],
  ["/equipes/:id", "Detalhe da equipe"],
  ["/classificacao", "Classificacao geral"],
  ["/classificacao/pilotos", "Classificacao de pilotos"],
  ["/classificacao/equipes", "Classificacao de equipes"],
  ["/admin", "Painel admin"],
  ["/admin/equipes", "Cadastro de equipes"],
  ["/admin/pilotos", "Cadastro de pilotos"],
  ["/admin/etapas", "Cadastro de etapas"],
  ["/admin/resultados", "Cadastro de resultados"],
  ["/mapa", "Mapa do app"],
];

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function initials(value) {
  return String(value || "F1")
    .split(/\s+/)
    .filter(Boolean)
    .slice(0, 2)
    .map((part) => part[0].toUpperCase())
    .join("");
}

function pluralize(count, singular, plural) {
  return count === 1 ? singular : plural;
}

function formatDate(value) {
  if (!value) return "Data aberta";
  const [year, month, day] = value.split("-");
  return year && month && day ? `${day}/${month}/${year}` : value;
}

function isAdmin() {
  return state.currentUser?.role === "admin";
}

function pathForEvent(event) {
  return `/etapas/${event.id}`;
}

function pathForSession(event, session) {
  return `${pathForEvent(event)}/${SESSION_SLUGS[session.type] || session.type.toLowerCase()}`;
}

function byId(rows, id) {
  return rows.find((row) => Number(row.id) === Number(id)) || null;
}

function getSession(event, sessionType) {
  return event?.sessions.find((session) => session.type === sessionType) || null;
}

async function apiFetch(path, options = {}) {
  const headers = {
    "Content-Type": "application/json",
    ...(state.token ? { Authorization: `Bearer ${state.token}` } : {}),
    ...(options.headers || {}),
  };
  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers,
  });

  const payload = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(payload.error || "Erro na API");
  }
  return payload;
}

function setToken(token) {
  state.token = token || "";
  if (state.token) {
    localStorage.setItem("f1-auth-token", state.token);
  } else {
    localStorage.removeItem("f1-auth-token");
  }
}

function setHero(kicker, title, subtitle = "") {
  elements.pageHero.querySelector(".control-copy").innerHTML = `
    <span class="eyebrow">${escapeHtml(kicker)}</span>
    <h1>${escapeHtml(title)}</h1>
    ${subtitle ? `<p class="hero-subtitle">${escapeHtml(subtitle)}</p>` : ""}
  `;
}

function renderSummary() {
  const resultCount = state.events.reduce(
    (total, event) => total + event.sessions.reduce((subtotal, session) => subtotal + session.results.length, 0),
    0
  );
  const sprintCount = state.events.filter((event) => event.hasSprint).length;
  const predictedCount = state.myPredictions.length;

  elements.summaryStats.innerHTML = [
    { value: state.events.length, label: pluralize(state.events.length, "etapa", "etapas") },
    { value: state.drivers.length, label: pluralize(state.drivers.length, "piloto", "pilotos") },
    { value: state.teams.length, label: pluralize(state.teams.length, "equipe", "equipes") },
    { value: sprintCount, label: "sprints" },
    { value: resultCount, label: pluralize(resultCount, "resultado", "resultados") },
    { value: predictedCount, label: pluralize(predictedCount, "previsao", "previsoes") },
  ].map((item) => `
    <div class="stat-card">
      <strong>${escapeHtml(item.value)}</strong>
      <span>${escapeHtml(item.label)}</span>
    </div>
  `).join("");
}

function updateAuthNav() {
  elements.adminLinks.forEach((link) => {
    link.hidden = !isAdmin();
  });
  if (elements.authLink) {
    elements.authLink.textContent = state.currentUser ? "Conta" : "Entrar";
  }
}

function teamBadge(team, className = "") {
  const color = team?.color || "#e10600";
  const label = team?.shortName || team?.name || "Equipe";
  if (team?.emblemUrl) {
    return `
      <span class="team-badge ${className}" style="--team-color:${escapeHtml(color)}">
        <img src="${escapeHtml(team.emblemUrl)}" alt="${escapeHtml(label)}" />
      </span>
    `;
  }

  return `
    <span class="team-badge ${className}" style="--team-color:${escapeHtml(color)}">
      <span>${escapeHtml(initials(label))}</span>
    </span>
  `;
}

function driverToken(driver) {
  const team = driver?.team;
  return `
    <a class="driver-token linked-token" href="/pilotos/${escapeHtml(driver?.id || "")}" data-route>
      <span class="driver-number" style="--team-color:${escapeHtml(team?.color || "#e10600")}">${escapeHtml(driver?.number || "-")}</span>
      <div>
        <strong>${escapeHtml(driver?.name || "Piloto")}</strong>
        <small>${escapeHtml(team?.name || "Sem equipe")}</small>
      </div>
    </a>
  `;
}

function actionLink(href, label, variant = "") {
  return `<a class="action-link ${variant}" href="${escapeHtml(href)}" data-route>${escapeHtml(label)}</a>`;
}

function sectionHead(kicker, title, aside = "") {
  return `
    <div class="section-head">
      <div>
        <span class="eyebrow">${escapeHtml(kicker)}</span>
        <h2>${escapeHtml(title)}</h2>
      </div>
      ${aside}
    </div>
  `;
}

function emptyState(title, body, aside = "") {
  return `
    <div class="empty-state">
      <h3>${escapeHtml(title)}</h3>
      <p>${escapeHtml(body)}</p>
      ${aside ? `<div class="panel-actions centered">${aside}</div>` : ""}
    </div>
  `;
}

function adminGate() {
  if (isAdmin()) {
    return "";
  }
  if (!state.currentUser) {
    return emptyState("Login necessario", "Entre com a conta admin para manipular cadastros.", actionLink("/login", "Entrar", "primary"));
  }
  return emptyState("Acesso bloqueado", "Sua conta pode ver resultados e criar previsoes, mas nao pode alterar dados oficiais.", actionLink("/", "Voltar ao painel", "primary"));
}

function resultTable(results) {
  const rows = results.length
    ? results.map((result) => `
      <tr>
        <td class="position-cell">${escapeHtml(result.position || "-")}</td>
        <td>${driverToken(result.driver)}</td>
        <td>${escapeHtml(result.time || "-")}</td>
        <td>${escapeHtml(result.gap || "-")}</td>
        <td>${escapeHtml(result.status || "-")}</td>
        <td class="points-cell">${escapeHtml(result.points || 0)}</td>
      </tr>
    `).join("")
    : `<tr><td colspan="6" class="empty-row">Aguardando resultado cadastrado.</td></tr>`;

  return `
    <div class="table-scroll">
      <table>
        <thead>
          <tr>
            <th>Pos</th>
            <th>Piloto</th>
            <th>Tempo</th>
            <th>Gap</th>
            <th>Status</th>
            <th>Pts</th>
          </tr>
        </thead>
        <tbody>${rows}</tbody>
      </table>
    </div>
  `;
}

function sessionCard(event, session) {
  return `
    <article class="session-block">
      <header>
        <div>
          <span>${escapeHtml(session.group)}</span>
          <h3>${escapeHtml(session.label)}</h3>
        </div>
        <a href="${escapeHtml(pathForSession(event, session))}" data-route>${escapeHtml(session.shortLabel)}</a>
      </header>
      ${resultTable(session.results)}
    </article>
  `;
}

function eventCover(event) {
  return `
    <div class="event-cover">
      <span class="round-number">Round ${escapeHtml(event.round)}</span>
      <h3>${escapeHtml(event.name)}</h3>
      <p>${escapeHtml(event.circuit || "Circuito aberto")}</p>
      <div class="event-meta">
        <span>${escapeHtml(event.country || "Pais aberto")}</span>
        <span>${formatDate(event.date)}</span>
        <span>${event.hasSprint ? "Sprint" : "GP tradicional"}</span>
        <span>${escapeHtml(event.practiceSessionsCount)} ${pluralize(event.practiceSessionsCount, "TL", "TLs")}</span>
      </div>
    </div>
  `;
}

function eventCard(event) {
  const filledSessions = event.sessions.filter((session) => session.results.length).length;
  return `
    <article class="route-card event-card">
      <div>
        <span class="round-number mini">Round ${escapeHtml(event.round)}</span>
        <h3>${escapeHtml(event.name)}</h3>
        <p>${escapeHtml(event.circuit || "Circuito aberto")}</p>
      </div>
      <div class="event-meta compact">
        <span>${formatDate(event.date)}</span>
        <span>${event.hasSprint ? "Sprint" : "Tradicional"}</span>
        <span>${filledSessions}/${event.sessions.length} sessoes com dados</span>
      </div>
      <div class="button-row">
        ${actionLink(pathForEvent(event), "Abrir etapa", "primary")}
        ${event.sessions.map((session) => actionLink(pathForSession(event, session), session.shortLabel)).join("")}
      </div>
    </article>
  `;
}

function driverCard(driver) {
  return `
    <article class="driver-card" style="--team-color:${escapeHtml(driver.team?.color || "#e10600")}">
      <div class="driver-photo">
        ${driver.photoUrl ? `<img src="${escapeHtml(driver.photoUrl)}" alt="${escapeHtml(driver.name)}" loading="lazy" />` : `<span>${escapeHtml(driver.code || initials(driver.name))}</span>`}
      </div>
      <div class="driver-card-body">
        <span class="driver-number large">${escapeHtml(driver.number)}</span>
        <h3>${escapeHtml(driver.name)}</h3>
        <p>${escapeHtml(driver.country || "Pais aberto")}</p>
        <div class="team-line">${teamBadge(driver.team)}<a href="/equipes/${escapeHtml(driver.teamId)}" data-route>${escapeHtml(driver.team?.name || "Sem equipe")}</a></div>
        <div class="button-row">${actionLink(`/pilotos/${driver.id}`, "Detalhes", "primary")}</div>
      </div>
    </article>
  `;
}

function teamCard(team) {
  const teamDrivers = state.drivers.filter((driver) => Number(driver.teamId) === Number(team.id));
  return `
    <article class="team-card" style="--team-color:${escapeHtml(team.color)}">
      <div class="team-card-head">
        ${teamBadge(team, "large")}
        <div>
          <h3>${escapeHtml(team.name)}</h3>
          <p>${escapeHtml(team.fullName || team.name)}</p>
        </div>
      </div>
      <dl>
        <div><dt>Base</dt><dd>${escapeHtml(team.base || "-")}</dd></div>
        <div><dt>Motor</dt><dd>${escapeHtml(team.powerUnit || "-")}</dd></div>
        <div><dt>Chefe</dt><dd>${escapeHtml(team.chief || "-")}</dd></div>
      </dl>
      <div class="team-drivers">
        ${teamDrivers.map((driver) => `<a href="/pilotos/${escapeHtml(driver.id)}" data-route>${escapeHtml(driver.number)} ${escapeHtml(driver.name)}</a>`).join("") || "<span>Sem pilotos</span>"}
      </div>
      <div class="button-row">${actionLink(`/equipes/${team.id}`, "Detalhes", "primary")}</div>
    </article>
  `;
}

function standingsTable(rows, type) {
  if (!rows.length) return '<div class="empty-state compact">Sem dados para classificacao.</div>';

  return `
    <div class="table-scroll">
      <table>
        <thead>
          <tr>
            <th>#</th>
            <th>${type === "drivers" ? "Piloto" : "Equipe"}</th>
            <th>Pts</th>
            <th>Vitorias</th>
            <th>Podios</th>
          </tr>
        </thead>
        <tbody>
          ${rows.map((row, index) => {
            const subject = type === "drivers"
              ? driverToken(row.driver)
              : `<a class="team-line linked-token" href="/equipes/${escapeHtml(row.team.id)}" data-route>${teamBadge(row.team)}<strong>${escapeHtml(row.team.name)}</strong></a>`;
            return `
              <tr>
                <td class="position-cell">${index + 1}</td>
                <td>${subject}</td>
                <td class="points-cell">${escapeHtml(row.points || 0)}</td>
                <td>${escapeHtml(row.wins || 0)}</td>
                <td>${escapeHtml(row.podiums || 0)}</td>
              </tr>
            `;
          }).join("")}
        </tbody>
      </table>
    </div>
  `;
}

function renderDashboard() {
  setHero("Dashboard", "F1 Results Hub", `${declaredPages.length} paginas/rotas, resultados reais cadastrados e previsoes de usuarios`);
  const latestEvent = state.events.findLast((event) => event.sessions.some((session) => session.results.length)) || state.events[0];
  return `
    ${sectionHead("Visao geral", "Centro do campeonato", actionLink("/mapa", "Ver mapa completo", "primary"))}
    <div class="dashboard-grid">
      <article class="route-card feature-card">
        <h3>Resultados por etapa</h3>
        <p>Abra TLs, qualificacoes, sprint e corrida. So aparece o que foi cadastrado pelo admin.</p>
        ${actionLink("/resultados", "Abrir resultados", "primary")}
      </article>
      <article class="route-card feature-card">
        <h3>Previsoes</h3>
        <p>Monte seu top 10 para corridas futuras e pontue quando acertar a posicao final.</p>
        ${actionLink("/previsoes", "Criar previsao", "primary")}
      </article>
      <article class="route-card feature-card">
        <h3>Ranking</h3>
        <p>Quem acertar piloto e posicao recebe a mesma pontuacao que o piloto fez na sessao.</p>
        ${actionLink("/ranking-usuarios", "Ver ranking", "primary")}
      </article>
      ${isAdmin() ? `
        <article class="route-card feature-card admin-feature">
          <h3>Painel admin</h3>
          <p>Cadastre equipes, pilotos, etapas e resultados sem abrir outra area externa.</p>
          ${actionLink("/admin", "Abrir admin", "primary")}
        </article>
      ` : ""}
    </div>
    <div class="split-layout">
      <div class="table-panel">
        <h3>Top pilotos</h3>
        ${standingsTable((state.standings.drivers || []).slice(0, 8), "drivers")}
      </div>
      <div class="table-panel">
        <h3>Etapa em destaque</h3>
        ${latestEvent ? `${eventCard(latestEvent)}` : emptyState("Sem etapas", "Cadastre etapas no painel admin.")}
      </div>
    </div>
  `;
}

function renderLogin() {
  setHero("Conta", state.currentUser ? "Sua conta" : "Entrar", state.currentUser ? "Sessao ativa neste navegador" : "Login de usuario ou admin");

  if (state.currentUser) {
    return `
      ${sectionHead("Conta", state.currentUser.name, isAdmin() ? actionLink("/admin", "Abrir admin", "primary") : actionLink("/previsoes", "Criar previsao", "primary"))}
      <div class="auth-grid">
        <article class="auth-panel">
          <span class="eyebrow">${escapeHtml(state.currentUser.role === "admin" ? "Admin" : "Usuario")}</span>
          <h3>${escapeHtml(state.currentUser.email)}</h3>
          <p>${isAdmin() ? "Admin liberado para manipular cadastros e resultados." : "Usuario liberado para consultar resultados e criar previsoes."}</p>
          <button type="button" id="logout-button">Sair</button>
        </article>
        <article class="auth-panel dark-panel">
          <span class="eyebrow">Atalhos</span>
          <div class="button-row">
            ${actionLink("/minhas-previsoes", "Minhas previsoes", "primary")}
            ${actionLink("/ranking-usuarios", "Ranking")}
            ${isAdmin() ? actionLink("/admin/resultados", "Resultados admin") : ""}
          </div>
        </article>
      </div>
    `;
  }

  return `
    ${sectionHead("Login", "Acessar sistema", actionLink("/registro", "Criar conta"))}
    <div class="auth-grid">
      <form class="auth-panel" id="login-form">
        <label>Email<input name="email" type="email" required autocomplete="email" placeholder="voce@email.com" /></label>
        <label>Senha<input name="password" type="password" required autocomplete="current-password" /></label>
        <button type="submit">Entrar</button>
        <div class="admin-status" id="auth-status"></div>
      </form>
      <article class="auth-panel dark-panel">
        <span class="eyebrow">Admin local</span>
        <h3>${escapeHtml(state.adminEmail || "admin configurado")}</h3>
        <p>Entrando com as credenciais admin, o menu de admin aparece e as rotas de cadastro ficam liberadas.</p>
      </article>
    </div>
  `;
}

function renderRegister() {
  setHero("Registro", "Criar conta", "Conta comum para previsoes e ranking");
  if (state.currentUser) {
    return emptyState("Voce ja esta logado", "Saia da conta atual para criar outro usuario.", actionLink("/login", "Ver conta", "primary"));
  }

  return `
    ${sectionHead("Registro", "Novo usuario", actionLink("/login", "Ja tenho conta"))}
    <form class="auth-panel narrow-panel" id="register-form">
      <div class="form-grid">
        <label>Nome<input name="name" required autocomplete="name" /></label>
        <label>Email<input name="email" type="email" required autocomplete="email" /></label>
        <label class="full-field">Senha<input name="password" type="password" minlength="6" required autocomplete="new-password" /></label>
      </div>
      <button type="submit">Criar conta</button>
      <div class="admin-status" id="auth-status"></div>
    </form>
  `;
}

function renderResults() {
  setHero("Resultados", "Todas as etapas", "Cada sessao tem sua propria pagina");
  const aside = isAdmin() ? actionLink("/admin/resultados", "Adicionar resultado", "primary") : actionLink("/previsoes", "Criar previsao", "primary");
  if (!state.events.length) return `${sectionHead("Etapas", "Resultados")}${emptyState("Sem etapas", "Cadastre etapas no painel admin.")}`;
  return `
    ${sectionHead("Etapas", "Resultados gerais", aside)}
    <div class="route-grid">${state.events.map(eventCard).join("")}</div>
  `;
}

function renderEvents() {
  setHero("Calendario", "Etapas cadastradas", "Fim de semana tradicional ou sprint");
  const aside = isAdmin() ? actionLink("/admin/etapas", "Nova etapa", "primary") : "";
  return `
    ${sectionHead("Etapas", "Calendario", aside)}
    <div class="route-grid">${state.events.map(eventCard).join("") || emptyState("Sem etapas", "Cadastre a primeira etapa no admin.")}</div>
  `;
}

function renderEventDetail(eventId) {
  const event = byId(state.events, eventId);
  if (!event) {
    setHero("Etapa", "Etapa nao encontrada");
    return emptyState("Nao encontrada", "Essa etapa nao existe no banco local.");
  }

  setHero(`Round ${event.round}`, event.name, event.circuit || "Circuito aberto");
  return `
    ${sectionHead("Etapa", event.name, actionLink("/etapas", "Voltar para etapas"))}
    <article class="event-focus">
      ${eventCover(event)}
      <div class="sessions-grid">${event.sessions.map((session) => sessionCard(event, session)).join("")}</div>
    </article>
  `;
}

function renderEventSession(eventId, sessionSlug) {
  const event = byId(state.events, eventId);
  const sessionType = SLUG_TO_SESSION[sessionSlug];
  const session = getSession(event, sessionType);

  if (!event || !session) {
    setHero("Sessao", "Sessao nao encontrada");
    return emptyState("Nao encontrada", "Essa sessao nao existe para a etapa selecionada.");
  }

  setHero(session.shortLabel, session.label, `${event.name} - ${event.circuit || "circuito aberto"}`);
  return `
    ${sectionHead(session.group, session.label, actionLink(pathForEvent(event), "Voltar para etapa"))}
    ${eventCover(event)}
    <article class="session-block standalone">
      <header>
        <div>
          <span>${escapeHtml(session.group)}</span>
          <h3>${escapeHtml(session.label)}</h3>
        </div>
        <strong>${escapeHtml(session.shortLabel)}</strong>
      </header>
      ${resultTable(session.results)}
    </article>
    <div class="button-row session-nav">
      ${event.sessions.map((item) => actionLink(pathForSession(event, item), item.shortLabel, item.type === session.type ? "primary" : "")).join("")}
    </div>
  `;
}

function renderDrivers() {
  setHero("Grid", "Pilotos", "Numero, equipe e detalhes individuais");
  const aside = isAdmin() ? actionLink("/admin/pilotos", "Novo piloto", "primary") : "";
  return `
    ${sectionHead("Pilotos", "Grid cadastrado", aside)}
    <div class="driver-grid">${state.drivers.map(driverCard).join("") || emptyState("Sem pilotos", "Cadastre pilotos no admin.")}</div>
  `;
}

function renderDriverDetail(driverId) {
  const driver = byId(state.drivers, driverId);
  if (!driver) {
    setHero("Piloto", "Piloto nao encontrado");
    return emptyState("Nao encontrado", "Esse piloto nao existe no banco local.");
  }

  const driverResults = state.events.flatMap((event) =>
    event.sessions.flatMap((session) =>
      session.results
        .filter((result) => Number(result.driverId) === Number(driver.id))
        .map((result) => ({ event, session, result }))
    )
  );

  setHero(`#${driver.number}`, driver.name, driver.team?.name || "Sem equipe");
  return `
    ${sectionHead("Piloto", driver.name, actionLink("/pilotos", "Voltar para pilotos"))}
    <div class="split-layout">
      ${driverCard(driver)}
      <div class="table-panel">
        <h3>Resultados do piloto</h3>
        <div class="table-scroll">
          <table>
            <thead><tr><th>Etapa</th><th>Sessao</th><th>Pos</th><th>Pts</th></tr></thead>
            <tbody>
              ${driverResults.length ? driverResults.map(({ event, session, result }) => `
                <tr>
                  <td><a href="${escapeHtml(pathForEvent(event))}" data-route>${escapeHtml(event.name)}</a></td>
                  <td><a href="${escapeHtml(pathForSession(event, session))}" data-route>${escapeHtml(session.shortLabel)}</a></td>
                  <td>${escapeHtml(result.position || "-")}</td>
                  <td class="points-cell">${escapeHtml(result.points || 0)}</td>
                </tr>
              `).join("") : '<tr><td colspan="4" class="empty-row">Sem resultados cadastrados.</td></tr>'}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  `;
}

function renderTeams() {
  setHero("Garagens", "Equipes", "Emblemas, cores, pilotos e dados de base");
  const aside = isAdmin() ? actionLink("/admin/equipes", "Nova equipe", "primary") : "";
  return `
    ${sectionHead("Equipes", "Construtores", aside)}
    <div class="team-grid">${state.teams.map(teamCard).join("") || emptyState("Sem equipes", "Cadastre equipes no admin.")}</div>
  `;
}

function renderTeamDetail(teamId) {
  const team = byId(state.teams, teamId);
  if (!team) {
    setHero("Equipe", "Equipe nao encontrada");
    return emptyState("Nao encontrada", "Essa equipe nao existe no banco local.");
  }

  const teamDrivers = state.drivers.filter((driver) => Number(driver.teamId) === Number(team.id));
  setHero(team.shortName || team.name, team.name, team.fullName || "");
  return `
    ${sectionHead("Equipe", team.name, actionLink("/equipes", "Voltar para equipes"))}
    <div class="split-layout">
      ${teamCard(team)}
      <div>
        <h3 class="inline-title">Pilotos da equipe</h3>
        <div class="driver-grid compact-grid">${teamDrivers.map(driverCard).join("") || emptyState("Sem pilotos", "Nenhum piloto vinculado.")}</div>
      </div>
    </div>
  `;
}

function renderStandingsOverview() {
  setHero("Pontos", "Classificacao", "Pilotos e equipes separados");
  return `
    ${sectionHead("Classificacao", "Tabelas do campeonato")}
    <div class="standings-layout">
      <div class="table-panel">
        <h3>Pilotos</h3>
        ${standingsTable(state.standings.drivers || [], "drivers")}
        <div class="panel-actions">${actionLink("/classificacao/pilotos", "Pagina de pilotos", "primary")}</div>
      </div>
      <div class="table-panel">
        <h3>Equipes</h3>
        ${standingsTable(state.standings.teams || [], "teams")}
        <div class="panel-actions">${actionLink("/classificacao/equipes", "Pagina de equipes", "primary")}</div>
      </div>
    </div>
  `;
}

function renderDriverStandingsPage() {
  setHero("Pilotos", "Classificacao de pilotos");
  return `${sectionHead("Classificacao", "Pilotos", actionLink("/classificacao", "Voltar"))}<div class="table-panel">${standingsTable(state.standings.drivers || [], "drivers")}</div>`;
}

function renderTeamStandingsPage() {
  setHero("Equipes", "Classificacao de equipes");
  return `${sectionHead("Classificacao", "Equipes", actionLink("/classificacao", "Voltar"))}<div class="table-panel">${standingsTable(state.standings.teams || [], "teams")}</div>`;
}

function predictionOpenSessions() {
  return state.events.flatMap((event) =>
    event.sessions
      .filter((session) => session.pointsSession && !session.results.length)
      .map((session) => ({ event, session }))
  );
}

function selectedPredictionTarget() {
  const open = predictionOpenSessions();
  if (!open.length) return null;

  let target = open.find(
    (item) =>
      Number(item.event.id) === Number(state.selectedPredictionEventId) &&
      item.session.type === state.selectedPredictionSession
  );

  if (!target) {
    target = open.find((item) => Number(item.event.id) === Number(state.selectedPredictionEventId)) || open[0];
    state.selectedPredictionEventId = target.event.id;
    state.selectedPredictionSession = target.session.type;
  }

  return target;
}

function renderPredictions() {
  setHero("Previsoes", "Monte seu grid", "Acertou piloto e posicao, ganhou os pontos reais daquele resultado");
  if (!state.currentUser) {
    return emptyState("Entre para jogar", "Crie uma conta ou faca login para salvar previsoes.", actionLink("/login", "Entrar", "primary"));
  }

  const open = predictionOpenSessions();
  const target = selectedPredictionTarget();
  if (!open.length || !target) {
    return `${sectionHead("Previsoes", "Sem sessoes abertas")}${emptyState("Nada aberto agora", "As corridas com resultado cadastrado ficam bloqueadas para evitar previsao atrasada.")}`;
  }

  const eventOptions = [...new Map(open.map((item) => [item.event.id, item.event])).values()]
    .map((event) => `<option value="${escapeHtml(event.id)}" ${Number(event.id) === Number(target.event.id) ? "selected" : ""}>${String(event.round).padStart(2, "0")} - ${escapeHtml(event.name)}</option>`)
    .join("");
  const sessionOptions = open
    .filter((item) => Number(item.event.id) === Number(target.event.id))
    .map((item) => `<option value="${escapeHtml(item.session.type)}" ${item.session.type === target.session.type ? "selected" : ""}>${escapeHtml(item.session.label)}</option>`)
    .join("");

  return `
    ${sectionHead("Previsoes", "Enviar palpite", actionLink("/minhas-previsoes", "Minhas previsoes"))}
    <div class="prediction-layout">
      <form class="admin-panel prediction-panel" id="prediction-form">
        <div class="form-grid">
          <label>Etapa<select id="prediction-event-select" name="eventId">${eventOptions}</select></label>
          <label>Sessao<select id="prediction-session-select" name="sessionType">${sessionOptions}</select></label>
        </div>
        <div class="prediction-grid">
          ${Array.from({ length: Math.min(10, state.drivers.length) }, (_, index) => {
            const position = index + 1;
            return `
              <label class="prediction-row">
                <span class="driver-number" style="--team-color:#e10600">${position}</span>
                <select name="driverId-${position}" required>${driverOptions()}</select>
              </label>
            `;
          }).join("")}
        </div>
        <button type="submit">Salvar previsao</button>
        <div class="admin-status" id="prediction-status"></div>
      </form>
      <aside class="route-card prediction-help">
        <span class="round-number mini">Round ${escapeHtml(target.event.round)}</span>
        <h3>${escapeHtml(target.event.name)}</h3>
        <p>${escapeHtml(target.session.label)} em ${formatDate(target.event.date)}. Depois que o admin cadastrar esse resultado, sua pontuacao aparece automaticamente.</p>
      </aside>
    </div>
  `;
}

function predictionCard(prediction) {
  const score = prediction.score || {};
  return `
    <article class="route-card prediction-card">
      <div class="event-meta compact">
        <span>${escapeHtml(prediction.event?.name || "Etapa")}</span>
        <span>${escapeHtml(prediction.sessionLabel)}</span>
        <span>${score.evaluated ? `${score.points} pts` : "Aguardando"}</span>
      </div>
      <div class="table-scroll">
        <table>
          <thead><tr><th>Pos</th><th>Piloto</th></tr></thead>
          <tbody>
            ${prediction.picks.map((pick) => `
              <tr>
                <td class="position-cell">${escapeHtml(pick.position)}</td>
                <td>${driverToken(pick.driver)}</td>
              </tr>
            `).join("")}
          </tbody>
        </table>
      </div>
    </article>
  `;
}

function renderMyPredictions() {
  setHero("Previsoes", "Minhas previsoes", "Historico e pontuacao calculada pelo backend");
  if (!state.currentUser) {
    return emptyState("Entre para ver suas previsoes", "Suas previsoes ficam vinculadas a conta.", actionLink("/login", "Entrar", "primary"));
  }

  return `
    ${sectionHead("Conta", "Minhas previsoes", actionLink("/previsoes", "Nova previsao", "primary"))}
    <div class="route-grid">${state.myPredictions.map(predictionCard).join("") || emptyState("Sem previsoes", "Crie sua primeira previsao para uma corrida futura.")}</div>
  `;
}

function renderUserLeaderboard() {
  setHero("Ranking", "Usuarios", "Pontuacao das previsoes ja avaliadas");
  const rows = state.leaderboard.length
    ? state.leaderboard.map((row, index) => `
      <tr>
        <td class="position-cell">${index + 1}</td>
        <td>
          <strong>${escapeHtml(row.user.name)}</strong>
          <small>${escapeHtml(row.user.role === "admin" ? "Admin" : "Usuario")}</small>
        </td>
        <td class="points-cell">${escapeHtml(row.points || 0)}</td>
        <td>${escapeHtml(row.correctPicks || 0)}</td>
        <td>${escapeHtml(row.evaluatedCount || 0)}/${escapeHtml(row.predictionsCount || 0)}</td>
      </tr>
    `).join("")
    : '<tr><td colspan="5" class="empty-row">Ainda nao ha previsoes pontuadas.</td></tr>';

  return `
    ${sectionHead("Ranking", "Liga de usuarios", actionLink("/previsoes", "Criar previsao", "primary"))}
    <div class="table-panel">
      <h3>Classificacao das previsoes</h3>
      <div class="table-scroll">
        <table>
          <thead><tr><th>#</th><th>Usuario</th><th>Pts</th><th>Acertos</th><th>Avaliadas</th></tr></thead>
          <tbody>${rows}</tbody>
        </table>
      </div>
    </div>
  `;
}

function adminSessionPanel() {
  return `
    <div class="admin-card admin-session">
      <strong>Admin conectado</strong>
      <span>${escapeHtml(state.currentUser?.email || "")}</span>
      <div class="admin-status" id="admin-status"></div>
    </div>
  `;
}

function adminNav() {
  return `
    <div class="route-grid admin-routes">
      ${actionLink("/admin/equipes", "Cadastrar equipes", "primary")}
      ${actionLink("/admin/pilotos", "Cadastrar pilotos", "primary")}
      ${actionLink("/admin/etapas", "Cadastrar etapas", "primary")}
      ${actionLink("/admin/resultados", "Cadastrar resultados", "primary")}
    </div>
  `;
}

function renderAdminHome() {
  setHero("Admin", "Painel de controle", "Cadastros integrados ao proprio site");
  const gate = adminGate();
  if (gate) return gate;
  return `
    ${sectionHead("Admin", "Escolha uma area", actionLink("/mapa", "Ver rotas"))}
    ${adminSessionPanel()}
    ${adminNav()}
  `;
}

function renderAdminTeams() {
  setHero("Admin", "Cadastrar equipe");
  const gate = adminGate();
  if (gate) return gate;
  return `
    ${sectionHead("Admin", "Equipe", actionLink("/admin", "Voltar"))}
    ${adminSessionPanel()}
    <form class="admin-panel narrow-panel" id="team-form">
      <div class="form-grid">
        <label>Nome<input name="name" required /></label>
        <label>Nome curto<input name="shortName" /></label>
        <label>Nome completo<input name="fullName" /></label>
        <label>Base<input name="base" /></label>
        <label>Pais<input name="country" /></label>
        <label>Motor<input name="powerUnit" /></label>
        <label>Chefe<input name="chief" /></label>
        <label>Cor<input name="color" type="color" value="#e10600" /></label>
        <label class="full-field">URL do emblema<input name="emblemUrl" type="url" placeholder="https://..." /></label>
      </div>
      <button type="submit">Cadastrar equipe</button>
    </form>
  `;
}

function renderAdminDrivers() {
  setHero("Admin", "Cadastrar piloto");
  const gate = adminGate();
  if (gate) return gate;
  return `
    ${sectionHead("Admin", "Piloto", actionLink("/admin", "Voltar"))}
    ${adminSessionPanel()}
    <form class="admin-panel narrow-panel" id="driver-form">
      <div class="form-grid">
        <label>Nome<input name="name" required /></label>
        <label>Codigo<input name="code" maxlength="4" /></label>
        <label>Numero<input name="number" type="number" min="1" required /></label>
        <label>Equipe<select name="teamId" required>${teamOptions()}</select></label>
        <label>Pais<input name="country" /></label>
        <label class="checkbox-field"><input name="active" type="checkbox" checked /> Ativo</label>
        <label class="full-field">URL da foto<input name="photoUrl" type="url" placeholder="https://..." /></label>
      </div>
      <button type="submit">Cadastrar piloto</button>
    </form>
  `;
}

function renderAdminEvents() {
  setHero("Admin", "Cadastrar etapa");
  const gate = adminGate();
  if (gate) return gate;
  return `
    ${sectionHead("Admin", "Etapa", actionLink("/admin", "Voltar"))}
    ${adminSessionPanel()}
    <form class="admin-panel narrow-panel" id="event-form">
      <div class="form-grid">
        <label>Numero<input name="round" type="number" min="1" required /></label>
        <label>Nome<input name="name" required /></label>
        <label>Circuito<input name="circuit" /></label>
        <label>Cidade<input name="city" /></label>
        <label>Pais<input name="country" /></label>
        <label>Data<input name="date" type="date" /></label>
        <label>TLs<select name="practiceSessionsCount"><option>1</option><option>2</option><option selected>3</option></select></label>
        <label>Qualis<select name="qualifyingSessionsCount"><option>1</option><option>2</option><option selected>3</option></select></label>
        <label class="checkbox-field"><input name="hasSprint" type="checkbox" /> Sprint</label>
        <label class="full-field">Notas<input name="notes" /></label>
      </div>
      <button type="submit">Cadastrar etapa</button>
    </form>
  `;
}

function renderAdminResults() {
  setHero("Admin", "Cadastrar resultado");
  const gate = adminGate();
  if (gate) return gate;
  const eventOptions = state.events.map((event) => `<option value="${escapeHtml(event.id)}">${String(event.round).padStart(2, "0")} - ${escapeHtml(event.name)}</option>`).join("");
  const firstEvent = state.events[0];
  const sessionOptions = firstEvent ? firstEvent.sessions.map((session) => `<option value="${escapeHtml(session.type)}">${escapeHtml(session.label)}</option>`).join("") : "";
  return `
    ${sectionHead("Admin", "Resultado", actionLink("/admin", "Voltar"))}
    ${adminSessionPanel()}
    <form class="admin-panel narrow-panel" id="result-form">
      <div class="form-grid">
        <label>Etapa<select name="eventId" id="result-event-select" required>${eventOptions}</select></label>
        <label>Sessao<select name="sessionType" id="result-session-select" required>${sessionOptions}</select></label>
        <label>Piloto<select name="driverId" required>${driverOptions()}</select></label>
        <label>Posicao<input name="position" type="number" min="1" /></label>
        <label>Tempo<input name="time" placeholder="1:32.608" /></label>
        <label>Gap<input name="gap" placeholder="+0.241" /></label>
        <label>Voltas<input name="laps" /></label>
        <label>Status<select name="status">${state.statuses.map((status) => `<option value="${escapeHtml(status.value)}">${escapeHtml(status.label)}</option>`).join("")}</select></label>
        <label class="full-field">Notas<input name="notes" /></label>
      </div>
      <button type="submit">Salvar resultado</button>
    </form>
  `;
}

function renderSitemap() {
  setHero("Mapa", `${declaredPages.length} paginas/rotas`, "Estrutura navegavel por area");
  const firstEvent = state.events[0];
  const firstDriver = state.drivers[0];
  const firstTeam = state.teams[0];
  return `
    ${sectionHead("Rotas", "Mapa navegavel")}
    <div class="route-grid">
      ${declaredPages.map(([path, label]) => {
        const href = path
          .replace(":id", firstEvent?.id || firstDriver?.id || firstTeam?.id || "1");
        const resolvedHref = path.startsWith("/pilotos/:id") ? `/pilotos/${firstDriver?.id || 1}`
          : path.startsWith("/equipes/:id") ? `/equipes/${firstTeam?.id || 1}`
          : path.startsWith("/etapas/:id") ? path.replace(":id", firstEvent?.id || 1)
          : href;
        const adminTag = path.startsWith("/admin") ? `<span class="admin-route-tag">Admin</span>` : "";
        return `<article class="route-card"><code>${escapeHtml(path)}</code><h3>${escapeHtml(label)}</h3>${adminTag}${actionLink(resolvedHref, "Abrir")}</article>`;
      }).join("")}
    </div>
  `;
}

function teamOptions(selectedId = "") {
  return `<option value="">Equipe</option>${state.teams.map((team) => `<option value="${escapeHtml(team.id)}" ${Number(selectedId) === Number(team.id) ? "selected" : ""}>${escapeHtml(team.name)}</option>`).join("")}`;
}

function driverOptions(selectedId = "") {
  return `<option value="">Piloto</option>${state.drivers.map((driver) => `<option value="${escapeHtml(driver.id)}" ${Number(selectedId) === Number(driver.id) ? "selected" : ""}>${escapeHtml(driver.number)} - ${escapeHtml(driver.name)}</option>`).join("")}`;
}

function formPayload(form) {
  return Object.fromEntries(new FormData(form).entries());
}

function setStatus(selector, message, variant = "ok") {
  const status = document.querySelector(selector);
  if (!status) return;
  status.textContent = message;
  status.dataset.variant = variant;
}

function setAdminStatus(message, variant = "ok") {
  setStatus("#admin-status", message, variant);
}

async function submitAdminForm(form, path, transform = (payload) => payload) {
  const payload = transform(formPayload(form));
  await apiFetch(path, {
    method: "POST",
    body: JSON.stringify(payload),
  });
  form.reset();
  await loadData(false);
}

function navigate(path) {
  history.pushState({}, "", path);
  renderRoute();
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function bindAuthEvents() {
  document.querySelector("#login-form")?.addEventListener("submit", async (event) => {
    event.preventDefault();
    try {
      const payload = formPayload(event.currentTarget);
      const result = await apiFetch("/auth/login", {
        method: "POST",
        body: JSON.stringify(payload),
      });
      setToken(result.token);
      state.currentUser = result.user;
      await loadData(false);
      navigate("/");
    } catch (error) {
      setStatus("#auth-status", error.message, "error");
    }
  });

  document.querySelector("#register-form")?.addEventListener("submit", async (event) => {
    event.preventDefault();
    try {
      const payload = formPayload(event.currentTarget);
      const result = await apiFetch("/auth/register", {
        method: "POST",
        body: JSON.stringify(payload),
      });
      setToken(result.token);
      state.currentUser = result.user;
      await loadData(false);
      navigate("/previsoes");
    } catch (error) {
      setStatus("#auth-status", error.message, "error");
    }
  });

  document.querySelector("#logout-button")?.addEventListener("click", async () => {
    try {
      await apiFetch("/auth/logout", { method: "POST", body: "{}" });
    } catch {
      // The local session should still be cleared if the token expired.
    }
    setToken("");
    state.currentUser = null;
    state.myPredictions = [];
    await loadData(false);
    renderRoute();
  });
}

function bindPredictionEvents() {
  const eventSelect = document.querySelector("#prediction-event-select");
  eventSelect?.addEventListener("change", () => {
    state.selectedPredictionEventId = eventSelect.value;
    state.selectedPredictionSession = "RACE";
    renderRoute();
  });

  const sessionSelect = document.querySelector("#prediction-session-select");
  sessionSelect?.addEventListener("change", () => {
    state.selectedPredictionSession = sessionSelect.value;
    renderRoute();
  });

  document.querySelector("#prediction-form")?.addEventListener("submit", async (event) => {
    event.preventDefault();
    const form = event.currentTarget;
    const payload = formPayload(form);
    const picks = Array.from({ length: 10 }, (_, index) => {
      const position = index + 1;
      return {
        position,
        driverId: payload[`driverId-${position}`],
      };
    }).filter((pick) => pick.driverId);

    try {
      await apiFetch("/predictions", {
        method: "POST",
        body: JSON.stringify({
          eventId: payload.eventId,
          sessionType: payload.sessionType,
          picks,
        }),
      });
      setStatus("#prediction-status", "Previsao salva.", "ok");
      await loadData(false);
      renderRoute();
    } catch (error) {
      setStatus("#prediction-status", error.message, "error");
    }
  });
}

function bindAdminEvents() {
  document.querySelector("#team-form")?.addEventListener("submit", async (event) => {
    event.preventDefault();
    try {
      await submitAdminForm(event.currentTarget, "/teams");
      setAdminStatus("Equipe cadastrada.", "ok");
    } catch (error) {
      setAdminStatus(error.message, "error");
    }
  });

  document.querySelector("#driver-form")?.addEventListener("submit", async (event) => {
    event.preventDefault();
    try {
      await submitAdminForm(event.currentTarget, "/drivers", (payload) => ({
        ...payload,
        active: event.currentTarget.elements.active.checked,
      }));
      setAdminStatus("Piloto cadastrado.", "ok");
    } catch (error) {
      setAdminStatus(error.message, "error");
    }
  });

  document.querySelector("#event-form")?.addEventListener("submit", async (event) => {
    event.preventDefault();
    try {
      await submitAdminForm(event.currentTarget, "/events", (payload) => ({
        ...payload,
        hasSprint: event.currentTarget.elements.hasSprint.checked,
      }));
      setAdminStatus("Etapa cadastrada.", "ok");
    } catch (error) {
      setAdminStatus(error.message, "error");
    }
  });

  const eventSelect = document.querySelector("#result-event-select");
  eventSelect?.addEventListener("change", () => {
    const selectedEvent = byId(state.events, eventSelect.value);
    const sessionSelect = document.querySelector("#result-session-select");
    sessionSelect.innerHTML = selectedEvent
      ? selectedEvent.sessions.map((session) => `<option value="${escapeHtml(session.type)}">${escapeHtml(session.label)}</option>`).join("")
      : "";
  });

  document.querySelector("#result-form")?.addEventListener("submit", async (event) => {
    event.preventDefault();
    try {
      await submitAdminForm(event.currentTarget, "/results");
      setAdminStatus("Resultado salvo.", "ok");
    } catch (error) {
      setAdminStatus(error.message, "error");
    }
  });
}

function bindPageEvents() {
  bindAuthEvents();
  bindPredictionEvents();
  bindAdminEvents();
}

function updateActiveNav() {
  const path = window.location.pathname;
  elements.navLinks.forEach((link) => {
    const href = link.getAttribute("href");
    link.classList.toggle("active", href !== "/" ? path.startsWith(href) : path === "/");
  });
}

function matchRoute(path) {
  for (const route of routes) {
    const match = path.match(route.pattern);
    if (match) {
      return { route, params: match.slice(1) };
    }
  }
  return null;
}

function renderRoute() {
  const path = window.location.pathname;
  const match = matchRoute(path);
  updateAuthNav();
  updateActiveNav();

  if (!match) {
    setHero("404", "Pagina nao encontrada");
    elements.pageRoot.innerHTML = `${sectionHead("Erro", "Rota inexistente", actionLink("/mapa", "Ver mapa"))}${emptyState("Nao achei essa pagina", "Use o mapa para navegar pelas rotas disponiveis.")}`;
    return;
  }

  document.title = `${match.route.name} - F1 Results Hub`;
  elements.pageRoot.innerHTML = match.route.render(match.params);
  bindPageEvents();
}

async function loadData(shouldRender = true) {
  const [snapshot, standings, meta, leaderboard] = await Promise.all([
    apiFetch("/snapshot"),
    apiFetch("/standings"),
    apiFetch("/meta"),
    apiFetch("/predictions/leaderboard"),
  ]);

  state.teams = snapshot.teams || [];
  state.drivers = snapshot.drivers || [];
  state.events = snapshot.events || [];
  state.standings = standings.standings || { drivers: [], teams: [] };
  state.statuses = meta.statuses || state.statuses;
  state.adminEmail = meta.auth?.adminEmail || "";
  state.leaderboard = leaderboard.leaderboard || [];

  if (state.token) {
    try {
      const session = await apiFetch("/auth/me");
      state.currentUser = session.user || null;
      if (!state.currentUser) {
        setToken("");
        state.myPredictions = [];
      } else {
        const predictions = await apiFetch("/predictions/me");
        state.myPredictions = predictions.predictions || [];
      }
    } catch {
      setToken("");
      state.currentUser = null;
      state.myPredictions = [];
    }
  } else {
    state.currentUser = null;
    state.myPredictions = [];
  }

  renderSummary();
  updateAuthNav();
  if (shouldRender) renderRoute();
}

document.addEventListener("click", (event) => {
  const link = event.target.closest("a[data-route]");
  if (!link) return;

  const url = new URL(link.href);
  if (url.origin !== window.location.origin) return;

  event.preventDefault();
  history.pushState({}, "", url.pathname + url.search);
  renderRoute();
  window.scrollTo({ top: 0, behavior: "smooth" });
});

window.addEventListener("popstate", renderRoute);

loadData().catch((error) => {
  setHero("API", "API indisponivel");
  elements.pageRoot.innerHTML = emptyState("Nao consegui conectar", error.message);
});
