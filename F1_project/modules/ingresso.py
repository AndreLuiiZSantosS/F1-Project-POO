class Ingresso:
    def __init__(self, etapa_id, dias, quantidade, valor_unitario):
        
        self.etapa_id = etapa_id
        self.dias = dias
        self.quantidade = quantidade
        self.valor_unitario = valor_unitario

    def calcular_total(self):

        return self.quantidade * self.valor_unitario * len(self.dias)

    def __str__(self):
       
        return (f"Ingresso para Etapa ID {self.etapa_id} | "
                f"Dias: {', '.join(self.dias)} | "
                f"Quantidade: {self.quantidade} | "
                f"Valor Unitário: R$ {self.valor_unitario} | "
                f"Total: R$ {self.calcular_total()}")