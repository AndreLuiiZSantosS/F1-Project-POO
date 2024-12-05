import json

# Definindo o caminho do banco de dados
CAMINHO_BANCO_DE_DADOS = "dados.json"

def carregar_dados():
    """Carrega os dados do banco de dados JSON."""
    try:
        with open(CAMINHO_BANCO_DE_DADOS, 'r') as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        print("Banco de dados não encontrado. Um novo arquivo será criado.")
        return {
            "pilotos": [],
            "resultados": [],
            "etapas": [],
              "construtores": [],
                "estatisticas": [] 
        }
    except json.JSONDecodeError:
        print("Erro ao decodificar o banco de dados. Inicializando banco vazio.")
        return {
            "pilotos": [],
            "resultados": [],
            "etapas": [],
            "construtores": [],
                "estatisticas": [] 
        }

def salvar_dados(dados):
    """Salva os dados no banco de dados JSON."""
    try:
        with open(CAMINHO_BANCO_DE_DADOS, 'w') as arquivo:
            json.dump(dados, arquivo, indent=4)
            print("Dados salvos com sucesso.")
    except Exception as e:
        print(f"Erro ao salvar os dados: {e}")
