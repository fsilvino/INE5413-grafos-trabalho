class Aresta:

    def __init__(self, v1, v2, peso):
        self.uid = Aresta.gerarIdAresta(v1, v2)
        self.v1 = v1
        self.v2 = v2
        self.peso = peso

    def obterOutraParte(self, v):
        return self.v1 if self.v1.numero != v.numero else self.v2

    def gerarIdAresta(v1, v2):
        return f'{min(v1.numero, v2.numero)}.{max(v1.numero, v2.numero)}'
    gerarIdAresta = staticmethod(gerarIdAresta)