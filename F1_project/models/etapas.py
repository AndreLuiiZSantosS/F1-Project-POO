import json
class Etapa:
    def __init__(self, nome, data, pista):
        self.nome = nome
        self.data = data
        self.pista = pista
    
    def __str__(self):
        return f"{self.nome} - {self.data} - {self.pista}"

# Caminho do banco de dados de etapas
CAMINHO_BD_ETAPAS = "../data/etapas.json"
class Etapas:
    def carregar_etapas():
        """Carrega as etapas do arquivo JSON."""
        try:
            with open(CAMINHO_BD_ETAPAS, "r") as arquivo:
                return json.load(arquivo).get("etapas", [])
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            print(f"Erro ao carregar o arquivo {CAMINHO_BD_ETAPAS}.")
            return []

    def salvar_etapas(etapas):
        """Salva as etapas no arquivo JSON."""
        try:
            with open(CAMINHO_BD_ETAPAS, "w") as arquivo:
                json.dump({"etapas": etapas}, arquivo, indent=4)
        except Exception as e:
            print(f"Erro ao salvar etapas: {e}")

    def menu_etapas():
        """Exibe o menu de etapas disponíveis (usuário comum)."""
        while True:
            etapas = carregar_etapas()

            print("\n" + "="*30)
            print("✓ Etapas do Campeonato")
            print("="*30)

            if not etapas:
                print("Nenhuma etapa cadastrada.")
                input("\nPressione Enter para voltar...")
                return

            for idx, etapa in enumerate(etapas, 1):
                print(f"{idx}. {etapa['nome']} - {etapa['data']}")
            print(f"{len(etapas) + 1}. Voltar")

            opcao = input("Selecione uma opção: ")

            if opcao.isdigit():
                opcao = int(opcao)
                if 1 <= opcao <= len(etapas):
                    exibir_detalhes_etapa(etapas[opcao - 1])
                elif opcao == len(etapas) + 1:
                    return
                else:
                    print("Opção inválida. Tente novamente.")
            else:
                print("Entrada inválida. Digite um número correspondente.")

    def exibir_detalhes_etapa(etapa):
        """Exibe detalhes de uma etapa específica."""
        print("\n" + "="*30)
        print(f"✓ Detalhes da Etapa: {etapa['nome']}")
        print("="*30)
        print(f"Data: {etapa['data']}")
        print(f"pista: {etapa.get('pista', 'Não especificado')}")
        print(f"Treinos: {etapa.get('treinos', 'Não informados')}")
        print(f"Classificação: {etapa.get('classificacao', 'Não informada')}")
        print(f"Corrida: {etapa.get('corrida', 'Não informada')}")
        
        input("\nPressione Enter para voltar...")

    # ========================= MENU DO ADMINISTRADOR =========================

    def menu_admin_etapas():
        """Exibe o menu de gerenciamento de etapas para o administrador."""
        while True:
            print("\n=== Gerenciamento de Etapas ===")
            print("1. Listar Etapas")
            print("2. Adicionar Etapa")
            print("3. Editar Etapa")
            print("4. Remover Etapa")
            print("5. Voltar")

            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                menu_etapas()
            elif opcao == "2":
                adicionar_etapa()
            elif opcao == "3":
                editar_etapa()
            elif opcao == "4":
                remover_etapa()
            elif opcao == "5":
                return
            else:
                print("Opção inválida. Tente novamente.")

    def adicionar_etapa():
        """Adiciona uma nova etapa ao campeonato."""
        nome = input("Nome da etapa: ")
        data = input("Data da etapa: ")
        pista = input("pista da etapa: ")

        etapas = carregar_etapas()
        etapas.append({"nome": nome, "data": data, "pista": pista})

        salvar_etapas(etapas)
        print("Etapa adicionada com sucesso!")

    def editar_etapa():
        """Edita uma etapa existente."""
        etapas = carregar_etapas()
        if not etapas:
            print("Nenhuma etapa cadastrada.")
            return

        for idx, etapa in enumerate(etapas, 1):
            print(f"{idx}. {etapa['nome']} - {etapa['data']}")

        opcao = input("Selecione a etapa para editar: ")
        if opcao.isdigit() and 1 <= int(opcao) <= len(etapas):
            idx = int(opcao) - 1
            etapas[idx]['nome'] = input(f"Novo nome ({etapas[idx]['nome']}): ") or etapas[idx]['nome']
            etapas[idx]['data'] = input(f"Nova data ({etapas[idx]['data']}): ") or etapas[idx]['data']
            etapas[idx]['pista'] = input(f"Novo pista ({etapas[idx]['pista']}): ") or etapas[idx]['pista']

            salvar_etapas(etapas)
            print("Etapa editada com sucesso!")
        else:
            print("Opção inválida.")

    def remover_etapa():
        """Remove uma etapa existente."""
        etapas = carregar_etapas()
        if not etapas:
            print("Nenhuma etapa cadastrada.")
            return

        for idx, etapa in enumerate(etapas, 1):
            print(f"{idx}. {etapa['nome']} - {etapa['data']}")

        opcao = input("Selecione a etapa para remover: ")
        if opcao.isdigit() and 1 <= int(opcao) <= len(etapas):
            etapas.pop(int(opcao) - 1)
            salvar_etapas(etapas)
            print("Etapa removida com sucesso!")
        else:
            print("Opção inválida.")
