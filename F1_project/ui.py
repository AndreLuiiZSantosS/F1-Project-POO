from views import View
from modules.menu_admin import MenuAdmin

class UI:
    # dados do usuário logado
    cliente_id = 0
    cliente_nome = ""
    @staticmethod
    def menu():
        MenuAdmin.exibir()
        return int(input("Informe uma opção: "))
    @staticmethod
    def main():
        View.usuario_admin()
        op = 0
        while op != 99:
            op = UI.menu()
            if op == 1: UI.cliente_inserir()
            if op == 2: UI.cliente_listar()
            if op == 3: UI.cliente_atualizar()
            if op == 4: UI.cliente_excluir()

            if op == 5: UI.categoria_inserir()
            if op == 6: UI.categoria_listar()
            if op == 7: UI.categoria_atualizar()
            if op == 8: UI.categoria_excluir()

            if op == 9:  UI.produto_inserir()
            if op == 10: UI.produto_listar()
            if op == 11: UI.produto_atualizar()
            if op == 12: UI.produto_excluir()
            if op == 13: UI.produto_reajustar()

            if op == 14: UI.visitante_abrir_conta()
            if op == 15: UI.visitante_entrar_no_sistema()

UI.main()