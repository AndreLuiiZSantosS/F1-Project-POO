def exibir_menu_admin():
    while True:
        print("\n===== Menu Administrador =====")
        print("1. Gerenciar Etapas")
        print("2. Gerenciar Pilotos")
        print("3. Gerenciar Resultados")
        print("4. Gerenciar Estatísticas")
        print("5. Gerenciar Vendas")
        print("6. Sair")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            menu_admin_etapas()
        elif opcao == "2":
            menu_admin_pilotos()
        elif opcao == "3":
            menu_admin_resultados()
        elif opcao == "4":
            menu_admin_estatisticas()
        elif opcao == "5":
            menu_admin_vendas()
        elif opcao == "6":
            print("Saindo do menu administrador...")
            break
        else:
            print("Opção inválida! Tente novamente.")
