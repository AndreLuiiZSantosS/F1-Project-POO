import json
from models.ingresso import Ingresso

class Carrinho:
    def __init__(self, id):
        self.id = id
        self.itens = []  # Lista de itens no carrinho

    def adicionar_ingresso(self, ingresso):
        """Adiciona um ingresso ao carrinho."""
        self.itens.append(ingresso)

    def remover_ingresso(self, id_ingresso):
        """Remove um ingresso do carrinho."""
        self.itens = [item for item in self.itens if item.id != id_ingresso]

    def calcular_total(self):
        """Calcula o valor total do carrinho."""
        return sum(item.calcular_total() for item in self.itens)

    def __str__(self):
        return f"Carrinho {self.id} - Total: R$ {self.calcular_total():.2f}"

    def to_dict(self):
        """Converte o carrinho em um dicionário."""
        return {
            "id": self.id,
            "itens": [vars(item) for item in self.itens]
        }

    @classmethod
    def from_dict(cls, data):
        """Cria um carrinho a partir de um dicionário."""
        carrinho = cls(data["id"])
        for item_data in data["itens"]:
            carrinho.adicionar_ingresso(Ingresso(**item_data))
        return carrinho


class Carrinhos:
    objetos = []  # Lista de carrinhos

    @classmethod
    def carregar_carrinhos(cls):
        """Carrega a lista de carrinhos do arquivo JSON."""
        cls.objetos = []
        try:
            with open("carrinhos.json", mode="r") as arquivo:
                dados = json.load(arquivo)
                for obj in dados:
                    cls.objetos.append(Carrinho.from_dict(obj))
        except FileNotFoundError:
            pass

    @classmethod
    def salvar_carrinhos(cls):
        """Salva a lista de carrinhos no arquivo JSON."""
        with open("carrinhos.json", mode="w") as arquivo:
            json.dump([carrinho.to_dict() for carrinho in cls.objetos], arquivo, indent=4)

    @classmethod
    def listar_carrinhos(cls):
        """Retorna a lista de carrinhos."""
        cls.carregar_carrinhos()
        return cls.objetos

    @classmethod
    def buscar_por_id(cls, id):
        """Busca um carrinho pelo ID."""
        cls.carregar_carrinhos()
        for carrinho in cls.objetos:
            if carrinho.id == id:
                return carrinho
        return None

    @classmethod
    def adicionar_carrinho(cls, carrinho):
        """Adiciona um novo carrinho à lista."""
        cls.carregar_carrinhos()
        # Verifica se o ID já existe
        if cls.buscar_por_id(carrinho.id):
            raise ValueError(f"Já existe um carrinho com o ID {carrinho.id}.")
        cls.objetos.append(carrinho)
        cls.salvar_carrinhos()

    @classmethod
    def remover_carrinho(cls, id):
        """Remove um carrinho da lista."""
        cls.carregar_carrinhos()
        carrinho = cls.buscar_por_id(id)
        if not carrinho:
            raise ValueError(f"Carrinho com ID {id} não encontrado.")
        cls.objetos.remove(carrinho)
        cls.salvar_carrinhos()