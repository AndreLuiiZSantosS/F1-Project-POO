from views import View

class AbrirContaUI:
    def main():
        print("Abrir Conta no Sistema")
        AbrirContaUI.inserir()

    def inserir():
        nome = input("Informe o nome: ")
        senha = input("Informe a senha: ")
        
        conta = View.cliente_inserir(nome, senha)
        
        print("conta criada com sucesso!")