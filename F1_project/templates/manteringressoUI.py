import json
from modules.venda import Vendas  

class ManterIngressoUI:
    """Menu para gerenciamento de vendas."""

    @staticmethod
    def menu_vendas_usuario():
        """Menu para o usuário comprar ingressos."""
        while True:
            etapas = Venda.carregar_dados(Venda.DB_ETAPAS)

            print("\n===== Compra de Ingressos =====")
            for idx, etapa in enumerate(etapas, 1):
                print(f"{idx}. {etapa['nome']} - {etapa['data']}")
            print(f"{len(etapas) + 1}. Voltar")

            opcao = input("Escolha uma opção: ")
            if opcao.isdigit() and 1 <= int(opcao) <= len(etapas):
                etapa_selecionada = etapas[int(opcao) - 1]
                ManterIngressoUI.processar_compra(etapa_selecionada)
            elif opcao == str(len(etapas) + 1):
                return
            else:
                print("Opção inválida.")

    @staticmethod
    def processar_compra(etapa):
        """Processa a compra de um ingresso."""
        while True:
            print(f"\nIngressos para {etapa['nome']} - {etapa['data']}:")
            print("1. Arquibancada - R$ 100")
            print("2. VIP - R$ 500")
            print("3. Cancelar")

            tipo = input("Escolha uma opção: ")

            if tipo == "1":
                tipo_ingresso = "Arquibancada"
                preco = 100
            elif tipo == "2":
                tipo_ingresso = "VIP"
                preco = 500
            elif tipo == "3":
                return
            else:
                print("Opção inválida. Tente novamente.")
                continue

            nome_comprador = input("Digite seu nome: ")
            Venda.comprar_ingresso(etapa, nome_comprador, tipo_ingresso, preco)
            return

    @staticmethod
    def menu_vendas_admin():
        """Menu para o administrador visualizar as vendas."""
        while True:
            vendas = Venda.carregar_dados(Venda.DB_VENDAS)
            if not vendas:
                print("\nNenhuma venda registrada.")
                return

            print("\n===== Gerenciamento de Vendas =====")
            for idx, venda in enumerate(vendas, 1):
                print(f"{idx}. {venda['comprador']} - {venda['tipo']} ({venda['etapa']}) - R$ {venda['preco']}")

            print(f"{len(vendas) + 1}. Voltar")

            opcao = input("Escolha uma opção: ")
            if opcao == str(len(vendas) + 1):
                return
            else:
                print("Opção inválida.")


class Ingresso:
    def __init__(self, id, etapa_id, quantidade, valor):
        self.id = id
        self.etapa_id = etapa_id
        self.quantidade = quantidade
        self.valor = valor

    def __str__(self):
        return f"Ingresso {self.id} - Etapa {self.etapa_id} - Quantidade: {self.quantidade} - Valor: R$ {self.valor:.2f}"

    @classmethod
    def carregar_ingresso(cls):
        """Carrega a lista de ingressos do arquivo JSON."""
        cls.objetos = []
        try:
            with open("ingresso.json", mode="r") as arquivo:
                dados = json.load(arquivo)
                for obj in dados:
                    cls.objetos.append(Ingresso(**obj))
        except FileNotFoundError:
            pass

    @classmethod
    def salvar_ingresso(cls):
        """Salva a lista de ingressos no arquivo JSON."""
        with open("ingresso.json", mode="w") as arquivo:
            json.dump([vars(ingresso) for ingresso in cls.objetos], arquivo, indent=4)

    @classmethod
    def listar_ingresso(cls):
        """Retorna a lista de ingressos."""
        cls.carregar_ingresso()
        return cls.objetos

    @classmethod
    def listar_id(cls, id):
        """Busca um ingresso pelo ID."""
        cls.carregar_ingresso()
        for x in cls.objetos:
            if x.id == id:
                return x
        return None

    @classmethod
    def adicionar_ingresso(cls, obj):
        """Adiciona um novo ingresso à lista."""
        cls.carregar_ingresso()
        # Calcula o ID do objeto
        novo_id = max([x.id for x in cls.objetos], default=0) + 1
        obj.id = novo_id
        cls.objetos.append(obj)
        cls.salvar_ingresso()

    @classmethod
    def editar_ingresso(cls, obj):
        """Edita um ingresso existente."""
        cls.carregar_ingresso()
        x = cls.listar_id(obj.id)
        if x is not None:
            cls.objetos.remove(x)
            cls.objetos.append(obj)
            cls.salvar_ingresso()

    @classmethod
    def remover_ingresso(cls, obj):
        """Remove um ingresso da lista."""
        cls.carregar_ingresso()
        x = cls.listar_id(obj.id)
        if x is not None:
            cls.objetos.remove(x)
            cls.salvar_ingresso()