import json

# Caminho do banco de dados de pilotos
CAMINHO_BD_PILOTOS = "data/pilotos.json"

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
    for piloto in pilotos:
        print(f"- {piloto['nome']} ({piloto['equipe']})")

def adicionar_piloto():
    """Adiciona um novo piloto ao banco de dados."""
    dados = carregar_pilotos()
    pilotos = dados.get("pilotos", [])
    nome = input("Nome do piloto: ")
    equipe = input("Nome da equipe: ")
    pilotos.append({"nome": nome, "equipe": equipe})
    salvar_pilotos(dados)
    print("Piloto adicionado com sucesso!")

def editar_piloto():
    """Edita as informações de um piloto cadastrado."""
    dados = carregar_pilotos()
    pilotos = dados.get("pilotos", [])
    listar_pilotos()
    opcao = input("Selecione o índice do piloto para editar ou 'voltar': ")
    if opcao.isdigit() and 1 <= int(opcao) <= len(pilotos):
        piloto = pilotos[int(opcao) - 1]
        piloto["nome"] = input(f"Novo nome ({piloto['nome']}): ") or piloto["nome"]
        piloto["equipe"] = input(f"Nova equipe ({piloto['equipe']}): ") or piloto["equipe"]
        salvar_pilotos(dados)
        print("Piloto atualizado!")
    elif opcao.lower() == "voltar":
        return
    else:
        print("Opção inválida.")
