class Carrinho:
    def __init__(self):

        self.itens = []  # Lista de ingressos no carrinho

    def adicionar_ingresso(self, ingresso):
        
        self.itens.append(ingresso)

    def calcular_total(self):
        
        return sum(ingresso.calcular_total() for ingresso in self.itens)

    def finalizar_compra(self):
        
        ingressos_comprados = self.itens.copy()
        self.itens.clear()  # Limpa o carrinho
        return ingressos_comprados

    def __str__(self):
        
        return "\n".join(str(ingresso) for ingresso in self.itens)