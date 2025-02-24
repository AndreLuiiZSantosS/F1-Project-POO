import random
#from models.piloto import piloto

class SimuladorCorrida:
    """Classe para simular corridas e atribuir pontuações aos pilotos."""

    PONTUACAO_F1 = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]

    @classmethod
    def simular_corrida(cls, pilotos):
        """
        Simula uma corrida e atribui pontuações aos pilotos.
        :param pilotos: Lista de objetos piloto.
        :return: Lista de pilotos com pontuações atualizadas.
        """
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

        return pilotos