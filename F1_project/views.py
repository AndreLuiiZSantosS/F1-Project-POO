from models.piloto import Piloto, Pilotos

class View:
    @staticmethod
    def usuario_admin():
        for c in Pilotos.listar_pilotos():
            if c.equipe == "admin": return None
        View.piloto_inserir("admin", "0000", "1234") 
    


    @staticmethod
    def piloto_listar():
        return Pilotos.listar_pilotos()
    
    @staticmethod
    def piloto_inserir(nome, equipe, pontuacao):
        p = Piloto(0, nome, equipe, pontuacao)
        Pilotos.adicionar_piloto(p)
    
    @staticmethod
    def piloto_atualizar(id, nome, equipe, pontuacao):
        c = Piloto(id, nome, equipe, pontuacao)
        Pilotos.editar_piloto(c)
    
    @staticmethod
    def piloto_excluir(id):
        c = Piloto(id, "", "", "")
        Pilotos.remover_piloto(c)
    