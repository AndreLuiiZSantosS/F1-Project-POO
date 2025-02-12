from views import View
from modules.menu_admin import MenuAdmin

class UI:
    # dados do usuário logado
    piloto_id = 0
    piloto_nome = ""
    @staticmethod
    def menu():
        print("\n===== Menu Administrador =====")
        print("1. Gerenciar Etapas")
        print("2. adicionar Pilotos")
        print("3. listar Pilotos")
        print("4. editar Pilotos")
        print("5. excluir Pilotos")
        print("6. Gerenciar Pilotos")
        print("3. Gerenciar Resultados")
        print("4. Gerenciar Estatísticas")
        print("5. Gerenciar Vendas")
        print("6. Sair")
        return int(input("Informe uma opção: "))
    @staticmethod
    def main():
        #View.usuario_admin()
        op = 0
        while op != 99:
            op = UI.menu()
            if op == 2: UI.adicionar_pilotos()
            if op == 3: UI.listar_pilotos()
            if op == 4: UI.piloto_atualizar()
            if op == 5: UI.piloto_excluir()
    
    @classmethod
    def adicionar_pilotos(cls):
        nome = input("Informe o nome: ")
        equipe = input("Informe a equipe: ")
        pontuacao = input("Informe a pontuacao: ")

        View.piloto_inserir(nome, equipe, pontuacao)

    @classmethod
    def listar_pilotos(cls):
        pilotos = View.piloto_listar()
        if len(pilotos) == 0:
            print("Nenhum piloto cadastrado")
        else:    
            for piloto in pilotos: print(piloto)

    @classmethod 
    def piloto_atualizar(cls):
        cls.listar_pilotos()
        # Lê o id do piloto a ser atualizado
        id = int(input("Informe o id do piloto a ser alterado: "))
        # Lê os novos dados do piloto
        nome = input("Informe o novo nome: ")
        equipe = input("Informe o novo equipe: ")
        pontuacao = input("Informe o novo pontuacao: ")
        # instancia a classe piloto -> objeto piloto
        # piloto = piloto(id, nome, equipe, pontuacao)
        # chama a operação de atualizar 
        # pilotos.atualizar(piloto)
        View.piloto_atualizar(id, nome, equipe, pontuacao)
    
    @classmethod
    def piloto_excluir(cls):
        cls.listar_pilotos()
        # Lê o id do piloto a ser excluído
        id = int(input("Informe o id do piloto a ser excluído: "))
        # instancia a classe piloto -> objeto piloto
        # piloto = piloto(id, "", "", "")
        # chama a operação de excluir 
        # pilotos.excluir(piloto)
        View.piloto_excluir(id)
UI.main()