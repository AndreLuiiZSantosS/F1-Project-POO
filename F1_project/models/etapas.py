import json
class Etapa:
    def __init__(self, id, nome, data, pista):
        self.id = id
        self.nome = nome
        self.data = data
        self.pista = pista
    
    def __str__(self):
        return f"{self.nome} - {self.data} - {self.pista}"

# Caminho do banco de dados de etapas
CAMINHO_BD_ETAPAS = "../data/etapas.json"

class Etapas:
    objetos = []
    @classmethod
    def carregar_etapas(cls):
        """Carrega as etapas do arquivo JSON."""
        cls.objetos = []
        try:
            with open("etapas.json", mode="r") as arquivo:
                objetos_json = json.load(arquivo)
                for obj in objetos_json: 
                    c = Etapa(obj["nome"])
                    cls.objetos.append(c)
        except FileNotFoundError:
            print("erro")
            return []
        except json.JSONDecodeError:
            print(f"Erro ao carregar o arquivo {CAMINHO_BD_ETAPAS}.")
            return []
    @classmethod
    def salvar_etapas(cls, etapas):
        """Salva as etapas no arquivo JSON."""
        try:
            with open("etapas.json", mode="w") as arquivo:
                json.dump({"etapas": etapas}, arquivo, indent=4)
        except Exception as e:
            print(f"Erro ao salvar etapas: {e}")
    @classmethod
    def menu_etapas(cls):
        """Exibe o menu de etapas disponíveis (usuário comum)."""
        while True:
            etapas = cls.carregar_etapas()

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
                    cls.exibir_detalhes_etapa(etapas[opcao - 1])
                elif opcao == len(etapas) + 1:
                    return
                else:
                    print("Opção inválida. Tente novamente.")
            else:
                print("Entrada inválida. Digite um número correspondente.")
    @classmethod
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
    @classmethod
    def menu_admin_etapas(cls):
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
                cls.listar_etapa()
            elif opcao == "2":
                cls.adicionar_etapa()
            elif opcao == "3":
                cls.editar_etapa()
            elif opcao == "4":
                cls.remover_etapa()
            elif opcao == "5":
                return
            else:
                print("Opção inválida. Tente novamente.")
    @classmethod
    def adicionar_etapa(cls):
        """Adiciona uma nova etapa ao campeonato."""
        id = 0 
        for x in cls.obj:
            if x.id > id: id = x.id
        
        nome = input("Nome da etapa: ")
        data = input("Data da etapa: ")
        pista = input("pista da etapa: ")

        etapas = cls.carregar_etapas()
        etapas.append({"nome": nome, "data": data, "pista": pista})

        cls.salvar_etapas(etapas)
        print("Etapa adicionada com sucesso!")
    @classmethod
    def editar_etapa(cls):
        """Edita uma etapa existente."""
        etapas = cls.carregar_etapas()
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

            cls.salvar_etapas(etapas)
            print("Etapa editada com sucesso!")
        else:
            print("Opção inválida.")
            
    @classmethod
    def listar_etapa(cls):
        cls.carregar_etapas()
        return cls.objetos[:]
    
    @classmethod
    def remover_etapa(cls):
        """Remove uma etapa existente."""
        etapas = cls.carregar_etapas()
        if not etapas:
            print("Nenhuma etapa cadastrada.")
            return

        for idx, etapa in enumerate(etapas, 1):
            print(f"{idx}. {etapa['nome']} - {etapa['data']}")

        opcao = input("Selecione a etapa para remover: ")
        if opcao.isdigit() and 1 <= int(opcao) <= len(etapas):
            etapas.pop(int(opcao) - 1)
            cls.salvar_etapas(etapas)
            print("Etapa removida com sucesso!")
        else:
            print("Opção inválida.")
