from modules.vendas import Venda
from views import View
from models.etapas import Etapas  
from templates.abrircontaUI import AbrirContaUI


class UI:
    # Dados do usuário logado
    piloto_id = 0
    piloto_nome = ""
    is_admin = False

    @staticmethod
    def login():
        """Método para realizar o login."""
        username = input("Digite o nome de usuário: ")
        password = input("Digite a senha: ")
        
        autenticado = View.cliente_autenticar(username, password)

        if username == "admin" and password == "admin":
            UI.is_admin = True
            print("Login como administrador realizado com sucesso!")
        elif autenticado != None:
            UI.is_admin = False
            print("Login como usuário comum realizado com sucesso.")
        
        if autenticado != None:
            return 1
        else:
            return None
    
    @staticmethod
    def menu():
        if UI.login() == 1:
            
            #Exibe o menu organizado horizontalmente por categorias.

            print("\n===== Menu Principal =====")
            print("Categorias: Pilotos | Etapas | Resultados | Estatísticas | Vendas | Sair")
            print("-------------------------------------------------------------")
            
            if UI.is_admin:
                print("1. Gerenciar etapas")
                print("2. adicionar Pilotos       3. Listar Pilotos        4. Editar Piloto         5. Excluir Piloto")
                print("7. Gerenciar Estatísticas 8. Gerenciar Vendas      9. Sair")
            else:
                print("1. Listar Pilotos        9. Sair")
            return int(input("Informe uma opção: "))
        else:
            print("Usuario ou senha errados!")
    @staticmethod
    def main():
        abrirconta = input("gostaria de criar uma conta? (sim/nao) ")
        if abrirconta.lower() == "sim":
            AbrirContaUI.main()
            UI.menu()
        else:
            UI.menu()
        
        if UI.is_admin:
            op = 0
            while op != 9:  
                op = UI.menu()
                if op == 1: UI.gerenciar_etapas()
                if op == 2: UI.adicionar_pilotos()
                if op == 3: UI.listar_pilotos()
                if op == 4: UI.piloto_atualizar()
                if op == 5: UI.piloto_excluir()
                if op == 6: UI.gerenciar_resultados()
                if op == 7: UI.gerenciar_estatisticas()
                if op == 8: UI.gerenciar_vendas()
        else:
            op = 0
            while op != 9:  
                op = UI.menu()
                if op == 1: UI.listar_pilotos()
                if op == 2: UI.listar_etapas()
               #if op == 3: UI.listar_estatisticas()
                if op == 4: UI.comprar_ingresso() 
    
    @classmethod
    def gerenciar_etapas(cls):
        #exibe o menu de gerenciamento de etapas.
        while True:
            print("\n=== Gerenciamento de Etapas ===")
            print("1. Listar Etapas")
            print("2. Adicionar Etapa")
            print("3. Editar Etapa")
            print("4. Remover Etapa")
            print("5. Voltar")

            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                cls.listar_etapas()
            elif opcao == "2":
                cls.adicionar_etapa()
            elif opcao == "3":
                cls.editar_etapa()
            elif opcao == "4":
                cls.remover_etapa()
            elif opcao == "5":
                return
            else:
                print("Opção inválida. Tente novamente.")

    @classmethod
    def listar_etapas(cls):
        """Lista todas as etapas cadastradas."""
        etapas = Etapas.listar_etapas()
        if not etapas:
            print("Nenhuma etapa cadastrada.")
        else:
            for etapa in etapas:
                print(etapa)

    @classmethod
    def adicionar_etapa(cls):
        """Adiciona uma nova etapa."""
        nome = input("Nome da etapa: ")
        data = input("Data da etapa: ")
        pista = input("Pista da etapa: ")
        Etapas.adicionar_etapa(nome, data, pista)
        print("Etapa adicionada com sucesso!")

    @classmethod
    def editar_etapa(cls):
        """Edita uma etapa existente."""
        cls.listar_etapas()
        id = int(input("ID da etapa a editar: "))
        nome = input("Novo nome (deixe em branco para manter): ")
        data = input("Nova data (deixe em branco para manter): ")
        pista = input("Nova pista (deixe em branco para manter): ")
        Etapas.editar_etapa(id, nome or None, data or None, pista or None)

    @classmethod
    def remover_etapa(cls):
        """Remove uma etapa existente."""
        cls.listar_etapas()
        id = int(input("ID da etapa a remover: "))
        Etapas.remover_etapa(id)

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
        id = int(input("Informe o id do piloto a ser alterado: "))
        nome = input("Informe o novo nome: ")
        equipe = input("Informe o novo equipe: ")
        pontuacao = input("Informe o novo pontuacao: ")
        View.piloto_atualizar(id, nome, equipe, pontuacao)
    
    @classmethod
    def piloto_excluir(cls):
        cls.listar_pilotos()
        id = int(input("Informe o id do piloto a ser excluído: "))
        View.piloto_excluir(id)

    @classmethod
    def gerenciar_resultados(cls):
        """Exibe o menu de gerenciamento de resultados."""
        print("Gerenciamento de Resultados (em desenvolvimento)")

    @classmethod
    def gerenciar_estatisticas(cls):
        """Exibe o menu de gerenciamento de estatísticas."""
        print("Gerenciamento de Estatísticas (em desenvolvimento)")

    @classmethod
    def gerenciar_vendas(cls):
        """Exibe o menu de gerenciamento de vendas."""
        while True:
            print("\n=== Gerenciamento de Vendas ===")
            print("1. Listar Vendas")
            print("2. Adicionar Venda")
            print("3. Remover Venda")
            print("4. Voltar")

            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                UI.listar_vendas()
            elif opcao == "2":
                cls.adicionar_venda()
            elif opcao == "3":
                cls.remover_venda()
            elif opcao == "4":
                return
            else:
                print("Opção inválida. Tente novamente.")

    @classmethod
    def listar_vendas(cls):
        """Lista todas as vendas cadastradas."""
        vendas = View.listar_vendas()
        if not vendas:
            print("Nenhuma venda cadastrada.")
        else:
            for venda in vendas:
                print(venda)

    @classmethod
    def adicionar_venda(cls):
        """Adiciona uma nova venda."""
        etapa_id = input("Informe o ID da etapa: ")
        dias = input("Informe os dias do ingresso: ")
        quantidade = input("Informe a quantidade de ingressos: ")
    
        nova_venda = View.criar_ingresso(etapa_id, dias, quantidade)
        View.adicionar_venda(nova_venda)
    
        print("Venda adicionada com sucesso!")

    @classmethod
    def remover_venda(cls):
        """Remove uma venda existente."""
        cls.listar_vendas()
        id_venda = input("Informe o ID da venda a ser removida: ")
        Venda.remover_venda(id_venda)
        print("Venda removida com sucesso!")

UI.main()
