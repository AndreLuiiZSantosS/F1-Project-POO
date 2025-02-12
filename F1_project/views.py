from models.piloto import Piloto, Pilotos

class View:
    @staticmethod
    def usuario_admin():
        for c in Pilotos.listar_pilotos():
            if c.email == "admin": return None
        View.piloto_inserir("admin", "0000", "1234") 
    


    @staticmethod
    def piloto_listar():
        return Pilotos.listar()
    @staticmethod
    def piloto_inserir(nome, equipe, pontuacao):
        p = Piloto(0, nome, equipe, pontuacao)
        Pilotos.adicionar_piloto(p)
    