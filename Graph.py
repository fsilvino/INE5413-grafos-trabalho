from Vertex import Vertex
from VertexAnalysed import VertexAnalysed
from queue import Queue
# from random import randint
import random

class Graph:

    def __init__(self):
        self.vertices = []
        self.numOfVertices = 0
        self.numOfEdges = 0
        self.loaded = False
        #RETIRAR ANTES DE ENTRAGAR TRABALHO
        self.ler("fln_pequena.net")

    def show_graph(self):
        for v in self.vertices:
            print(str(v.number) + ": " + ", ".join(map(lambda x: str(x.number), v.relationships)))

    def isLoaded(self):
        return self.loaded

    def ler(self, arquivo):
        f = open(arquivo, "r", encoding='utf-8')
        lines = f.readlines()
        f.close()
        self.loadVertices(lines)
        self.loadRelationships(lines)
        self.fileLoaded = True


    def loadVertices(self, lines):
        self.vertices.clear()
        self.numOfVertices = int(lines[0].split(" ")[1])
        for i in range(1, self.numOfVertices + 1):
            line = lines[i]
            spaceIndex = line.index(" ")
            vertexNumber = int(line[0:spaceIndex])
            startIndex = spaceIndex + 2
            endIndex = len(line)-2
            label = line[startIndex:endIndex]
            self.vertices.append(Vertex(vertexNumber, label))


    def loadRelationships(self, lines):
        self.numOfEdges = 0
        for i in range(self.numOfVertices + 2, len(lines)):
            values = lines[i].split(" ")

            originVertex = self.vertices[int(values[0]) - 1]
            destinationVertex = self.vertices[int(values[1]) - 1]
            weight = 1
            if (len(values) >= 3):
                weight = float(values[2])

            # nesse caso, self.numOfEdges esta sendo usado como identificador unico do relacionamento
            originVertex.addRelationship(destinationVertex, weight, self.numOfEdges)
            destinationVertex.addRelationship(originVertex, weight, self.numOfEdges)

            self.numOfEdges = self.numOfEdges + 1


    def qtdVertices(self):
        return self.numOfVertices


    def qtdArestas(self):
        return self.numOfEdges


    def grau(self, v):
        return len(self.vertices[v-1].relationships)


    def rotulo(self, v):
        return self.vertices[v-1].label


    def vizinhos(self, v):
        return self.vertices[v-1].relationships


    def haAresta(self, u, v):
        return self.vertices[u-1].isNeighborOf(v) or self.vertices[v-1].isNeighborOf(u)


    def peso(self, u, v):
        relationship = self.vertices[u-1].findRelationship(v)
        if (relationship != None):
            return relationship.weight

        relationship = self.vertices[v-1].findRelationship(u)
        if (relationship != None):
            return relationship.weight

        return float("inf")

    # Este método foi implementado seguindo o pseudocódigo disponibilizado nas anotações da disciplina.
    # Mesmo não utilizando a estrutura de ancestrais para efeitos práticos, a mesma foi adicionada para uma implementação completa do exemplo
    def realizarBuscaEmLargura(self, s):
        # utiliza o número de vértices para inicializar os itens dos arrays com os valores default
        numVertices = self.qtdVertices()
        visitados = [False] * numVertices
        custos = [float("inf")] * numVertices
        ancestrais = [None] * numVertices

        # define os valores para o vértice inicial
        visitados[s - 1] = True
        custos[s - 1] = 0

        # estrutura de dados utilizada para a impressão do resultado conforme requisito do trabalho
        resultado = [[s]]

        # inicializa a fila que é utilizada para a busca em largura, adicionando o índice do array que guarda os vértices no grafo
        fila = Queue()
        fila.put(s - 1)

        while not fila.empty():
            u = fila.get()

            # o método vizinhos() recebe o número do vértice, portando precisa somar 1 ao índice do array
            for verticeDestino in self.vizinhos(u + 1):

                # passa por cada vizinho e verifica se o mesmo ainda não foi visitado
                v = verticeDestino.number - 1
                if not visitados[v]:

                    # marca o vizinho como visitado, calcula seu custo e seta seu ancestral
                    visitados[v] = True
                    custo = custos[u] + 1
                    custos[v] = custo
                    ancestrais[v] = u

                    # atualiza a estrutura de dados do resultado para impressão do mesmo posteriormente
                    if custo >= len(resultado):
                        resultado.append([])
                    resultado[custo].append(v + 1)

                    # adiciona o vértice na fila para visitar seus vizinhos
                    fila.put(v)

        return resultado

    # Apenas mostra o resultado no console conforme requisito do trabalho, recebendo o resultado obtido com o método realizarBuscaEmLargura()
    def mostrarResultadoBuscaEmLargura(self, resultado):
        for nivel, vertices in enumerate(resultado):
            print(str(nivel) + ": " + ",".join(map(str, vertices)))

    # Procura de ciclos eulerianos utilizando algoritmo de Hierholzer
    def procuraCicloEuleriano(self):
        # arestasVisitadas = [False] * self.qtdArestas()
        # posicao inicial escolhida arbitrariamente
        posicaoInicial = random.randint(0, self.qtdVertices()-1)
        verticeInicial = self.vertices[posicaoInicial]
        ciclo = []

        x = self.buscaSubcicloEuleriano(verticeInicial, ciclo)

        print("Vertice inicial:", end="")
        print(verticeInicial.number)
        if x is not None:
            print("Achou ciclo")
            for i in x:
                print(i.number, end=", ")
        else:
            print("Retornou nulo")
        print("")
        print("Acabou de listar o ciclo")
        print("")
        return None

    def buscaSubcicloEuleriano(self, v, ciclo):
        arestasVisitadas = [False] * self.qtdArestas()
        ciclo = []
        ciclo.append(v)
        t =v # variavel t serve como comparativo para saber se um ciclo foi fechado ou nao
        # procurar maneira de fazer do/while
        busca = True
        while(busca):
            if False not in arestasVisitadas:
            # if False not in arestasVisitadas[v.number-1 :: len(v.relationships)]:
                # retorna nulo
                return None
            else:
                keysRelationsList = list(v.relationships.keys())
                randomKey = random.randint(0, len(keysRelationsList)-1)
                key = keysRelationsList[randomKey] # key eh do tipo Vertex
                u = v.relationships[key]
                # marca aresta como vistitada
                arestasVisitadas[u.uid] = True
                #v recebe vertice da outra ponta da aresta
                v= u.destinationVertex
                # ciclo recebe novo vertice
                ciclo.append(u.destinationVertex)
            if(v == t):
                busca = False
        return ciclo
