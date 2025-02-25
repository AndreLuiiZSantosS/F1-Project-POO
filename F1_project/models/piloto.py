import json

class Piloto:
    def __init__(self, id, nome, equipe, pontuacao):
        self.id = id
        self.nome = nome
        self.equipe = equipe
        self.pontuacao = pontuacao

    def __str__(self):
        return f"{self.id} - {self.nome} - {self.equipe} - {self.pontuacao}"

# Caminho do banco de dados de pilotos
#"pilotos.json" = "../data/pilotos.json"

class Pilotos:
    objetos = []
    @classmethod
    def carregar_pilotos(cls):
         # esvazia a lista de objetos
        cls.objetos = []
        try:
            with open("pilotos.json", mode="r", encoding="utf-8") as arquivo:
                # abre o arquivo com a lista de dicionários -> clientes_json
                clientes_json = json.load(arquivo)
                # percorre a lista de dicionários
                for obj in clientes_json:
                    # recupera cada dicionário e cria um objeto
                    c = Piloto(obj["id"], obj["nome"], obj["equipe"], obj["pontuacao"])
                    # insere o objeto na lista
                    cls.objetos.append(c)    
        except FileNotFoundError:
            pass

    @classmethod
    def salvar_pilotos(cls):
        # open - cria e abre o arquivo clientes.json
        # vars - converte um objeto em um dicionário
        # dump - pega a lista de objetos e salva no arquivo
        with open("pilotos.json", mode="w") as arquivo:
            json.dump(cls.objetos, arquivo, default = vars)

    @classmethod
    def listar_pilotos(cls):
         # abre a lista do arquivo
        cls.carregar_pilotos()
        # retorna a lista para a UI
        return cls.objetos
    
    @classmethod
    def listar_id(cls, id):
        cls.carregar_pilotos()
        # percorre a lista procurando o id    
        for x in cls.objetos:
            if x.id == id: return x
        return None

    @classmethod
    def adicionar_piloto(cls, obj):
        # abre a lista do arquivo
        cls.carregar_pilotos()
        # calcula o id do objeto
        id = 0
        for x in cls.objetos:
            if x.id > id: id = x.id
        obj.id = id + 1    
        # insere o objeto na lista
        cls.objetos.append(obj)
        # salva a lista no arquivo
        cls.salvar_pilotos()

    @classmethod
    def editar_piloto(cls, obj):
        x = cls.listar_id(obj.id)
        if x != None:
            cls.objetos.remove(x)
            cls.objetos.append(obj)
            #x.nome = obj.nome
            #x.email = obj.email
            #x.fone = obj.fone
            cls.salvar_pilotos()     
    @classmethod   
    def remover_piloto(cls, obj):
        x = cls.listar_id(obj.id)
        if x != None:
            cls.objetos.remove(x)
            cls.salvar_pilotos()     
    
    @classmethod
    def resetar_pontuacoes(cls):
        """Reseta as pontuações de todos os pilotos para zero."""
        cls.carregar_pilotos()
        for piloto in cls.objetos:
            piloto.pontuacao = 0
        cls.salvar_pilotos()
