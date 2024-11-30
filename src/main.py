from src.menu_principal import exibir_menu_principal
from src.banco_de_dados import carregar_dados, salvar_dados

# Função principal que inicia o programa
def main():
    dados = carregar_dados()
    exibir_menu_principal(dados)
    salvar_dados(dados)

if __name__ == "__main__":
    main()