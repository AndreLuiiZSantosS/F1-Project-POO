from views import View

class AbrircontaUI:
    def main():
        print("abrir conta no sistema")
        AbrircontaUI.inserir()
    
    def inserir():
        nome = input("Digite o nome: ")
        senha = input("Digite a sua senha: ")

        View.cliente_inserir(nome, senha)
        print("conta criada com sucesso!")