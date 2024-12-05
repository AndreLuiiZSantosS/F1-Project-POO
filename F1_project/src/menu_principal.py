def exibir_menu_principal(dados):
    while True:
        print("\n✓ Menu Principal")
        print("1. Visualizar etapas")
        print("2. Visualizar estatísticas")
        print("3. Voltar ao Login")
        opcao = input("Selecione uma opção: ")

        if opcao == "1":
            from etapas import menu_etapas
            menu_etapas(dados)
        elif opcao == "2":
            from estatisticas import menu_estatisticas
            menu_estatisticas(dados)
        elif opcao == "3":
            return  # Volta ao login
        else:
            print("Opção inválida. Tente novamente.")