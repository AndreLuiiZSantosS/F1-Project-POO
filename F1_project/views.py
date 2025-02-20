from models.piloto import Piloto, Pilotos
from models.etapas import Etapas  
from F1_project.templates.manteringressoUI import Venda
from models.carrinho import Carrrinho, Carrinhos
from models.cliente import Cliente, Clientes

class View:
    @staticmethod
    def usuario_admin():
        """Cria um usuário admin se não existir."""
        for c in Pilotos.listar_pilotos():
            if c.equipe == "admin": 
                return None
        View.piloto_inserir("admin", "0000", "1234") 

    @staticmethod
    def piloto_listar():
        """Retorna a lista de pilotos."""
        return Pilotos.listar_pilotos()
    
    @staticmethod
    def piloto_inserir(nome, equipe, pontuacao):
        """Adiciona um novo piloto."""
        p = Piloto(0, nome, equipe, pontuacao)
        Pilotos.adicionar_piloto(p)
    
    @staticmethod
    def piloto_atualizar(id, nome, equipe, pontuacao):
        """Atualiza os dados de um piloto."""
        c = Piloto(id, nome, equipe, pontuacao)
        Pilotos.editar_piloto(c)
    
    @staticmethod
    def piloto_excluir(id):
        """Remove um piloto."""
        c = Piloto(id, "", "", "")
        Pilotos.remover_piloto(c)

    @staticmethod
    def etapa_listar():
        """Retorna a lista de etapas."""
        return Etapas.listar_etapas()
    
    @staticmethod
    def etapa_inserir(nome, data, pista):
        """Adiciona uma nova etapa."""
        Etapas.adicionar_etapa(nome, data, pista)
    
    @staticmethod
    def etapa_atualizar(id, nome=None, data=None, pista=None):
        """Atualiza os dados de uma etapa."""
        Etapas.editar_etapa(id, nome, data, pista)
    
    @staticmethod
    def etapa_excluir(id):
        """Remove uma etapa."""
        Etapas.remover_etapa(id)

    @staticmethod
    def listar_vendas():
        return Venda.listar_vendas()
    
    @staticmethod
    def adicionar_venda(venda):
        Venda.adicionar_venda(venda)
    
    @staticmethod
    def criar_carrinho():
        return Carrinho()
    
    @staticmethod
    def criar_ingresso(etapa_id, dias, qtd):
        return ingresso(etapa_id=etapa_id, dias=dias, qtd=qtd)

    @staticmethod
    def inserir_carrinho(id_produto):
        c = Carrrinho(id_produto)
        Carrinhos.inserir(c)
    @staticmethod
    def listar_carrinho():
        return Carrinhos.listar()
    @staticmethod
    def excluir_carrinho(id):
        c = Carrrinho(id)
        Carrinhos.excluir(c)

    @staticmethod
    def cliente_autenticar(nome, senha):
        for c in Clientes.listar():
            if c.nome == nome and c.senha == senha:
                return { "id" : c.id, "nome" : c.nome }
        return None    
    
    @staticmethod
    def cliente_listar():
        return Clientes.listar()
    @staticmethod
    def cliente_inserir(nome, senha):
        c = Cliente(0, nome, senha)
        Clientes.inserir(c)
    @staticmethod
    def cliente_atualizar(id, nome, senha):
        c = Cliente(id, nome, senha)
        Clientes.atualizar(c)
    @staticmethod
    def cliente_excluir(id):
        c = Cliente(id, "", "")
        Clientes.excluir(c)