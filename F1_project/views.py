from models.piloto import Piloto, Pilotos
from models.etapas import Etapas  
from models.cliente import Cliente, Clientes
from models.ingresso import Ingresso, Ingressos
from models.resultados import Resultado, Resultados


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
    def criar_ingresso(etapa_id, dias, qtd):
        return Ingresso(etapa_id, dias, qtd)
    
    @staticmethod
    def excluir_ingresso(id_venda):
        try:
            id_venda = int(id_venda)  
            Ingressos.remover_Ingresso(id_venda)  
        except ValueError:
            print("Erro: ID da venda deve ser um número inteiro.")

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

    @staticmethod
    def listar_ingressos_por_cliente(cliente_id):
        """Retorna os ingressos comprados por um cliente."""
        ingressos = Ingressos.listar_ingresso()  # Carrega todos os ingressos
        return [ingresso for ingresso in ingressos if ingresso.cliente_id == cliente_id]

    @staticmethod
    def buscar_etapa_por_id(etapa_id):
        """Retorna os detalhes de uma etapa pelo ID."""
        etapas = Etapas.listar_etapas()  # Carrega todas as etapas
        for etapa in etapas:
            if etapa.id == etapa_id:
                return {"nome": etapa.nome, "data": etapa.data}  # Retorna um dicionário com os detalhes
        return None

    @staticmethod
    def gerenciar_campeonato_construtores():
        """
        Chama os métodos do módulo de resultados para gerar (se necessário) 
        e exibir o campeonato de construtores.
        """
        Resultados.gerar_resultados_aleatorios()
        Resultados.exibir_resultado_construtores()
    
    @staticmethod
    def resetar_pontuacoes():
        """Reseta as pontuações de todos os pilotos para zero."""
        Pilotos.resetar_pontuacoes()
