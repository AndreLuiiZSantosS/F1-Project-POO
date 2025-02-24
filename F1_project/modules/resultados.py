# resultados.py 
import json
import random
from estatisticas import Estatistica  # Importe para acessar dados de pilotos

class Resultado:
    CAMINHO_BD_RESULTADOS = "../data/resultados.json"
    CAMINHO_PILOTOS = Estatistica.CAMINHO_BD_PILOTOS  # Usar o mesmo caminho

    # ... (métodos carregar_resultados, salvar_resultados e listar_resultados existentes)

    @staticmethod
    def gerar_resultado_etapa():
        """Gera um resultado aleatório para uma etapa incluindo DNFs"""
        etapa_id = input("ID da etapa: ").strip()
        etapa_nome = input("Nome da etapa: ").strip()
        
        # Carregar pilotos
        try:
            with open(Resultado.CAMINHO_PILOTOS, "r") as f:
                pilotos = json.load(f)["pilotos"]
        except Exception as e:
            print(f"Erro ao carregar pilotos: {e}")
            return

        if len(pilotos) < 20:
            print("Erro: Cadastre pelo menos 20 pilotos!")
            return

        # Embaralhar pilotos e selecionar 20
        random.shuffle(pilotos)
        pilotos_corrida = pilotos[:20]
        
        # Gerar posições com DNFs
        resultados_etapa = []
        for posicao_real, piloto in enumerate(pilotos_corrida, 1):
            dnf = random.choices([True, False], weights=[0.2, 0.8])[0]
            
            resultados_etapa.append({
                "id": etapa_id,
                "etapa": etapa_nome,
                "piloto": piloto["nome"],
                "equipe": piloto["equipe"],
                "posicao": posicao_real,
                "dnf": dnf
            })

        # Salvar resultados
        dados = Resultado.carregar_resultados()
        dados["resultados"].extend(resultados_etapa)
        Resultado.salvar_resultados(dados)
        print(f"Resultado da etapa {etapa_nome} gerado com sucesso!")

class MenuResultados:
    @staticmethod
    def exibir():
        while True:
            print("\n✓ Gerenciamento de Resultados")
            print("1. Listar resultados")
            print("2. Adicionar resultado manual")
            print("3. Gerar resultado automático")
            print("4. Voltar")

            opcao = input("Selecione uma opção: ")

            if opcao == "1":
                Resultado.listar_resultados()
            elif opcao == "2":
                Resultado.adicionar_resultado()
            elif opcao == "3":
                Resultado.gerar_resultado_etapa()
            elif opcao == "4":
                return
            else:
                print("Opção inválida. Tente novamente.")