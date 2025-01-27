def menu_etapas(dados):
    etapas = dados.get("etapas", [])
    while True:
        if not etapas:
            print("\nNenhuma etapa cadastrada.")
            print("1. Voltar")
            opcao = input("Selecione uma opção: ")

            if opcao == "1":
                return
            else:
                print("Opção inválida. Tente novamente.")
        else:
            print("\n✓ Etapas Cadastradas:")
            for idx, etapa in enumerate(etapas, 1):
                print(f"{idx}. {etapa['nome']} - {etapa['data']}")
            print(f"{len(etapas) + 1}. Voltar")

            opcao = input("Selecione uma opção: ")

            if opcao.isdigit() and 1 <= int(opcao) <= len(etapas):
                exibir_detalhes_etapa(etapas[int(opcao) - 1])
            elif opcao == str(len(etapas) + 1):
                return
            else:
                print("Opção inválida. Tente novamente.")
