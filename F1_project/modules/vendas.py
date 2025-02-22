from models.carrinho import Carrinho  # Importação corrigida
from models.ingresso import Ingresso
import json

class Venda:
    DB_VENDAS = "vendas.json"

    @staticmethod
    def carregar_dados():
        """Carrega as vendas do arquivo JSON."""
        try:
            with open(Venda.DB_VENDAS, mode="r") as arquivo:
                return json.load(arquivo)
        except FileNotFoundError:
            return []

    @staticmethod
    def salvar_dados(dados):
        """Salva as vendas no arquivo JSON."""
        with open(Venda.DB_VENDAS, mode="w") as arquivo:
            json.dump(dados, arquivo, indent=4)

    @staticmethod
    def comprar_ingresso(venda):
        """Registra uma nova venda."""
        vendas = Venda.carregar_dados()
        vendas.append(venda)
        Venda.salvar_dados(vendas)

    @staticmethod
    def listar_vendas():
        """Retorna a lista de vendas."""
        return Venda.carregar_dados()