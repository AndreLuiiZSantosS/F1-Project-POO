class Estatistica: # ... (outros métodos existentes)

@staticmethod
def calcular_pontos(resultado):
    """Calcula pontos considerando DNFs"""
    if resultado.get("dnf", False):
        return 0
    return Estatistica.tabela_pontos().get(resultado["posicao"], 0)

@staticmethod
def tabela_pontos():
    return {
        1: 25, 2: 18, 3: 15, 4: 12, 5: 10,
        6: 8, 7: 6, 8: 4, 9: 2, 10: 1
    }

@staticmethod
def exibir_estatisticas_pilotos():
    """Calcula pontos considerando TODOS os pilotos, incluindo reservas"""
    pilotos = {p["nome"]: p for p in Estatistica.carregar_dados(Estatistica.CAMINHO_BD_PILOTOS)["pilotos"]}
    resultados = Estatistica.carregar_dados(Estatistica.CAMINHO_BD_RESULTADOS)["resultados"]
    
    pontuacao = {}
    for res in resultados:
        pontos = Estatistica.calcular_pontos(res)
        if res["piloto"] in pilotos:
            pontuacao[res["piloto"]] = pontuacao.get(res["piloto"], 0) + pontos
    
    # Ordenar por pontos (decrescente) e vitórias (desempate)
    ranking = sorted(pontuacao.items(), 
                     key=lambda x: (-x[1], -sum(1 for r in resultados if r["piloto"] == x[0] and r["posicao"] == 1)))
    
    for i, (piloto, pontos) in enumerate(ranking, start=1):
        print(f"{i}. {piloto}: {pontos} pontos")

@staticmethod
def exibir_estatisticas_construtores():
    """Calcula pontos somando TODOS os pilotos de cada equipe"""
    pilotos = Estatistica.carregar_dados(Estatistica.CAMINHO_BD_PILOTOS)["pilotos"]
    mapa_equipes = {p["nome"]: p["equipe"] for p in pilotos}
    resultados = Estatistica.carregar_dados(Estatistica.CAMINHO_BD_RESULTADOS)["resultados"]
    
    pontuacao = {}
    for res in resultados:
        equipe = mapa_equipes.get(res["piloto"], "Desconhecida")
        pontos = Estatistica.calcular_pontos(res)
        pontuacao[equipe] = pontuacao.get(equipe, 0) + pontos
    
    # Ordenar equipes por pontos (maior primeiro)
    ranking_equipes = sorted(pontuacao.items(), key=lambda x: -x[1])
    
    for i, (equipe, pontos) in enumerate(ranking_equipes, start=1):
        print(f"{i}. {equipe}: {pontos} pontos")

class MenuEstatisticas: """Menu para exibição de estatísticas do campeonato."""

@staticmethod
def exibir():
    """Exibe o menu de estatísticas do campeonato."""
    while True:
        print("\n✓ Estatísticas do Campeonato")
        print("1. Visualizar Campeonato de Pilotos")
        print("2. Visualizar Campeonato de Construtores")
        print("3. Voltar")

        opcao = input("Selecione uma opção: ")

        if opcao == "1":
            Estatistica.exibir_estatisticas_pilotos()
        elif opcao == "2":
            Estatistica.exibir_estatisticas_construtores()
        elif opcao == "3":
            return
        else:
            print("Opção inválida. Tente novamente.")

