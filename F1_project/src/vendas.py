import os
import json

CAMINHO_VENDAS = os.path.join(os.path.dirname(__file__), "../data/vendas.json")


def carregar_vendas():
    """Carrega o banco de dados de vendas."""
    if not os.path.exists(os.path.dirname(CAMINHO_VENDAS)):
        os.makedirs(os.path.dirname(CAMINHO_VENDAS))  # Cria a pasta data, se não existir

    if not os.path.exists(CAMINHO_VENDAS):
        with open(CAMINHO_VENDAS, "w") as arquivo:
            json.dump({"vendas": []}, arquivo, indent=4)

    with open(CAMINHO_VENDAS, "r") as arquivo:
        return json.load(arquivo)


def salvar_vendas(dados):
    """Salva os dados de vendas no arquivo."""
    with open(CAMINHO_VENDAS, "w") as arquivo:
        json.dump(dados, arquivo, indent=4)
    print("Dados de vendas salvos com sucesso!")


def listar_etapas_disponiveis(etapas):
    """Lista as etapas disponíveis para venda de ingressos."""
    print("\n✓ Etapas Disponíveis:")
    for idx, etapa in enumerate(etapas, 1):
        print(f"{idx}. {etapa['nome']} - Data: {etapa['data']}")
    return etapas


def registrar_venda(vendas, etapas, usuario):
    """Registra a compra de ingressos para uma etapa."""
    listar_etapas_disponiveis(etapas)
    opcao = input("\nSelecione uma etapa para comprar ingressos: ")

    if opcao.isdigit() and 1 <= int(opcao) <= len(etapas):
        etapa = etapas[int(opcao) - 1]
        quantidade = int(input(f"Quantos ingressos para {etapa['nome']} deseja comprar? "))
        preco_unitario = 100.00  # Valor fictício por ingresso
        total = quantidade * preco_unitario

        # Adicionar a venda ao banco de dados
        vendas["vendas"].append({
            "usuario": usuario,
            "etapa": etapa["nome"],
            "quantidade": quantidade,
            "total": total
        })

        print(f"\nCompra realizada com sucesso! Total: R$ {total:.2f}")
        salvar_vendas(vendas)
    else:
        print("Opção inválida. Tente novamente.")


def exibir_historico_compras(vendas, usuario):
    """Exibe o histórico de compras do usuário."""
    print("\n✓ Histórico de Compras:")
    compras_usuario = [venda for venda in vendas["vendas"] if venda["usuario"] == usuario]

    if not compras_usuario:
        print("Você não realizou nenhuma compra.")
        return

    for idx, compra in enumerate(compras_usuario, 1):
        print(f"{idx}. Etapa: {compra['etapa']} - Ingressos: {compra['quantidade']} - Total: R$ {compra['total']:.2f}")


def exibir_relatorio_vendas(vendas):
    """Exibe um relatório com o total arrecadado e ingressos vendidos."""
    print("\n✓ Relatório de Vendas:")
    total_arrecadado = sum(venda["total"] for venda in vendas["vendas"])
    total_ingressos = sum(venda["quantidade"] for venda in vendas["vendas"])

    print(f"Total Arrecadado: R$ {total_arrecadado:.2f}")
    print(f"Ingressos Vendidos: {total_ingressos}")
