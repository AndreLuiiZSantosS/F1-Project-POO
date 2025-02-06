import json

class Piloto:
    def __init__(self, nome, equipe, pontuacao):
        self.nome = nome
        self.equipe = equipe
        self.pontuacao = pontuacao

    def __str__(self):
        return f"{self.nome} - {self.equipe} - {self.pontuacao}"

# Caminho do banco de dados de pilotos
#"pilotos.json" = "../data/pilotos.json"

class Pilotos:

    @classmethod
    def carregar_pilotos(cls):
        """Carrega os dados dos pilotos do arquivo JSON."""
        try:
            with open("pilotos.json", "r") as arquivo:
                return json.load(arquivo)
        except FileNotFoundError:
            return {"pilotos": []}
        except json.JSONDecodeError:
            print("Erro ao carregar o banco de dados de pilotos.")
            return {"pilotos": []}

    @classmethod
    def salvar_pilotos(cls, dados):
        """Salva os dados dos pilotos no arquivo JSON."""
        try:
            with open("pilotos.json", "w") as arquivo:
                json.dump(dados, arquivo, indent=4)
        except Exception as e:
            print(f"Erro ao salvar o banco de dados de pilotos: {e}")

    @classmethod
    def listar_pilotos(cls):
        """Lista todos os pilotos cadastrados."""
        dados = cls.carregar_pilotos()
        pilotos = dados.get("pilotos", [])
        if not pilotos:
            print("Nenhum piloto cadastrado.")
            return
        print("\n✓ Pilotos Cadastrados:")
        for i, piloto in enumerate(pilotos, start=1):
            print(f"{i}. {piloto['nome']} - {piloto['equipe']} - {piloto['pontuacao']}")

    @classmethod
    def adicionar_piloto(cls):
        """Adiciona um novo piloto ao banco de dados."""
        dados = cls.carregar_pilotos()
        nome = input("Nome do piloto: ")
        equipe = input("Nome da equipe: ")
        pontuacao = int(input("Pontuação do Piloto: "))
        dados["pilotos"].append({"nome": nome, "equipe": equipe, "pontuacao": pontuacao})
        cls.salvar_pilotos(dados)
        print("Piloto adicionado com sucesso!")

    @classmethod
    def editar_piloto(cls):
        """Edita as informações de um piloto cadastrado."""
        dados = cls.carregar_pilotos()
        pilotos = dados.get("pilotos", [])
        cls.listar_pilotos()
        
        opcao = input("Selecione o índice do piloto para editar ou 'voltar': ")
        if opcao.isdigit() and 1 <= int(opcao) <= len(pilotos):
            indice = int(opcao) - 1
            pilotos[indice]["nome"] = input(f"Novo nome ({pilotos[indice]['nome']}): ") or pilotos[indice]["nome"]
            pilotos[indice]["equipe"] = input(f"Nova equipe ({pilotos[indice]['equipe']}): ") or pilotos[indice]["equipe"]
            pontuacao = input(f"Nova pontuação ({pilotos[indice]['pontuacao']}): ")
            if pontuacao:
                pilotos[indice]["pontuacao"] = int(pontuacao)
            dados["pilotos"] = pilotos  # Atualiza os dados antes de salvar
            cls.salvar_pilotos(dados)
            print("Piloto atualizado!")
        elif opcao.lower() == "voltar":
            return
        else:
            print("Opção inválida.")

    @classmethod
    def remover_piloto(cls):
        """Remove um piloto do banco de dados."""
        dados = cls.carregar_pilotos()
        pilotos = dados.get("pilotos", [])
        cls.listar_pilotos()
        
        opcao = input("Selecione o índice do piloto para remover ou 'voltar': ")
        if opcao.isdigit() and 1 <= int(opcao) <= len(pilotos):
            indice = int(opcao) - 1
            pilotos.pop(indice)
            dados["pilotos"] = pilotos
            cls.salvar_pilotos(dados)
            print("Piloto removido com sucesso!")
        elif opcao.lower() == "voltar":
            return
        else:
            print("Opção inválida.")

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