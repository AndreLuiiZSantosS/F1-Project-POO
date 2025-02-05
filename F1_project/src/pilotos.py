import json

# Caminho do banco de dados de pilotos
CAMINHO_BD_PILOTOS = "../data/pilotos.json"

def carregar_pilotos():
    """Carrega os dados dos pilotos do arquivo JSON."""
    try:
        with open(CAMINHO_BD_PILOTOS, "r") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return {"pilotos": []}
    except json.JSONDecodeError:
        print("Erro ao carregar o banco de dados de pilotos.")
        return {"pilotos": []}

def salvar_pilotos(dados):
    """Salva os dados dos pilotos no arquivo JSON."""
    try:
        with open(CAMINHO_BD_PILOTOS, "w") as arquivo:
            json.dump(dados, arquivo, indent=4)
    except Exception as e:
        print(f"Erro ao salvar o banco de dados de pilotos: {e}")

def listar_pilotos():
    """Lista todos os pilotos cadastrados."""
    dados = carregar_pilotos()
    pilotos = dados.get("pilotos", [])
    if not pilotos:
        print("Nenhum piloto cadastrado.")
        return
    print("\n✓ Pilotos Cadastrados:")
    sorted_pilots = sorted(pilotos.items(), key=lambda x:x["pontuacao"])
    for i, pilotos in enumerate(pilotos, start=1):
        print(f"{i}. {sorted_pilots}")

def adicionar_piloto():
    """Adiciona um novo piloto ao banco de dados."""
    dados = carregar_pilotos()
    nome = input("Nome do piloto: ")
    equipe = input("Nome da equipe: ")
    pontuacao = input("Pontuacao do Piloto")
    dados["pilotos"].append({"nome": nome, "equipe": equipe, "pontuacao": pontuacao})
    salvar_pilotos(dados)
    print("Piloto adicionado com sucesso!")

def editar_piloto():
    """Edita as informações de um piloto cadastrado."""
    dados = carregar_pilotos()
    pilotos = dados.get("pilotos", [])
    listar_pilotos()
    
    opcao = input("Selecione o índice do piloto para editar ou 'voltar': ")
    if opcao.isdigit() and 1 <= int(opcao) <= len(pilotos):
        indice = int(opcao) - 1
        pilotos[indice]["nome"] = input(f"Novo nome ({pilotos[indice]['nome']}): ") or pilotos[indice]["nome"]
        pilotos[indice]["equipe"] = input(f"Nova equipe ({pilotos[indice]['equipe']}): ") or pilotos[indice]["equipe"]
        pilotos[indice]["pontuacao"] = input(f"Nova pontuacao ({pilotos[indice]['pontuacao']}): ") or pilotos[indice]["pontuacao"]
        dados["pilotos"] = pilotos  # Atualiza os dados antes de salvar
        salvar_pilotos(dados)
        print("Piloto atualizado!")
    elif opcao.lower() == "voltar":
        return
    else:
        print("Opção inválida.")

def remover_piloto():
    """Remove um piloto do banco de dados."""
    dados = carregar_pilotos()
    pilotos = dados.get("pilotos", [])
    listar_pilotos()
    
    opcao = input("Selecione o índice do piloto para remover ou 'voltar': ")
    if opcao.isdigit() and 1 <= int(opcao) <= len(pilotos):
        indice = int(opcao) - 1
        pilotos.pop(indice)
        dados["pilotos"] = pilotos
        salvar_pilotos(dados)
        print("Piloto removido com sucesso!")
    elif opcao.lower() == "voltar":
        return
    else:
        print("Opção inválida.")

# ========================= MENU DO ADMINISTRADOR =========================

def menu_admin_pilotos():
    """Exibe o menu de gerenciamento de pilotos para o administrador."""
    while True:
        print("\n=== Gerenciamento de Pilotos ===")
        print("1. Listar Pilotos")
        print("2. Adicionar Piloto")
        print("3. Editar Piloto")
        print("4. Remover Piloto")
        print("5. Voltar")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            listar_pilotos()
        elif opcao == "2":
            adicionar_piloto()
        elif opcao == "3":
            editar_piloto()
        elif opcao == "4":
            remover_piloto()
        elif opcao == "5":
            return
        else:
            print("Opção inválida. Tente novamente.")
