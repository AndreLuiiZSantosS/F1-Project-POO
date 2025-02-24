import json
import os

class Etapa:
    def __init__(self, id, nome, data, pista, ingressos_disponiveis=100):
        self.id = id
        self.nome = nome
        self.data = data
        self.pista = pista
        self.ingressos_disponiveis = ingressos_disponiveis  # Quantidade de ingressos disponíveis

    def __str__(self):
        return (f"{self.id} - {self.nome} - {self.data} - {self.pista} | "
                f"Ingressos Disponíveis: {self.ingressos_disponiveis}")
class Etapas:
    objetos = []

    @classmethod
    def carregar_etapas(cls):
        """Carrega as etapas do arquivo JSON."""
        cls.objetos = []
        try:
            with open("etapas.json", mode="r", encoding="utf-8") as arquivo:
                objetos_json = json.load(arquivo)
                for obj in objetos_json:
                    e = Etapa(obj["id"], obj["nome"], obj["data"], obj["pista"])
                    cls.objetos.append(e)
        except FileNotFoundError:
            print(f"Arquivo '{"etapas.json"}' não encontrado. Criando um novo...")
            # Cria o diretório "../data" se ele não existir
            os.makedirs(os.path.dirname("etapas.json"), exist_ok=True)
            # Cria o arquivo com uma lista vazia
            with open("etapas.json", mode="w") as arquivo:
                json.dump([], arquivo)
        except json.JSONDecodeError:
            print(f"Erro ao decodificar o arquivo '{"etapas.json"}'.")

    @classmethod
    def salvar_etapas(cls):
        """Salva as etapas no arquivo JSON."""
        with open("etapas.json", mode="w") as arquivo:
            json.dump([vars(e) for e in cls.objetos], arquivo, indent=4)

    @classmethod
    def listar_etapas(cls):
        """Retorna a lista de etapas."""
        cls.carregar_etapas()
        return cls.objetos[:]

    @classmethod
    def buscar_etapa_por_id(cls, id):
        """Busca uma etapa pelo ID."""
        cls.carregar_etapas()
        for etapa in cls.objetos:
            if etapa.id == id:
                return etapa
        return None

    @classmethod
    def adicionar_etapa(cls, nome, data, pista):
        """Adiciona uma nova etapa."""
        cls.carregar_etapas()
        # Calcula o próximo ID
        id = 1 if not cls.objetos else max(e.id for e in cls.objetos) + 1
        nova_etapa = Etapa(id, nome, data, pista)
        cls.objetos.append(nova_etapa)
        cls.salvar_etapas()

    @classmethod
    def editar_etapa(cls, id, nome=None, data=None, pista=None):
        """Edita uma etapa existente."""
        etapa = cls.buscar_etapa_por_id(id)
        if etapa:
            etapa.nome = nome if nome else etapa.nome
            etapa.data = data if data else etapa.data
            etapa.pista = pista if pista else etapa.pista
            cls.salvar_etapas()

    @classmethod
    def remover_etapa(cls, id):
        """Remove uma etapa existente."""
        etapa = cls.buscar_etapa_por_id(id)
        if etapa:
            cls.objetos.remove(etapa)
            cls.salvar_etapas()

