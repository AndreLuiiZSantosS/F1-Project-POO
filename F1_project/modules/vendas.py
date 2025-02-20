import json
from F1_project.models.ingresso import Ingresso

class Venda:
    # Caminho do banco de dados
    DB_VENDAS = "../data/vendas.json"
    DB_ETAPAS = "../data/etapas.json"

    @staticmethod
    def carregar_dados(caminho):
        """Carrega dados de um arquivo JSON."""
        try:
            with open(caminho, "r") as arquivo:
                return json.load(arquivo)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    @staticmethod
    def salvar_dados(caminho, dados):
        """Salva dados em um arquivo JSON."""
        with open(caminho, "w") as arquivo:
            json.dump(dados, arquivo, indent=4)

    @staticmethod
    def comprar_ingresso(etapa, nome_comprador, tipo_ingresso, preco):
        """Realiza o processo de compra do ingresso."""
        venda = {
            "etapa": etapa["nome"],
            "data": etapa["data"],
            "tipo": tipo_ingresso,
            "preco": preco,
            "comprador": nome_comprador
        }

        vendas = Venda.carregar_dados(Venda.DB_VENDAS)
        vendas.append(venda)
        Venda.salvar_dados(Venda.DB_VENDAS, vendas)

        print(f"Ingresso {tipo_ingresso} comprado para {etapa['nome']}! Total: R$ {preco}")


    @staticmethod
    def criar_ingresso(etapa_id, dias, quantidade):
    
        return criar_ingresso
    
        etapa_id=etapa_id, dias=dias, quantidade=quantidade, valor_unitario=100
    

    @staticmethod
    def menu_vendas_usuario():
        """Menu para o usuário comprar ingressos."""
        while True:
            etapas = Venda.carregar_dados(Venda.DB_ETAPAS)
            if not etapas:
                print("Nenhuma etapa disponível para venda.")
                return

            print("\n===== Compra de Ingressos =====")
            for idx, etapa in enumerate(etapas, 1):
                print(f"{idx}. {etapa['nome']} - {etapa['data']}")
            print(f"{len(etapas) + 1}. Voltar")

            opcao = input("Escolha uma opção: ")
            if opcao.isdigit() and 1 <= int(opcao) <= len(etapas):
                etapa_selecionada = etapas[int(opcao) - 1]
                MenuVendas.processar_compra(etapa_selecionada)
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
                
    