from views import View
from models.etapas import Etapas
from templates.abrircontaUI import AbrirContaUI
from templates.manteringressoUI import ManterIngressoUI
from templates.simularCorrida import SimuladorCorrida

class UI:
    
    cliente_id = None
    cliente_nome = ""
    piloto_id = 0
    piloto_nome = ""
    is_admin = False

    @staticmethod
    def login():
        """Método para realizar o login."""
        username = input("Digite o nome de usuário: ")
        password = input("Digite a senha: ")

        cliente = View.cliente_autenticar(username, password)

        if username == "admin" and password == "admin":
            UI.is_admin = True
            print("Login como administrador realizado com sucesso!")
            return True
        elif cliente is not None:
            UI.cliente_id = cliente['id'] 
            UI.cliente_nome = cliente['nome']  
            UI.is_admin = False
            print(f"Login como usuário comum realizado com sucesso. Bem-vindo, {cliente['nome']}!")
            return True
        else:
            print("Usuário ou senha incorretos.")
            return False
    
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
        print("8. Gerenciar Campeonato de Construtores")
        print("9. Resetar Campeonato")
        print("10. Sair")
        return int(input("Informe uma opção: "))

    @staticmethod
    def menu_usuario():
        """Menu específico para usuários comuns."""
        print("\n===== Menu Usuário =====")
        print("1. Listar Pilotos")
        print("2. Listar Etapas")
        print("3. Comprar Ingresso")
        print("4. Meus ingressos")
        print("5. Ver corrida")
        print("6. Sair")
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
                while op != 10:  # 10 é a opção de sair no menu admin
                    op = UI.menu_admin()
                    if op == 1: 
                        UI.gerenciar_etapas()
                    elif op == 2: 
                        UI.adicionar_pilotos()
                    elif op == 3: 
                        UI.listar_pilotos()
                    elif op == 4: 
                        UI.piloto_atualizar()
                    elif op == 5: 
                        UI.piloto_excluir()
                    elif op == 6: 
                        UI.gerenciar_estatisticas()
                    elif op == 7: 
                        UI.gerenciar_vendas()
                    elif op == 8: 
                        UI.gerenciar_campeonato_construtores()
                    elif op == 9: 
                        UI.resetar_pontuacoes()
                    elif op == 10: 
                        print("Saindo...")
                    else: 
                        print("Opção inválida!")
            else:
                op = 0
                while op != 6:  
                    op = UI.menu_usuario()
                    if op == 1: 
                        UI.listar_pilotos()
                    elif op == 2: 
                        UI.listar_etapas()
                    elif op == 3: 
                        UI.comprar_ingresso()
                    elif op == 4: 
                        UI.listar_meus_ingressos()
                    elif op == 5: 
                        UI.simular_corrida()
                    elif op == 6: 
                        print("Saindo...")
                    else: 
                        print("Opção inválida!")
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
        etapas = View.etapa_listar()
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
        View.etapa_inserir(nome, data, pista)
        print("Etapa adicionada com sucesso!")

    @classmethod
    def editar_etapa(cls):
        """Edita uma etapa existente."""
        cls.listar_etapas()
        id = int(input("ID da etapa a editar: "))
        nome = input("Novo nome (deixe em branco para manter): ")
        data = input("Nova data (deixe em branco para manter): ")
        pista = input("Nova pista (deixe em branco para manter): ")
        View.etapa_atualizar(id, nome or None, data or None, pista or None)

    @classmethod
    def remover_etapa(cls):
        """Remove uma etapa existente."""
        cls.listar_etapas()
        id = int(input("ID da etapa a remover: "))
        View.etapa_excluir(id)

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
                pilotos_ordenados = sorted(pilotos, key=lambda piloto: piloto.pontuacao, reverse=True)
                print("\n===== Lista de Pilotos =====")
                for idx, piloto in enumerate(pilotos_ordenados, 1):
                    print(f"{idx}. {piloto.nome} ({piloto.equipe}) - Pontuação: {piloto.pontuacao}")

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
    def adicionar_venda(cls):
        """Adiciona uma nova venda."""
        etapa_id = input("Informe o ID da etapa: ")
        dias = input("Informe os dias do ingresso: ")
        quantidade = input("Informe a quantidade de ingressos: ")
    
        nova_venda = View.criar_ingresso(etapa_id, dias, quantidade)
        View.adicionar_venda(nova_venda)
    
        print("Venda adicionada com sucesso!")

    @classmethod
    def remover_ingresso(cls):
        id_venda = input("Informe o ID da venda a ser removida: ")
        View.excluir_ingresso(id_venda)  
    
    @classmethod
    def comprar_ingresso(cls):
        """Inicia o processo de compra de ingressos."""
        if cls.cliente_id is None:
            print("Nenhum usuário logado. Faça login para comprar ingressos.")
            return
        ManterIngressoUI.menu_vendas_usuario(cls.cliente_id)

    @classmethod
    def listar_meus_ingressos(cls):
        """Lista os ingressos comprados pelo usuário logado."""
        if cls.cliente_id is None:
            print("Nenhum usuário logado.")
            return

        # Obtém os ingressos do usuário logado
        ingressos = View.listar_ingressos_por_cliente(cls.cliente_id)

        if not ingressos:
            print("\nVocê não possui ingressos comprados.")
            return

        print("\n===== Meus Ingressos =====")
        for ingresso in ingressos:
            # Busca os detalhes da etapa usando a classe View
            etapa = View.buscar_etapa_por_id(ingresso.etapa_id)
            if etapa:
                print(f"ID: {ingresso.id} - Evento: {etapa['nome']} - Data: {etapa['data']}")
                print(f"Quantidade: {ingresso.quantidade} - Valor Total: R$ {ingresso.valor}")
                print("---------------------------")
            else:
                print(f"Ingresso para etapa desconhecida (ID: {ingresso.etapa_id})")
        
        delete = input("Digite 'Y' para deletar algum ingresso / Digite 'N' para voltar \n")
        if delete.lower == "y":
            UI.remover_ingresso()
        
    
    @classmethod
    def simular_corrida(cls):
        """Simula uma corrida e atualiza as pontuações dos pilotos."""
        pilotos = View.piloto_listar()  
        if not pilotos:
            print("Nenhum piloto cadastrado.")
            return

        print("\n===== Simulação de Corrida =====")
        pilotos_atualizados = SimuladorCorrida.simular_corrida(pilotos)
        
        for piloto in pilotos_atualizados:
            View.piloto_atualizar(piloto.id, piloto.nome, piloto.equipe, piloto.pontuacao)

        print("\nPontuações atualizadas com sucesso!")
    
    @classmethod
    def gerenciar_campeonato_construtores(cls):
        """Chama a view para gerenciar o campeonato de construtores."""
        View.gerenciar_campeonato_construtores()
    
    @classmethod
    def resetar_pontuacoes(cls):
        """Reseta as pontuações de todos os pilotos."""
        confirmacao = input("Tem certeza que deseja resetar as pontuações de todos os pilotos? (sim/não): ")
        if confirmacao.lower() == "sim":
            View.resetar_pontuacoes()  
            print("Pontuações dos pilotos resetadas com sucesso!")
        else:
            print("Operação cancelada.")

UI.main()
