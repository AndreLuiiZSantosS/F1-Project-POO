from src.menu_principal import exibir_menu_principal
from src.menu_admin import exibir_menu_admin
from src.banco_de_dados import carregar_dados, salvar_dados

# Função de login
def login():
    while True:
        print("=== Tela de Login ===")
        print("0. Encerrar programa")
        username = input("Usuário: ")
        if username == "0":
            print("Programa encerrado.")
            exit()  # Encerra o programa
        password = input("Senha: ")

        if username == "admin" and password == "admin":
            return "admin"
        elif username == "user" and password == "user":
            return "user"
        else:
            print("Usuário ou senha incorretos. Tente novamente.")

# Função principal que inicia o programa
def main():
    while True:  # Permite retornar ao login após sair dos menus
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