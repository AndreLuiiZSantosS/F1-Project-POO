import random

class SimuladorCorrida:
    PONTUACAO_F1 = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]

    @classmethod
    def simular_corrida(cls, pilotos):
        if not pilotos:
            print("Nenhum piloto disponível para a corrida.")
            return []

        random.shuffle(pilotos)

        for idx, piloto in enumerate(pilotos):
            if idx < len(cls.PONTUACAO_F1):
                pontuacao_corrida = cls.PONTUACAO_F1[idx]
                piloto.pontuacao += pontuacao_corrida  
                print(f"{piloto.nome} ({piloto.equipe}) chegou em {idx + 1}º lugar e ganhou {pontuacao_corrida} pontos.")
            else:
                print(f"{piloto.nome} ({piloto.equipe}) chegou em {idx + 1}º lugar e não pontuou.")

        cls.exibir_pontuacao_equipes(pilotos)

        return pilotos

    @classmethod
    def exibir_pontuacao_equipes(cls, pilotos):
        pontuacao_equipes = {}  

        for piloto in pilotos:
            if piloto.equipe in pontuacao_equipes:
                pontuacao_equipes[piloto.equipe] += piloto.pontuacao
            else:
                pontuacao_equipes[piloto.equipe] = piloto.pontuacao

        print("\n===== Pontuação das Equipes =====")
        for equipe, pontuacao in pontuacao_equipes.items():
            print(f"{equipe}: {pontuacao} pontos")