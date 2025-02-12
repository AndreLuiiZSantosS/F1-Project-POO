from models.piloto import Piloto, Pilotos  
from modules.etapas import Etapas
from modules.resultados import MenuResultados
from modules.estatisticas import MenuEstatisticas
from modules.vendas import MenuVendas

class MenuAdmin:
    """Menu principal para administradores."""

    @staticmethod
    def exibir():
        """Exibe o menu principal para administradores."""
        while True:
            print("\n===== Menu Administrador =====")
            print("1. Gerenciar Etapas")
            print("2. Gerenciar Pilotos")
            print("3. Gerenciar Resultados")
            print("4. Gerenciar Estatísticas")
            print("5. Gerenciar Vendas")
            print("6. Sair")

            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                Etapas.menu_admin_etapas()  # Usa a classe MenuEtapas
            elif opcao == "2":
                Pilotos.menu_admin_pilotos()  # Mantém a chamada original
            elif opcao == "3":
                MenuResultados.exibir()  # Usa a classe MenuResultados
            elif opcao == "4":
                MenuEstatisticas.exibir()  # Usa a classe MenuEstatisticas
            elif opcao == "5":
                MenuVendas.menu_vendas_admin()  # Usa a classe MenuVendas
            elif opcao == "6":
                print("Saindo do menu administrador...")
                break
            else:
                print("Opção inválida! Tente novamente.")