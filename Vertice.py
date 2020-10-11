from Aresta import Aresta

class Vertice:

    def __init__(self, numero, rotulo):
        self.numero = numero
        self.rotulo = rotulo
        self.relacoes = {}

    def adicionarRelacao(self, aresta):
        self.relacoes[aresta.uid] = aresta

    def encontrarRelacao(self, v2):
        idAresta = Aresta.gerarIdAresta(self, v2)
        if (idAresta in self.relacoes):
            return self.relacoes[idAresta]
        return None

    def ehVizinhoDe(self, v2):
        return self.encontrarRelacao(v2) != None
