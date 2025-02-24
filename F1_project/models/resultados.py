import json

class Resultado:
    def __init__(self, id, pista ,pilotos):
        self.id = id
        self.pista = pista
        self.pilotos = pilotos
        self.itens = []  # Lista de itens no Resultado

    def __str__(self):
        return f"{self.id} - {self.pista} - {self.pilotos}"


class Resultados:
    objetos = []  # Lista de Resultados

    @classmethod
    def carregar_Resultados(cls):
        """Carrega a lista de Resultados do arquivo JSON."""
        cls.objetos = []
        try:
            with open("Resultados.json", mode="r") as arquivo:
                dados = json.load(arquivo)
                for obj in dados:
                    cls.objetos.append(Resultado.from_dict(obj))
        except FileNotFoundError:
            pass

    @classmethod
    def salvar_Resultados(cls):
        """Salva a lista de Resultados no arquivo JSON."""
        with open("Resultados.json", mode="w") as arquivo:
            json.dump([Resultado.to_dict() for Resultado in cls.objetos], arquivo, indent=4)

    @classmethod
    def listar_Resultados(cls):
        """Retorna a lista de Resultados."""
        cls.carregar_Resultados()
        return cls.objetos

    @classmethod
    def buscar_por_id(cls, id):
        """Busca um Resultado pelo ID."""
        cls.carregar_Resultados()
        for Resultado in cls.objetos:
            if Resultado.id == id:
                return Resultado
        return None

    @classmethod
    def adicionar_Resultado(cls, Resultado):
        """Adiciona um novo Resultado à lista."""
        cls.carregar_Resultados()
        # Verifica se o ID já existe
        if cls.buscar_por_id(Resultado.id):
            raise ValueError(f"Já existe um Resultado com o ID {Resultado.id}.")
        cls.objetos.append(Resultado)
        cls.salvar_Resultados()

    @classmethod
    def remover_Resultado(cls, id):
        """Remove um Resultado da lista."""
        cls.carregar_Resultados()
        Resultado = cls.buscar_por_id(id)
        if not Resultado:
            raise ValueError(f"Resultado com ID {id} não encontrado.")
        cls.objetos.remove(Resultado)
        cls.salvar_Resultados()

    @staticmethod
    def resetar_campeonato():
        """Reseta a tabela do campeonato, removendo todos os resultados existentes."""
        dados_iniciais = {"resultados": []}
        Resultados.salvar_Resultados(Resultados.CAMINHO_BD_RESULTADOS, dados_iniciais)
        print("Tabela do campeonato resetada com sucesso!")
