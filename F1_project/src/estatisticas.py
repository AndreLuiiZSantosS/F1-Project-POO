def exibir_estatisticas_pilotos(dados):
    """Exibe o ranking dos pilotos com base nos resultados."""
    pilotos = dados.get("pilotos", [])
    resultados = dados.get("resultados", [])
    
    pontuacao_pilotos = {}
    
    for piloto in pilotos:
        pontuacao_pilotos[piloto["nome"]] = 0
    
    for resultado in resultados:
        pontos = calcular_pontos(int(resultado["posicao"]))
        pontuacao_pilotos[resultado["piloto"]] += pontos
    
    ranking = sorted(pontuacao_pilotos.items(), key=lambda x: x[1], reverse=True)
    print("\n✓ Ranking de Pilotos:")
    for idx, (piloto, pontos) in enumerate(ranking, 1):
        print(f"{idx}. {piloto} - {pontos} pontos")

def exibir_estatisticas_construtores(dados):
    """Exibe o ranking das equipes com base nos resultados."""
    pilotos = dados.get("pilotos", [])
    resultados = dados.get("resultados", [])
    
    equipe_pontos = {}
    
    for piloto in pilotos:
        equipe = piloto["equipe"]
        if equipe not in equipe_pontos:
            equipe_pontos[equipe] = 0
    
    for resultado in resultados:
        pontos = calcular_pontos(int(resultado["posicao"]))
        equipe = next(p["equipe"] for p in pilotos if p["nome"] == resultado["piloto"])
        equipe_pontos[equipe] += pontos
    
    ranking = sorted(equipe_pontos.items(), key=lambda x: x[1], reverse=True)
    print("\n✓ Ranking de Construtores:")
    for idx, (equipe, pontos) in enumerate(ranking, 1):
        print(f"{idx}. {equipe} - {pontos} pontos")

def menu_estatisticas(dados):
    """Menu de visualização das estatísticas do campeonato."""
    while True:
        print("\n✓ Estatísticas do Campeonato")
        print("1. Ranking de Pilotos")
        print("2. Ranking de Construtores")
        print("3. Voltar")
        opcao = input("Selecione uma opção: ")

        if opcao == "1":
            exibir_estatisticas_pilotos(dados)
        elif opcao == "2":
            exibir_estatisticas_construtores(dados)
        elif opcao == "3":
            break
        else:
            print("Opção inválida. Tente novamente.")

def menu_admin_estatisticas(dados):
    """Menu administrativo para editar estatísticas."""
    while True:
        print("\n✓ Editar Estatísticas")
        print("1. Adicionar resultado do campeonato de pilotos")
        print("2. Adicionar resultado do campeonato de construtores")
        print("3. Voltar")
        opcao = input("Selecione uma opção: ")

        if opcao == "1":
            adicionar_resultado(dados)  # Reutilizamos função de 'resultados.py'
        elif opcao == "2":
            adicionar_resultado(dados)  # Reutilizamos função de 'resultados.py'
        elif opcao == "3":
            break
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