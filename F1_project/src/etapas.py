import os
import json

# Caminho relativo ao diretório do projeto
CAMINHO_ETAPAS = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "etapas.json")

def carregar_etapas():
    """Carrega as etapas do arquivo etapas.json ou cria o arquivo se não existir."""
    if not os.path.exists(os.path.dirname(CAMINHO_ETAPAS)):
        os.makedirs(os.path.dirname(CAMINHO_ETAPAS))  # Cria a pasta data se não existir

    if not os.path.exists(CAMINHO_ETAPAS):
        # Cria o arquivo etapas.json vazio com estrutura padrão
        with open(CAMINHO_ETAPAS, "w") as arquivo:
            json.dump({"etapas": []}, arquivo, indent=4)
        print("Arquivo etapas.json criado.")

    with open(CAMINHO_ETAPAS, "r") as arquivo:
        return json.load(arquivo)

def salvar_etapas(dados):
    """Salva os dados das etapas no arquivo etapas.json"""
    with open(CAMINHO_ETAPAS, "w") as arquivo:
        json.dump(dados, arquivo, indent=4)
    print("Dados de etapas salvos com sucesso!")


def menu_etapas(dados):
    etapas = dados.get("etapas", [])
    while True:
        if not etapas:
            print("\nNenhuma etapa cadastrada.")
            print("1. Voltar")
            opcao = input("Selecione uma opção: ")

            if opcao == "1":
                return  # Volta ao menu principal
            else:
                print("Opção inválida. Tente novamente.")
        else:
            print("\n✓ Etapas Cadastradas:")
            for idx, etapa in enumerate(etapas, 1):
                print(f"{idx}. {etapa['nome']} - {etapa['data']}")
            print(f"{len(etapas) + 1}. Voltar")

            opcao = input("Selecione uma opção: ")

            if opcao == str(len(etapas) + 1):
                return  # Volta ao menu principal
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
            adicionar_etapa(etapas, salvar_etapas, dados)
        elif opcao == "2":
            editar_etapa(etapas, salvar_etapas, dados)
        elif opcao == "3":
            excluir_etapa(etapas, salvar_etapas, dados)
        elif opcao == "4":
            break
        else:
            print("Opção inválida.")


def adicionar_etapa(etapas, salvar_dados, dados):
    nome = input("Nome da etapa: ")
    data = input("Data da etapa: ")
    etapas.append({"nome": nome, "data": data, "resultados": []})
    print("Etapa adicionada com sucesso!")
    salvar_dados(dados)  # Salva mudanças imediatamente


def editar_etapa(etapas, salvar_dados, dados):
    for idx, etapa in enumerate(etapas, 1):
        print(f"{idx}. {etapa['nome']} - {etapa['data']}")
    opcao = input("Selecione uma etapa para editar ou 'voltar': ")
    if opcao.isdigit() and 1 <= int(opcao) <= len(etapas):
        etapa = etapas[int(opcao) - 1]
        etapa["nome"] = input(f"Novo nome ({etapa['nome']}): ") or etapa["nome"]
        etapa["data"] = input(f"Nova data ({etapa['data']}): ") or etapa["data"]
        print("Etapa atualizada!")
        salvar_dados(dados)  # Salva mudanças imediatamente
    elif opcao.lower() == "voltar":
        return
    else:
        print("Opção inválida.")


def excluir_etapa(etapas, salvar_dados, dados):
    for idx, etapa in enumerate(etapas, 1):
        print(f"{idx}. {etapa['nome']} - {etapa['data']}")
    opcao = input("Selecione uma etapa para excluir ou 'voltar': ")
    if opcao.isdigit() and 1 <= int(opcao) <= len(etapas):
        etapas.pop(int(opcao) - 1)
        print("Etapa excluída com sucesso!")
        salvar_dados(dados)  # Salva mudanças imediatamente
    elif opcao.lower() == "voltar":
        return
    else:
        print("Opção inválida.")
