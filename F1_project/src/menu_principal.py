def exibir_menu_principal():
    while True:
        print("\n✓ Menu Principal")
        print("1. Visualizar etapas")
        print("2. Visualizar estatísticas")
        print("3. Comprar ingressos")
        print("4. Voltar ao Login")
        opcao = input("Selecione uma opção: ")

        if opcao == "1":
            from etapas import menu_etapas
            menu_etapas()  # Cada módulo lida com seus próprios dados
        elif opcao == "2":
            from estatisticas import menu_estatisticas
            menu_estatisticas()  # Cada módulo lida com seus próprios dados
        elif opcao == "3":
            from vendas import menu_vendas_usuario
            menu_vendas_usuario()  # Cada módulo lida com seus próprios dados
        elif opcao == "4":
            return  # Volta ao login
        else:
            print("Opção inválida. Tente novamente.")
