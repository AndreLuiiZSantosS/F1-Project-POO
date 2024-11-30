def listar_pilotos(dados):
    pilotos = dados.get("pilotos", [])
    if not pilotos:
        print("Nenhum piloto cadastrado.")
        return
    print("\n✓ Pilotos Cadastrados:")
    for piloto in pilotos:
        print(f"- {piloto['nome']} ({piloto['equipe']})")

def adicionar_piloto(dados):
    pilotos = dados.get("pilotos", [])
    nome = input("Nome do piloto: ")
    equipe = input("Nome da equipe: ")
    pilotos.append({"nome": nome, "equipe": equipe})
    print("Piloto adicionado com sucesso!")

def editar_piloto(dados):
    pilotos = dados.get("pilotos", [])
    listar_pilotos(dados)
    opcao = input("Selecione o índice do piloto para editar ou 'voltar': ")
    if opcao.isdigit() and 1 <= int(opcao) <= len(pilotos):
        piloto = pilotos[int(opcao) - 1]
        piloto["nome"] = input(f"Novo nome ({piloto['nome']}): ") or piloto["nome"]
        piloto["equipe"] = input(f"Nova equipe ({piloto['equipe']}): ") or piloto["equipe"]
        print("Piloto atualizado!")
    elif opcao.lower() == "voltar":
        return
    else:
        print("Opção inválida.")