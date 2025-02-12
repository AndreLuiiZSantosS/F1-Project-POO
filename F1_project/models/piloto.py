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
            with open("clientes.json", mode="r") as arquivo:
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
    def remover_piloto(cls, obj):
        x = cls.listar_id(obj.id)
        if x != None:
            cls.objetos.remove(x)
            cls.salvar_pilotos()     

    @classmethod
    def menu_admin_pilotos(cls):
        """Exibe o menu de gerenciamento de pilotos para o administrador."""
        while True:
            print("\n=== Gerenciamento de Pilotos ===")
            print("1. Listar Pilotos")
            print("2. Adicionar Piloto")
            print("3. Editar Piloto")
            print("4. Remover Piloto")
            print("5. Voltar")

            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                cls.listar_pilotos()
            elif opcao == "2":
                cls.adicionar_piloto()
            elif opcao == "3":
                cls.editar_piloto()
            elif opcao == "4":
                cls.remover_piloto()
            elif opcao == "5":
                return
            else:
                print("Opção inválida. Tente novamente.")