import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')

def carregar_dados():
    dados = {}
    arquivos = ["etapas.json", "pilotos.json", "resultados.json", "construtores.json"]
    for arquivo in arquivos:
        caminho = os.path.join(DATA_DIR, arquivo)
        if os.path.exists(caminho):
            with open(caminho, 'r') as f:
                dados[arquivo.split('.')[0]] = json.load(f)
        else:
            dados[arquivo.split('.')[0]] = []
    return dados

def salvar_dados(dados):
    for nome, conteudo in dados.items():
        caminho = os.path.join(DATA_DIR, f"{nome}.json")
        with open(caminho, 'w') as f:
            json.dump(conteudo, f, indent=4)