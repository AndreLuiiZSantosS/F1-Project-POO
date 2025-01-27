import json

# Caminho do banco de dados de pilotos e resultados
CAMINHO_BD_PILOTOS = "data/pilotos.json"
CAMINHO_BD_RESULTADOS = "data/resultados.json"

def carregar_dados(caminho):
    """Carrega dados de um arquivo JSON."""
    try:
        with open(caminho, "r") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print(f"Erro ao carregar o arquivo {caminho}.")
        return []

def exibir_estatisticas_pilotos():
    """Exibe o ranking dos pilotos com base nos resultados."""
    pilotos = carregar_dados(CAMINHO_BD_PILOTOS)
    resultados = carregar_dados(CAMINHO_BD_RESULTADOS)

    pontuacao_pilotos = {piloto["nome"]: 0 for piloto in pilotos}

    for resultado in resultados:
        pontos = calcular_pontos(int(resultado["posicao"]))
        pontuacao_pilotos[resultado["piloto"]] += pontos

    ranking = sorted(pontuacao_pilotos.items(), key=lambda x: x[1], reverse=True)

    if not ranking:
        print("\nNenhum piloto registrado no campeonato.")
    else:
        print("\n✓ Ranking de Pilotos:")
        for idx, (piloto, pontos) in enumerate(ranking, 1):
            print(f"{idx}. {piloto} - {pontos} pontos")

    print("\n1. Voltar")
    while input("Selecione uma opção: ") != "1":
        print("Opção inválida. Tente novamente.")

def exibir_estatisticas_construtores():
    """Exibe o ranking das equipes com base nos resultados."""
    pilotos = carregar_dados(CAMINHO_BD_PILOTOS)
    resultados = carregar_dados(CAMINHO_BD_RESULTADOS)

    equipe_pontos = {}
    for piloto in pilotos:
        equipe_pontos.setdefault(piloto["equipe"], 0)

    for resultado in resultados:
        pontos = calcular_pontos(int(resultado["posicao"]))
        equipe = next(p["equipe"] for p in pilotos if p["nome"] == resultado["piloto"])
        equipe_pontos[equipe] += pontos

    ranking = sorted(equipe_pontos.items(), key=lambda x: x[1], reverse=True)

    if not ranking:
        print("\nNenhuma equipe registrada no campeonato.")
    else:
        print("\n✓ Ranking de Construtores:")
        for idx, (equipe, pontos) in enumerate(ranking, 1):
            print(f"{idx}. {equipe} - {pontos} pontos")

    print("\n1. Voltar")
    while input("Selecione uma opção: ") != "1":
        print("Opção inválida. Tente novamente.")

def menu_estatisticas():
    """Exibe o menu de estatísticas do campeonato."""
    while True:
        print("\n✓ Estatísticas do Campeonato")
        print("1. Visualizar Campeonato de Pilotos")
        print("2. Visualizar Campeonato de Construtores")
        print("3. Voltar")

        opcao = input("Selecione uma opção: ")

        if opcao == "1":
            exibir_estatisticas_pilotos()
        elif opcao == "2":
            exibir_estatisticas_construtores()
        elif opcao == "3":
            return
        else:
            print("Opção inválida. Tente novamente.")

def calcular_pontos(posicao):
    """Calcula pontos com base na posição do piloto."""
    tabela_pontos = {
        1: 25,
        2: 18,
        3: 15,
        4: 12,
        5: 10,
        6: 8,
        7: 6,
        8: 4,
        9: 2,
        10: 1
    }
    return tabela_pontos.get(posicao, 0)
