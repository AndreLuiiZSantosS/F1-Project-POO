import json

class Ingresso:
    def __init__(self, id,etapa_id, quantidade, valor):
        
        self.id = id
        self.etapa_id = etapa_id
        self.quantidade = quantidade
        self.valor = valor
    
    def __str__(self):
        return f"{self.etapa_id} - {self.quantidade} - {self.valor}"

class Ingressos:
    objetos = []
    @classmethod
    def carregar_ingresso(cls):
         # esvazia a lista de objetos
        cls.objetos = []
        try:
            with open("ingresso.json", mode="r") as arquivo:
                # abre o arquivo com a lista de dicionários -> clientes_json
                clientes_json = json.load(arquivo)
                # percorre a lista de dicionários
                for obj in clientes_json:
                    # recupera cada dicionário e cria um objeto
                    c = Ingresso(obj["id"] ,obj["etapa_id"], obj["quantidade"], obj["valor"])
                    # insere o objeto na lista
                    cls.objetos.append(c)    
        except FileNotFoundError:
            pass

    @classmethod
    def salvar_ingresso(cls):
        # open - cria e abre o arquivo clientes.json
        # vars - converte um objeto em um dicionário
        # dump - pega a lista de objetos e salva no arquivo
        with open("ingresso.json", mode="w") as arquivo:
            json.dump(cls.objetos, arquivo, default = vars)

    @classmethod
    def listar_ingresso(cls):
         # abre a lista do arquivo
        cls.carregar_ingresso()
        # retorna a lista para a UI
        return cls.objetos
    
    @classmethod
    def listar_id(cls, id):
        cls.carregar_ingresso()
        # percorre a lista procurando o id    
        for x in cls.objetos:
            if x.id == id: return x
        return None

    @classmethod
    def adicionar_Ingresso(cls, obj):
        # abre a lista do arquivo
        cls.carregar_ingresso()
        # calcula o id do objeto
        id = 0
        for x in cls.objetos:
            if x.id > id: id = x.id
        obj.id = id + 1    
        # insere o objeto na lista
        cls.objetos.append(obj)
        # salva a lista no arquivo
        cls.salvar_ingresso()

    @classmethod
    def editar_Ingresso(cls, obj):
        x = cls.listar_id(obj.id)
        if x != None:
            cls.objetos.remove(x)
            cls.objetos.append(obj)
            #x.nome = obj.nome
            #x.email = obj.email
            #x.fone = obj.fone
            cls.salvar_ingresso()     
    @classmethod   
    def remover_Ingresso(cls, obj):
        x = cls.listar_id(obj.id)
        if x != None:
            cls.objetos.remove(x)
            cls.salvar_ingresso()



