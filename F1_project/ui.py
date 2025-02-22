from .views import View
from .models.carrinho import Carrinho
from .models.ingresso import Ingresso
from .models.etapas import Etapas
from .models.cliente import Cliente, Clientes
from .models.piloto import Piloto, Pilotos
from .templates.abrircontaUI import AbrirContaUI
from .modules.vendas import Venda 


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
        elif autenticado is not None:
            UI.is_admin = False
            print("Login como usuário comum realizado com sucesso.")
        
        return autenticado is not None or (username == "admin" and password == "admin")
    
    @staticmethod
    def menu_admin():
        """Menu específico para administradores."""
        print("\n===== Menu Administrador =====")
        print("1. Gerenciar etapas")
        print("2. Adicionar Pilotos")
        print("3. Listar Pilotos")
        print("4. Editar Piloto")
        print("5. Excluir Piloto")
        print("6. Gerenciar Estatísticas")
        print("7. Gerenciar Vendas")
        print("8. Sair")
        return int(input("Informe uma opção: "))

    @staticmethod
    def menu_usuario():
        """Menu específico para usuários comuns."""
        print("\n===== Menu Usuário =====")
        print("1. Listar Pilotos")
        print("2. Listar Etapas")
        print("3. Comprar Ingresso")
        print("4. Sair")
        return int(input("Informe uma opção: "))

    @staticmethod
    def main():
        """Método principal para iniciar a aplicação."""
        abrirconta = input("Gostaria de criar uma conta? (sim/não) ")
        if abrirconta.lower() == "sim":
            AbrirContaUI.main()
        
        if UI.login():
            if UI.is_admin:
                op = 0
                while op != 8:  # 8 é a opção de sair no menu admin
                    op = UI.menu_admin()
                    if op == 1: UI.gerenciar_etapas()
                    elif op == 2: UI.adicionar_pilotos()
                    elif op == 3: UI.listar_pilotos()
                    elif op == 4: UI.piloto_atualizar()
                    elif op == 5: UI.piloto_excluir()
                    elif op == 6: UI.gerenciar_estatisticas()
                    elif op == 7: UI.gerenciar_vendas()
                    elif op == 8: print("Saindo...")
                    else: print("Opção inválida!")
            else:
                op = 0
                while op != 4:  # 4 é a opção de sair no menu usuário
                    op = UI.menu_usuario()
                    if op == 1: UI.listar_pilotos()
                    elif op == 2: UI.listar_etapas()
                    elif op == 3: UI.comprar_ingresso()
                    elif op == 4: print("Saindo...")
                    else: print("Opção inválida!")
        else:
            print("Usuário ou senha incorretos!")

    @classmethod
    def gerenciar_etapas(cls):
        """Exibe o menu de gerenciamento de etapas."""
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
        """Adiciona um novo piloto."""
        nome = input("Informe o nome: ")
        equipe = input("Informe a equipe: ")
        pontuacao = input("Informe a pontuação: ")
        View.piloto_inserir(nome, equipe, pontuacao)

    @classmethod
    def listar_pilotos(cls):
        """Lista todos os pilotos cadastrados."""
        pilotos = View.piloto_listar()
        if len(pilotos) == 0:
            print("Nenhum piloto cadastrado")
        else:    
            for piloto in pilotos:
                print(piloto)

    @classmethod 
    def piloto_atualizar(cls):
        """Atualiza os dados de um piloto."""
        cls.listar_pilotos()
        id = int(input("Informe o ID do piloto a ser alterado: "))
        nome = input("Informe o novo nome: ")
        equipe = input("Informe a nova equipe: ")
        pontuacao = input("Informe a nova pontuação: ")
        View.piloto_atualizar(id, nome, equipe, pontuacao)
    
    @classmethod
    def piloto_excluir(cls):
        """Exclui um piloto."""
        cls.listar_pilotos()
        id = int(input("Informe o ID do piloto a ser excluído: "))
        View.piloto_excluir(id)

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
                cls.listar_vendas()
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

    @classmethod
    def comprar_ingresso(cls):
        """Permite ao usuário comprar um ingresso."""
        print("Funcionalidade de compra de ingresso (em desenvolvimento)")


# Inicia a aplicação
UI.main()