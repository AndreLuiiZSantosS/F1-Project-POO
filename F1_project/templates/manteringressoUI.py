import json

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
                GerenciarVendas.processar_compra(etapa_selecionada)
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


       def gerenciar_vendas ():

import json

class Ingresso:
    def __init__(self, id,etapa_id, quantidade, valor):
        
        self.id = id
        self.etapa_id = etapa_id
        self.quantidade = quantidade
        self.valor = valor
    
    def __str__(self):
        return f"{self.etapa_id} - {self.quantidade} - {self.valor}"

    def carregar_ingresso(cls):
         # esvazia a lista de objetos
        cls.objetos = []
        try:
            with open("ingresso.json", mode="r") as arquivo:
                # abre o arquivo com a lista de dicionários -> clientes_json
                clientes_json = json.load(arquivo)
                # percorre a lista de dicionários
                for obj in clientes_json:
                    # recupera cada dicionário e cria um objeto
                    c = Ingresso(obj["id"] ,obj["etapa_id"], obj["quantidade"], obj["valor"])
                    # insere o objeto na lista
                    cls.objetos.append(c)    
        except FileNotFoundError:
            pass

    def salvar_ingresso(cls):
        # open - cria e abre o arquivo clientes.json
        # vars - converte um objeto em um dicionário
        # dump - pega a lista de objetos e salva no arquivo
        with open("ingresso.json", mode="w") as arquivo:
            json.dump(cls.objetos, arquivo, default = vars)

    def listar_ingresso(cls):
         # abre a lista do arquivo
        cls.carregar_ingresso()
        # retorna a lista para a UI
        return cls.objetos
    
    def listar_id(cls, id):
        cls.carregar_ingresso()
        # percorre a lista procurando o id    
        for x in cls.objetos:
            if x.id == id: return x
        return None

    def adicionar_Ingresso(cls, obj):
        # abre a lista do arquivo
        cls.carregar_ingresso()
        # calcula o id do objeto
        id = 0
        for x in cls.objetos:
            if x.id > id: id = x.id
        obj.id = id + 1    
        # insere o objeto na lista
        cls.objetos.append(obj)
        # salva a lista no arquivo
        cls.salvar_ingresso()

    def editar_Ingresso(cls, obj):
        x = cls.listar_id(obj.id)
        if x != None:
            cls.objetos.remove(x)
            cls.objetos.append(obj)
            #x.nome = obj.nome
            #x.email = obj.email
            #x.fone = obj.fone
            cls.salvar_ingresso()     
    
    def remover_Ingresso(cls, obj):
        x = cls.listar_id(obj.id)
        if x != None:
            cls.objetos.remove(x)
            cls.salvar_ingresso()



