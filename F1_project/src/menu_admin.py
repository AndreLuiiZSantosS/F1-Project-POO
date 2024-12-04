def exibir_menu_admin(dados):
    while True:
        print("\n✓ Menu Admin")
        print("1. Editar etapas")
        print("2. Editar estatísticas")
        print("3. Voltar")
        opcao = input("Selecione uma opção: ")

        if opcao == "1":
            from src.etapas import menu_admin_etapas
            menu_admin_etapas(dados)
        elif opcao == "2":
            from src.estatisticas import menu_admin_estatisticas
            menu_admin_estatisticas(dados)
        elif opcao == "3":
            break
        else:
            print("Opção inválida. Tente novamente.")