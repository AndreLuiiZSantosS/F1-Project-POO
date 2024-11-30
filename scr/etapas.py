def menu_etapas(dados):
    etapas = dados.get("etapas", [])
    if not etapas:
        print("Nenhuma etapa cadastrada.")
        return

    print("\n✓ Visualizar Etapas")
    for idx, etapa in enumerate(etapas, 1):
        print(f"{idx}. {etapa['nome']} - {etapa['data']}")

    opcao = input("\nSelecione uma etapa para ver detalhes ou 'voltar': ")
    if opcao.isdigit() and 1 <= int(opcao) <= len(etapas):
        exibir_detalhes_etapa(etapas[int(opcao) - 1])
    elif opcao.lower() == "voltar":
        return
    else:
        print("Opção inválida. Tente novamente.")

def exibir_detalhes_etapa(etapa):
    print(f"\nDetalhes da Etapa: {etapa['nome']}")
    print(f"Data: {etapa['data']}")
    print("Resultados: ")
    for resultado in etapa.get("resultados", []):
        print(f"- {resultado['piloto']} ({resultado['equipe']}): {resultado['posicao']}")

def menu_admin_etapas(dados):
    etapas = dados.get("etapas", [])
    while True:
        print("\n✓ Editar Etapas")
        print("1. Adicionar etapa")
        print("2. Editar etapa existente")
        print("3. Excluir etapa")
        print("4. Voltar")
        opcao = input("Selecione uma opção: ")

        if opcao == "1":
            adicionar_etapa(etapas)
        elif opcao == "2":
            editar_etapa(etapas)
        elif opcao == "3":
            excluir_etapa(etapas)
        elif opcao == "4":
            break
        else:
            print("Opção inválida.")

def adicionar_etapa(etapas):
    nome = input("Nome da etapa: ")
    data = input("Data da etapa: ")
    etapas.append({"nome": nome, "data": data, "resultados": []})
    print("Etapa adicionada com sucesso!")

def editar_etapa(etapas):
    for idx, etapa in enumerate(etapas, 1):
        print(f"{idx}. {etapa['nome']} - {etapa['data']}")
    opcao = input("Selecione uma etapa para editar ou 'voltar': ")
    if opcao.isdigit() and 1 <= int(opcao) <= len(etapas):
        etapa = etapas[int(opcao) - 1]
        etapa["nome"] = input(f"Novo nome ({etapa['nome']}): ") or etapa["nome"]
        etapa["data"] = input(f"Nova data ({etapa['data']}): ") or etapa["data"]
        print("Etapa atualizada!")
    elif opcao.lower() == "voltar":
        return
    else:
        print("Opção inválida.")

def excluir_etapa(etapas):
    for idx, etapa in enumerate(etapas, 1):
        print(f"{idx}. {etapa['nome']} - {etapa['data']}")
    opcao = input("Selecione uma etapa para excluir ou 'voltar': ")
    if opcao.isdigit() and 1 <= int(opcao) <= len(etapas):
        etapas.pop(int(opcao) - 1)
        print("Etapa excluída com sucesso!")
    elif opcao.lower() == "voltar":
        return
    else:
        print("Opção inválida.")