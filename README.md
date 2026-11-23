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

Requisitos: Node.js 20.19 ou superior.

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

Antes de iniciar, configure `ADMIN_EMAIL` e `ADMIN_PASSWORD` no ambiente. Veja [Configuracao do administrador](#configuracao-do-administrador).

## Configuracao do administrador

A API nao possui credenciais padrao. Defina `ADMIN_EMAIL` e `ADMIN_PASSWORD` no ambiente antes de iniciar a API ou gerar os dados iniciais:

```powershell
$env:ADMIN_EMAIL = "<email-do-administrador>"
$env:ADMIN_PASSWORD = "<segredo-forte>"
node scripts/seed-2026.js
node api/src/server.js
```

O seed nao imprime a senha. Guarde os valores em um gerenciador de segredos e nao os versione.

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

O projeto usa ESLint com as regras recomendadas e verificacoes de estilo inspiradas no StandardJS, adaptadas ao uso existente de aspas duplas e ponto e virgula.

```powershell
npm --prefix api run lint
npm --prefix api run code-smells
npm --prefix api run duplicates
npm --prefix api test
npm --prefix api run deps:check
```

O ESLint e o jscpd verificam o codigo em cada push e pull request.
O jscpd fica na versao 4.x porque a versao 5.x requer glibc 2.32 ou superior, ausente no container Debian 11 do projeto.
O comando `code-smells` usa regras SonarJS para detectar complexidade cognitiva, condicionais aninhadas/colapsaveis e literais duplicados.

## Diagrama UML de classes

O diagrama das entidades de dominio da API esta em [`docs/diagrams/domain-classes.mmd`](docs/diagrams/domain-classes.mmd). A imagem e gerada no pipeline e publicada como artefato `diagrama-uml` em cada execucao do GitHub Actions; ela nao e versionada no repositorio. Abra a execucao na aba Actions para baixar o artefato. Para gerar a imagem localmente:

```powershell
npm --prefix api run diagram
```

O pipeline tambem executa esse comando a cada push e pull request.

## Analise estatica de seguranca

O pipeline instala o Semgrep CLI e executa as regras comunitarias de auditoria de seguranca/segredos e as regras locais em `.semgrep.yml`. A verificacao bloqueia achados de severidade `ERROR`, incluindo fallback de credenciais administrativas, bypass de autenticacao por credencial fixa e registro de senha em logs.

Para executar localmente:

```powershell
python -m pip install --only-binary=:all: semgrep==1.186.0
$semgrepScripts = python -c "import sysconfig; print(sysconfig.get_path('scripts', 'nt_user'))"
$env:PATH = "$semgrepScripts;$env:PATH"
semgrep scan --config p/security-audit --config p/secrets --config .semgrep.yml --severity ERROR --error .
```

Para atualizar dependencias npm dentro da faixa suportada pelo Node do projeto:

```powershell
npm --prefix api run deps:update
```
