from Vertex import Vertex

class Graph:

    def __init__(self):
        self.vertices = []
        self.numOfVertices = 0
        self.numOfEdges = 0

    def show_graph(self):
        for v in self.vertices:
            print(str(v.number)+": ", end="")
            for r in v.relationships:
                print(str(r.destinationVertex.number)+", ", end="")
            print()

    def ler(self, arquivo):
        f = open(arquivo, "r", encoding='utf-8')
        lines = f.readlines()
        f.close()
        self.loadVertices(lines)
        self.loadRelationships(lines)


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

    def x_debug(self,vertex, number_visiteds, queue):
        print("Analisando: "+str(vertex.number))
        print("Visitados:", end="")
        print(number_visiteds)
        print("Fila:", end="")
        print("[",end="")
        for u in queue:
            print(str(u.number)+",", end="")
        print("]")
        print()

    def busca_largura(self, inicio, buscado, queue = [], vertex = None, number_visiteds = []):
        if vertex == None:
            vertex = self.search_start_vertex_by_number(inicio)

        self.x_debug(vertex, number_visiteds, queue)
        # result[] = vertex.number
        if vertex.number == buscado:
            return "Encontrou"
        else:
            if vertex.number not in number_visiteds:
                number_visiteds.append(vertex.number)
            for r in vertex.relationships:
                if r.destinationVertex.number not in number_visiteds:
                    queue.append(r.destinationVertex)
                    number_visiteds.append(r.destinationVertex.number)
        next_vertex = queue.pop(0)
        self.busca_largura(inicio, buscado, queue, next_vertex, number_visiteds)

    def busca_largura_2(self, inicio, buscado):
        fila = []
        distancia_inicial = 0
        visitados = []

        vertice_inicial = self.search_start_vertex_by_number(inicio)
        fila.append(vertice_inicial)
        while fila: # enquanto a nao estiver vazio...
            u = fila.pop(0)
            for r in u.relationships:
                if not r.foiVisitado:
                    r.foiVisitado = true
                    nova_distancia = distancia_antiga+1
                    visitados.append(r)
                    fila.append(r.destinationVertex)
