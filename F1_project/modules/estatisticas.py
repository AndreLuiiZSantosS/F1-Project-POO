import json

class Estatistica:
    # Caminho do banco de dados de pilotos e resultados
    CAMINHO_BD_PILOTOS = "../data/pilotos.json"
    CAMINHO_BD_RESULTADOS = "../data/resultados.json"

    @staticmethod
    def carregar_dados(caminho):
        """Carrega dados de um arquivo JSON."""
        try:
            with open(caminho, "r") as arquivo:
                return json.load(arquivo)
        except FileNotFoundError:
            return {"pilotos": []} if "pilotos" in caminho else {"resultados": []}
        except json.JSONDecodeError:
            print(f"Erro ao carregar o arquivo {caminho}.")
            return {"pilotos": []} if "pilotos" in caminho else {"resultados": []}

    @staticmethod
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

    @staticmethod
    def exibir_estatisticas_pilotos():
        """Exibe o ranking dos pilotos com base nos resultados."""
        pilotos = Estatistica.carregar_dados(Estatistica.CAMINHO_BD_PILOTOS)["pilotos"]
        resultados = Estatistica.carregar_dados(Estatistica.CAMINHO_BD_RESULTADOS)["resultados"]

        pontuacao_pilotos = {}

        for resultado in resultados:
            piloto = resultado["piloto"]
            pontos = Estatistica.calcular_pontos(int(resultado["posicao"]))
            pontuacao_pilotos[piloto] = pontuacao_pilotos.get(piloto, 0) + pontos

        ranking = sorted(pontuacao_pilotos.items(), key=lambda x: x[1], reverse=True)

        print("\n" + "="*30)
        print("✓ Campeonato de Pilotos")
        print("="*30)

        if not ranking:
            print("Nenhum piloto registrado no campeonato.")
        else:
            for idx, (piloto, pontos) in enumerate(ranking, 1):
                print(f"{idx}. {piloto} - {pontos} pontos")

        input("\nPressione Enter para voltar...")

    @staticmethod
    def exibir_estatisticas_construtores():
        """Exibe o ranking das equipes com base nos resultados."""
        pilotos = Estatistica.carregar_dados(Estatistica.CAMINHO_BD_PILOTOS)["pilotos"]
        resultados = Estatistica.carregar_dados(Estatistica.CAMINHO_BD_RESULTADOS)["resultados"]

        equipe_pontos = {}

        for resultado in resultados:
            piloto_nome = resultado["piloto"]
            equipe = next((p["equipe"] for p in pilotos if p["nome"] == piloto_nome), None)

            if equipe:
                pontos = Estatistica.calcular_pontos(int(resultado["posicao"]))
                equipe_pontos[equipe] = equipe_pontos.get(equipe, 0) + pontos

        ranking = sorted(equipe_pontos.items(), key=lambda x: x[1], reverse=True)

        print("\n" + "="*30)
        print("✓ Campeonato de Construtores")
        print("="*30)

        if not ranking:
            print("Nenhuma equipe registrada no campeonato.")
        else:
            for idx, (equipe, pontos) in enumerate(ranking, 1):
                print(f"{idx}. {equipe} - {pontos} pontos")

        input("\nPressione Enter para voltar...")


class MenuEstatisticas:
    """Menu para exibição de estatísticas do campeonato."""

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