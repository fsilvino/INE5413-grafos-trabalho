from Vertex import Vertex
from VertexAnalysed import VertexAnalysed
from queue import Queue

class Graph:

    def __init__(self):
        self.vertices = []
        self.numOfVertices = 0
        self.numOfEdges = 0
        self.loaded = False

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

            originVertex.addRelationship(destinationVertex, weight)
            destinationVertex.addRelationship(originVertex, weight)

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

    def search_start_vertex_by_number(self, number):
        vertex = None
        for v in self.vertices:
            if number == v.number:
                vertex = v
                break
        return vertex

    # def busca_largura(self, inicio, buscado, queue = [], vertex = None, numbers_visiteds = [], vertex_visiteds = {}, level = 0):
    #     if vertex == None:
    #         vertex = self.search_start_vertex_by_number(inicio)
    #         # searched = VertexAnalysed(vertex, 0)
    #
    #     # result[] = vertex.number
    #     self.x_debug(vertex, numbers_visiteds, queue)
    #     vertex_visiteds[level] = vertex
    #     if vertex.number == buscado:
    #         print(vertex_visiteds)
    #         return vertex_visiteds
    #     else:
    #         if searched.vertex.number not in numbers_visiteds:
    #             numbers_visiteds.append(vertex.number)
    #         for r in vertex.relationships:
    #             if r.destinationVertex.number not in numbers_visiteds:
    #                 queue.append(r.destinationVertex)
    #                 numbers_visiteds.append(r.destinationVertex.number)
    #     next_vertex = queue.pop(0)
    #     self.busca_largura(inicio, buscado, queue, next_vertex, numbers_visiteds, vertex_visiteds)

    def busca_largura(self, start_number, number_searched):
        queue = []
        visited = []
        result_search = {}

        start_vertex = self.search_start_vertex_by_number(start_number)
        first_item_analysed = VertexAnalysed(start_vertex, 0)
        queue.append(first_item_analysed)

        while queue: # enquanto a fila nao estiver vazia...
            current_item_analysed = queue.pop(0)

            if current_item_analysed.level not in result_search:
                result_search[current_item_analysed.level] = []

            result_search[current_item_analysed.level].append(current_item_analysed.vertex.number)

            if current_item_analysed.vertex.number != number_searched:
                visited.append(current_item_analysed.vertex.number)
                for relation in current_item_analysed.vertex.relationships:
                    relation_vertex = relation.destinationVertex

                    if relation_vertex.number not in visited:
                        visited.append(relation_vertex.number)
                        queue.append(VertexAnalysed(relation_vertex,current_item_analysed.level+1))
            else:
                return result_search

    def show_result_busca_largura(self, result_search):
        for key in result_search:
            print(key, end=": ")
            for value in result_search[key]:
                print(value, end=", ")
            print()

    
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