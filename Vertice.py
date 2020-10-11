from Aresta import Aresta

class Vertice:

    def __init__(self, numero, rotulo):
        self.numero = numero
        self.rotulo = rotulo
        self.arestas = {}

    def adicionarAresta(self, aresta):
        self.arestas[aresta.uid] = aresta

    def ehVizinhoDe(self, v2):
        return self.encontrarAresta(v2) != None

    def encontrarAresta(self, v2):
        idAresta = Aresta.gerarIdAresta(self, v2)
        if (idAresta in self.arestas):
            return self.arestas[idAresta]
        return None