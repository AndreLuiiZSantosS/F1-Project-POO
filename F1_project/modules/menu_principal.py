from modules.estatisticas import MenuEstatisticas
from modules.vendas import MenuVendas
from models.etapas import Etapas

class MenuPrincipal:
    """Menu principal para usuários comuns."""

    @staticmethod
    def exibir():
        """Exibe o menu principal para usuários comuns."""
        while True:
            print("\n=== Menu do Usuário ===")
            print("1. Visualizar Etapas")
            print("2. Visualizar Estatísticas")
            print("3. Comprar Ingressos")
            print("4. Voltar ao Login")

            opcao = input("Selecione uma opção: ")

            if opcao == "1":
                Etapas.menu_etapas()  # Usa a classe MenuEtapas
            elif opcao == "2":
                MenuEstatisticas.exibir()  # Usa a classe MenuEstatisticas
            elif opcao == "3":
                MenuVendas.menu_vendas_usuario()  # Usa a classe MenuVendas
            elif opcao == "4":
                return  # Volta ao login
            else:
                print("Opção inválida. Tente novamente.")