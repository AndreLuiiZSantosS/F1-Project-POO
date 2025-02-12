from modules.menu_principal import MenuPrincipal 
from modules.menu_admin import MenuAdmin

def login():
    """Função de login com credenciais básicas."""
    print("\n=== Tela de Login ===")
    print("Digite 'sair' a qualquer momento para encerrar o programa.")

    while True:
        username = input("Usuário: ").strip()
        if username.lower() == "sair":
            print("Encerrando o programa...")
            exit()

        password = input("Senha: ").strip()
        if password.lower() == "sair":
            print("Encerrando o programa...")
            exit()

        if username and password:
            if username == "admin" and password == "admin":
                print("\nLogin bem-sucedido! Acessando painel administrativo...")
                return "admin"
            else:
                print("\nLogin como usuário comum.")
                return "user"
        else:
            print("Usuário e senha não podem estar vazios. Tente novamente.")

def main():
    """Função principal que inicia o programa."""
    while True:
        usuario = login()

        if usuario == "admin":
            MenuAdmin.exibir()  # Mantém a chamada original
        else:
            MenuPrincipal.exibir()  # Mantém a chamada original

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nErro detectado: {e}")
        opcao = input("Deseja reiniciar o programa? (S/N): ").strip().lower()
        if opcao == "s":
            main()
        else:
            print("Encerrando o programa.")
            exit()