from src.menu_principal import exibir_menu_principal
from src.menu_admin import exibir_menu_admin
from src.banco_de_dados import carregar_dados, salvar_dados

# Função de login
def login():
    print("=== Tela de Login ===")
    username = input("Usuário: ")
    password = input("Senha: ")

    if username == "admin" and password == "admin":
        return "admin"
    else:
        return "user"

# Função principal que inicia o programa
def main():
    dados = carregar_dados()

    usuario = login()

    if usuario == "admin":
        exibir_menu_admin(dados)
    else:
        exibir_menu_principal(dados)

    salvar_dados(dados)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Erro detectado: {e}")