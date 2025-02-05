import json

# Caminho do banco de dados de resultados
CAMINHO_BD_RESULTADOS = "../data/resultados.json"

def carregar_resultados():
    """Carrega os dados de resultados do arquivo JSON."""
    try:
        with open(CAMINHO_BD_RESULTADOS, "r") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return {"resultados": []}
    except json.JSONDecodeError:
        print("Erro ao carregar o banco de dados de resultados.")
        return {"resultados": []}

def salvar_resultados(dados):
    """Salva os dados de resultados no arquivo JSON."""
    try:
        with open(CAMINHO_BD_RESULTADOS, "w") as arquivo:
            json.dump(dados, arquivo, indent=4)
    except Exception as e:
        print(f"Erro ao salvar o banco de dados de resultados: {e}")

def listar_resultados():
    """Lista todos os resultados cadastrados."""
    dados = carregar_resultados()
    resultados = dados.get("resultados", [])
    if not resultados:
        print("Nenhum resultado cadastrado.")
        return
    print("\n✓ Resultados Registrados:")
    for i, resultado in enumerate(resultados, start=1):
        print(f"{i}. {resultado['etapa']} | {resultado['piloto']} ({resultado['equipe']}): P{resultado['posicao']}")

def adicionar_resultado():
    """Adiciona um novo resultado ao banco de dados."""
    dados = carregar_resultados()
    etapa = input("Nome da etapa: ")
    piloto = input("Nome do piloto: ")
    equipe = input("Nome da equipe: ")
    
    while True:
        try:
            posicao = int(input("Posição do piloto (número inteiro): "))
            break
        except ValueError:
            print("Erro: Digite um número inteiro válido para a posição.")
    
    dados["resultados"].append({"etapa": etapa, "piloto": piloto, "equipe": equipe, "posicao": posicao})
    salvar_resultados(dados)
    print("Resultado adicionado com sucesso!")
