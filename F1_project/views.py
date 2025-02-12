from models.piloto import Piloto, Pilotos
from etapas import Etapas  

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
