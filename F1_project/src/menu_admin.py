def exibir_menu_admin():
    while True:
        print("\n=== Menu do Administrador ===")
        print("1. Gerenciar Etapas")
        print("2. Gerenciar Pilotos")
        print("3. Gerenciar Resultados")
        print("4. Gerenciar Vendas")
        print("5. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            from etapas import menu_admin_etapas
            menu_admin_etapas()
        elif opcao == "2":
            from pilotos import menu_admin_pilotos
            menu_admin_pilotos()
        elif opcao == "3":
            from resultados import menu_admin_resultados
            menu_admin_resultados()
        elif opcao == "4":
            from vendas import menu_admin_vendas
            menu_admin_vendas()
        elif opcao == "5":
            print("Saindo do menu administrativo.")
            break
        else:
            print("Opção inválida. Tente novamente.")
