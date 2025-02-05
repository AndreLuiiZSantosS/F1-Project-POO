import json

# Caminho do banco de dados
db_vendas = "../data/vendas.json"
db_etapas = "../data/etapas.json"

def carregar_dados(caminho):
    """Carrega dados de um arquivo JSON."""
    try:
        with open(caminho, "r") as arquivo:
            return json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def salvar_dados(caminho, dados):
    """Salva dados em um arquivo JSON."""
    with open(caminho, "w") as arquivo:
        json.dump(dados, arquivo, indent=4)

def menu_vendas_usuario():
    """Menu para o usuário comprar ingressos."""
    while True:
        etapas = carregar_dados(db_etapas)
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
            comprar_ingresso(etapa_selecionada)
        elif opcao == str(len(etapas) + 1):
            return
        else:
            print("Opção inválida.")

def comprar_ingresso(etapa):
    """Realiza o processo de compra do ingresso."""
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

        venda = {
            "etapa": etapa["nome"],
            "data": etapa["data"],
            "tipo": tipo_ingresso,
            "preco": preco,
            "comprador": nome_comprador
        }

        vendas = carregar_dados(db_vendas)
        vendas.append(venda)
        salvar_dados(db_vendas, vendas)

        print(f"Ingresso {tipo_ingresso} comprado para {etapa['nome']}! Total: R$ {preco}")
        return

def menu_vendas_admin():
    """Menu para o administrador visualizar as vendas."""
    while True:
        vendas = carregar_dados(db_vendas)
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
