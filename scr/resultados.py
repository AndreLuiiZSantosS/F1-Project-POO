def listar_resultados(dados):
    resultados = dados.get("resultados", [])
    if not resultados:
        print("Nenhum resultado cadastrado.")
        return
    print("\n✓ Resultados Registrados:")
    for resultado in resultados:
        print(f"- {resultado['etapa']} | {resultado['piloto']} ({resultado['equipe']}): {resultado['posicao']}")

def adicionar_resultado(dados):
    resultados = dados.get("resultados", [])
    etapa = input("Nome da etapa: ")
    piloto = input("Nome do piloto: ")
    equipe = input("Nome da equipe: ")
    posicao = input("Posição do piloto: ")
    resultados.append({"etapa": etapa, "piloto": piloto, "equipe": equipe, "posicao": posicao})
    print("Resultado adicionado com sucesso!")