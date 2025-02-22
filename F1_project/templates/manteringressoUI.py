from models.ingresso import Ingresso, Ingressos
from models.etapas import Etapas

class ManterIngressoUI:
    """Menu para gerenciamento de vendas de ingressos."""

    @staticmethod
    def menu_vendas_usuario(cliente_id):
        """Menu para o usuário comprar ingressos."""
        while True:
            # Carrega etapas usando a classe Etapas
            etapas = Etapas.listar_etapas()

            print("\n===== Compra de Ingressos =====")
            for idx, etapa in enumerate(etapas, 1):
                print(f"{idx}. {etapa.nome} - {etapa.data}")  # Supondo que Etapa tenha atributos nome e data
            print(f"{len(etapas) + 1}. Voltar")

            opcao = input("Escolha uma opção: ")
            if opcao.isdigit() and 1 <= int(opcao) <= len(etapas):
                etapa_selecionada = etapas[int(opcao) - 1]
                ManterIngressoUI.processar_compra(etapa_selecionada, cliente_id)
            elif opcao == str(len(etapas) + 1):
                return
            else:
                print("Opção inválida.")

    @staticmethod
    def processar_compra(etapa, cliente_id):
        """Processa a compra de um ingresso."""
        while True:
            print(f"\nIngressos para {etapa.nome} - {etapa.data}:")
            print("1. Arquibancada - R$ 100 cada")
            print("2. VIP - R$ 500 cada")
            print("3. Cancelar")

            tipo = input("Escolha uma opção: ")

            if tipo == "1":
                preco_unitario = 100
                tipo_ingresso = "Arquibancada"
            elif tipo == "2":
                preco_unitario = 500
                tipo_ingresso = "VIP"
            elif tipo == "3":
                return
            else:
                print("Opção inválida. Tente novamente.")
                continue

            try:
                quantidade = int(input("Quantidade de ingressos desejada: "))
                if quantidade <= 0:
                    print("Quantidade deve ser maior que zero.")
                    continue
            except ValueError:
                print("Quantidade inválida. Insira um número inteiro.")
                continue

            valor_total = preco_unitario * quantidade

            # Cria o objeto Ingresso (id será gerado automaticamente)
            novo_ingresso = Ingresso(
                id=0,  # O ID será definido pela classe Ingressos
                etapa_id=etapa.id,  # Supondo que a classe Etapa tenha um atributo id
                cliente_id=cliente_id,  # ID do cliente passado como parâmetro
                quantidade=quantidade,
                valor=valor_total
            )

            # Salva o ingresso no JSON
            Ingressos.adicionar_Ingresso(novo_ingresso)
            print(f"Compra realizada com sucesso! Total: R$ {valor_total}")
            return