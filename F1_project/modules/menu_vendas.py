from models.carrinho import Carrinho
from F1_project.models.ingresso import Ingresso
from models.etapas import Etapas
from F1_project.templates.manteringressoUI import Venda

class MenuVendas:
    @staticmethod
    def exibir_menu(usuario):
        """
        Exibe o menu de vendas para o usuário.
        
        :param usuario: Nome do usuário logado.
        """
        carrinho = Carrinho()
        while True:
            print("\n=== Menu de Vendas ===")
            print("1. Escolher Etapa")
            print("2. Ver Carrinho")
            print("3. Finalizar Compra")
            print("4. Voltar")

            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                MenuVendas.escolher_etapa(carrinho)
            elif opcao == "2":
                print("\n=== Carrinho ===")
                print(carrinho)
                print(f"Total: R$ {carrinho.calcular_total()}")
            elif opcao == "3":
                MenuVendas.finalizar_compra(carrinho, usuario)
            elif opcao == "4":
                return
            else:
                print("Opção inválida. Tente novamente.")

    @staticmethod
    def escolher_etapa(carrinho):
        """
        Permite ao usuário escolher uma etapa e adicionar ingressos ao carrinho.
        
        :param carrinho: Objeto da classe Carrinho.
        """
        etapas = Etapas.listar_etapas()
        if not etapas:
            print("Nenhuma etapa cadastrada.")
            return

        print("\n=== Etapas Disponíveis ===")
        for etapa in etapas:
            print(etapa)

        etapa_id = int(input("Escolha o ID da etapa: "))
        etapa = Etapas.buscar_etapa_por_id(etapa_id)
        if not etapa:
            print("Etapa não encontrada.")
            return

        dias = []
        print("\nEscolha os dias:")
        print("1. Sexta")
        print("2. Sábado")
        print("3. Domingo")
        print("4. Todos os dias")
        opcao_dias = input("Escolha uma opção: ")
        if opcao_dias == "1":
            dias = ["sexta"]
        elif opcao_dias == "2":
            dias = ["sabado"]
        elif opcao_dias == "3":
            dias = ["domingo"]
        elif opcao_dias == "4":
            dias = ["sexta", "sabado", "domingo"]
        else:
            print("Opção inválida.")
            return

        quantidade = int(input("Quantidade de ingressos: "))
        if quantidade > etapa.ingressos_disponiveis:
            print("Quantidade de ingressos indisponível.")
            return

        valor_unitario = 100  # Valor simbólico
        ingresso = Ingresso(etapa_id, dias, quantidade, valor_unitario)
        carrinho.adicionar_ingresso(ingresso)
        print("Ingresso adicionado ao carrinho!")

    @staticmethod
    def finalizar_compra(carrinho, usuario):
        """
        Finaliza a compra e registra a venda.
        
        :param carrinho: Objeto da classe Carrinho.
        :param usuario: Nome do usuário logado.
        """
        if not carrinho.itens:
            print("Carrinho vazio.")
            return

        print("\n=== Resumo da Compra ===")
        print(carrinho)
        print(f"Total: R$ {carrinho.calcular_total()}")

        confirmacao = input("Confirmar compra? (S/N): ").strip().lower()
        if confirmacao == "s":
            ingressos_comprados = carrinho.finalizar_compra()
            for ingresso in ingressos_comprados:
                etapa = Etapas.buscar_etapa_por_id(ingresso.etapa_id)
                etapa.ingressos_disponiveis -= ingresso.quantidade
                Etapas.salvar_etapas()
                Vendas.adicionar_venda({
                    "usuario": usuario,
                    "etapa_id": ingresso.etapa_id,
                    "dias": ingresso.dias,
                    "quantidade": ingresso.quantidade,
                    "valor_total": ingresso.calcular_total()
                })
            print("Compra finalizada com sucesso!")
        else:
            print("Compra cancelada.")