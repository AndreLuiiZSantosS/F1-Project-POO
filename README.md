# F1 Results Hub

Projeto for-fun para cadastrar resultados reais de F1, consultar grid/calendario/classificacao e jogar previsoes no estilo Cartola.

## Estrutura ativa

- `api/`: backend Node puro, API HTTP, autenticacao e banco JSON local.
- `frontend/`: frontend estatico com rotas por URL e visual inspirado em F1.
- `shared/`: regras comuns de sessoes e pontuacao.
- `scripts/`: seed do banco com dados 2026.
- `docs/`: notas de arquitetura.
- `start-app.bat`: atalho para abrir API, frontend e navegador.

As pastas antigas `backend/` e `F1_project/` ficaram como legado da tentativa anterior. A aplicacao nova roda por `api/` + `frontend/`.

## Rodar

Requisitos: Node.js 20 ou superior.

Com duplo clique:

```text
start-app.bat
```

Ou manualmente, em dois terminais:

```powershell
node api/src/server.js
node frontend/server.js
```

Depois abra:

- Frontend: `http://127.0.0.1:5173`
- API: `http://127.0.0.1:8000/api/health`

## Login admin

Credenciais padrao locais:

- Email: `admin@f1.local`
- Senha: `admin-f1-2026`

Para trocar:

```powershell
$env:ADMIN_EMAIL="seu-email@exemplo.com"
$env:ADMIN_PASSWORD="sua-senha"
node scripts/seed-2026.js
node api/src/server.js
```

Usuario comum pode criar conta em `/registro`, ver resultados e criar previsoes. Apenas admin ve e usa as rotas de cadastro.

## Dados

O seed atual (`node scripts/seed-2026.js`) recria o banco com:

- 11 equipes e 23 pilotos do grid/entradas de 2026;
- 23 etapas do calendario 2026;
- resultados reais de corrida e sprint ate o Dutch GP de 23/08/2026;
- URLs dinamicas de fotos dos pilotos e emblemas das equipes via CDN oficial da F1;
- admin local sem previsoes ou tokens ativos.

## Pontuacao

- corrida: 25, 18, 15, 12, 10, 8, 6, 4, 2, 1;
- sprint: 8, 7, 6, 5, 4, 3, 2, 1;
- treinos e qualificacoes: 0.

Nas previsoes, o usuario pontua quando acerta piloto e posicao final. Os pontos recebidos sao os mesmos pontos reais do piloto naquela sessao.

## Testes

```powershell
node --test api/tests/*.test.js
```
