from Vertice import Vertice
from Aresta import Aresta
from queue import Queue
import numpy as np
# from random import randint
import random
import copy
from fibheap import *

class Grafo:

    def __init__(self):
        self.__reset()
        #RETIRAR ANTES DE ENTRAGAR TRABALHO
        self.lerArquivo("euleriano.net")
        # self.ler("fln_pequena_ciclo.net")

    def __reset(self):
        self.vertices = []
        self.numeroDeVertices = 0
        self.numeroDeArestas = 0
        self.carregado = False

    def mostrarGrafo(self):
        self.__validarSeFoiCarregado()
        for v in self.vertices:
            print(str(v.numero) + ": " + ", ".join(map(lambda r: str(r.obterOutraParte(v).numero), v.arestas.values())))

    def lerArquivo(self, arquivo):
        self.__reset()
        f = open(arquivo, "r", encoding='utf-8')
        linhas = f.readlines()
        f.close()
        self.__lerVertices(linhas)
        self.__lerArestas(linhas)
        self.carregado = True

    def __validarSeFoiCarregado(self):
        if not self.carregado:
            raise Exception("Nenhum arquivo foi carregado! Primeiro carregue um arquivo para poder executar operações no grafo")

    def __lerVertices(self, linhas):
        self.numeroDeVertices = int(linhas[0].split(" ")[1])
        for i in range(1, self.numeroDeVertices + 1):
            linha = linhas[i]
            posicaoEspaco = linha.index(" ")
            numeroVertice = int(linha[0:posicaoEspaco])
            posicaoInicioRotulo = posicaoEspaco + 2
            posicaoFimRotulo = len(linha) - 2
            rotulo = linha[posicaoInicioRotulo:posicaoFimRotulo]
            self.vertices.append(Vertice(numeroVertice, rotulo))


    def __lerArestas(self, linhas):
        self.numeroDeArestas = 0
        for i in range(self.numeroDeVertices + 2, len(linhas)):
            valores = linhas[i].split(" ")

            v1 = self.vertices[int(valores[0]) - 1]
            v2 = self.vertices[int(valores[1]) - 1]
            peso = 1
            if (len(valores) >= 3):
                peso = float(valores[2])

            # visando economizar memória, por ser um grafo não dirigido,
            # criamos uma única vez a representação da relação e adicionamos ela
            # em ambos os vértices
            aresta = Aresta(v1, v2, peso)
            v1.adicionarAresta(aresta)
            v2.adicionarAresta(aresta)

            self.numeroDeArestas = self.numeroDeArestas + 1

    def qtdVertices(self):
        self.__validarSeFoiCarregado()
        return self.numeroDeVertices

    def qtdArestas(self):
        self.__validarSeFoiCarregado()
        return self.numeroDeArestas

    def grau(self, v):
        self.__validarSeFoiCarregado()
        return len(self.vertices[v - 1].arestas)

    def rotulo(self, v):
        self.__validarSeFoiCarregado()
        return self.vertices[v - 1].rotulo

    def vizinhos(self, v):
        self.__validarSeFoiCarregado()
        vertice = self.vertices[v - 1]
        return list(map(lambda r: r.obterOutraParte(vertice), vertice.arestas.values()))

    def haAresta(self, u, v):
        self.__validarSeFoiCarregado()
        return self.vertices[u - 1].ehVizinhoDe(self.vertices[v - 1])

    def peso(self, u, v):
        self.__validarSeFoiCarregado()
        aresta = self.vertices[u - 1].encontrarArestaPara(self.vertices[v - 1])
        return aresta.peso if aresta != None else float("inf")

    # Este método foi implementado seguindo o pseudocódigo disponibilizado nas anotações da disciplina.
    # Mesmo não utilizando a estrutura de ancestrais para efeitos práticos, a mesma foi adicionada para uma implementação completa do exemplo
    def realizarBuscaEmLargura(self, s):
        self.__validarSeFoiCarregado()

        # utiliza o número de vértices para inicializar os itens dos arrays com os valores default
        visitados = [False] * self.numeroDeVertices
        custos = [float("inf")] * self.numeroDeVertices
        ancestrais = [None] * self.numeroDeVertices

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
                v = verticeDestino.numero - 1
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

    def buscarCicloEuleriano(self):
        self.__validarSeFoiCarregado()
        
        posicaoInicial = random.randint(0, self.numeroDeVertices - 1)
        verticeInicial = self.vertices[posicaoInicial]
        arestasVisitadas = {}

        ciclo = self.__buscarSubcicloEuleriano(verticeInicial, arestasVisitadas)

        if (not ciclo[0]) or (len(arestasVisitadas) != self.numeroDeArestas):
            return (False, None)
        else:
            return ciclo

    def __buscarSubcicloEuleriano(self, vertice, arestasVisitadas):
        ciclo = [vertice]
        t = vertice
        parar = False
        while (not parar):
            arestasNaoVisitadas = self.__buscarPorArestasNaoVisitadas(vertice, arestasVisitadas)

            if not arestasNaoVisitadas:
                return (False, None)
            else:
                arestaVisitar = random.choice(arestasNaoVisitadas)
                arestasVisitadas[arestaVisitar] = True
                vertice = vertice.arestas[arestaVisitar].obterOutraParte(vertice)
                ciclo.append(vertice) 

            if t == vertice:
                parar = True

        for (i, vertice) in enumerate(ciclo):
            arestasNaoVisitadas = self.__buscarPorArestasNaoVisitadas(vertice, arestasVisitadas)
            if arestasNaoVisitadas:
                subciclo = self.__buscarSubcicloEuleriano(vertice, arestasVisitadas)
                if not subciclo[0]:
                    return (False, None)
                ciclo[i:i+1] = subciclo[1]

        return (True, ciclo)

    def __buscarPorArestasNaoVisitadas(self, vertice, arestasVisitadas):
        naoVisitadas = []
        for aresta in vertice.arestas.values():
            if not (aresta.uid in arestasVisitadas):
                naoVisitadas.append(aresta.uid)
        return naoVisitadas


    def mostrarResultadoBuscaCicloEuleriano(self, resultado):
        if resultado[0]:
            print("1")
            print(", ".join(map(lambda vertice: str(vertice.numero), resultado[1])))
        else:
            print("0")

    # matriz de adjacencia Floyd-Warshal
    # para para cruzamento de mesmo vertice, colocar zero, para vertices que nao estao ligados, colocar infinito
    def __criarMatrizAdjacenciaFloydWarshall(self):
        matriz = [0] * self.numeroDeVertices
        for (i, vertice) in enumerate(self.vertices):
            matriz[i] = [float("inf")] * self.numeroDeVertices
            matriz[i][i] = float(0)
            for aresta in vertice.arestas.values():
                verticeDestino = aresta.obterOutraParte(vertice)
                matriz[vertice.numero - 1][verticeDestino.numero - 1] = aresta.peso
        
        return matriz

    def buscarComFloydWarshall(self):
        self.__validarSeFoiCarregado()
        matriz = self.__criarMatrizAdjacenciaFloydWarshall()
        for indiceVerticeInserir in range(0, self.numeroDeVertices):
            for linha in range(0, self.numeroDeVertices):
                if linha != indiceVerticeInserir:
                    for coluna in range(0, linha + 1):
                        x = matriz[linha][indiceVerticeInserir] + matriz[indiceVerticeInserir][coluna]
                        if x < matriz[linha][coluna]:
                            matriz[linha][coluna] = x
                            matriz[coluna][linha] = x
        return matriz

    def exibirFloydWarshall(self, matriz):
        for linha in range(0, len(matriz)):
            print(linha + 1, end=": ")
            print(", ".join(map(str, matriz[linha])))


    def buscarCaminhoMinimoComDijkstra(self, s):
        self.__validarSeFoiCarregado()
        
        heap = makefheap()
        caminhos = []
        for _ in range(0, self.numeroDeVertices):
            caminhos.append([float("inf"), []])

        # define os valores para o vértice inicial
        caminhos[s - 1][0] = 0
        caminhos[s - 1][1].append(s)
        fheappush(heap, (0, s - 1))
        
        while heap.num_nodes:
            item = fheappop(heap)
            custo_u = item[0]
            u = item[1]

            # se o custo do heap é diferente do custo que já está no array, é porque
            # o vértice já foi encontrado antes
            if custo_u != caminhos[u][0]:
                continue

            # o método vizinhos() recebe o número do vértice, portando precisa somar 1 ao índice do array
            for aresta in self.vertices[u].arestas.values():
                v = aresta.obterOutraParte(self.vertices[u]).numero - 1
                
                custo = caminhos[u][0] + aresta.peso
                if caminhos[v][0] > custo:
                    caminhos[v][0] = custo
                    caminhos[v][1].extend(caminhos[u][1])
                    caminhos[v][1].append(v + 1)

                    # adiciona o vértice na fila para visitar seus vizinhos
                    fheappush(heap, (custo, v))

        return caminhos