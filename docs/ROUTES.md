# Rotas do frontend

O frontend usa um shell leve com roteamento por URL. Cada endereco abaixo renderiza uma pagina propria, com navegacao sem recarregar a aplicacao inteira.

## Publicas

- `/`
- `/login`
- `/registro`
- `/resultados`
- `/etapas`
- `/etapas/:id`
- `/etapas/:id/tl1`
- `/etapas/:id/tl2`
- `/etapas/:id/tl3`
- `/etapas/:id/q1`
- `/etapas/:id/q2`
- `/etapas/:id/q3`
- `/etapas/:id/sprint-quali`
- `/etapas/:id/sprint`
- `/etapas/:id/corrida`
- `/pilotos`
- `/pilotos/:id`
- `/equipes`
- `/equipes/:id`
- `/classificacao`
- `/classificacao/pilotos`
- `/classificacao/equipes`
- `/ranking-usuarios`
- `/mapa`

## Logadas

- `/previsoes`
- `/minhas-previsoes`

## Admin

As rotas existem no frontend, mas o conteudo fica bloqueado para usuario comum. A API tambem exige token de admin para escrita.

- `/admin`
- `/admin/equipes`
- `/admin/pilotos`
- `/admin/etapas`
- `/admin/resultados`
