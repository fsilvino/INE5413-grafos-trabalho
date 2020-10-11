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
        self.ler("euleriano.net")
        # self.ler("fln_pequena_ciclo.net")

    def __reset(self):
        self.vertices = []
        self.numeroDeVertices = 0
        self.numeroDeArestas = 0
        self.carregado = False

    def mostrarGrafo(self):
        for v in self.vertices:
            print(str(v.numero) + ": " + ", ".join(map(lambda r: str(r.obterOutraParte(v).numero), v.relacoes.values())))

    def estaCarregado(self):
        return self.carregado

    def ler(self, arquivo):
        self.__reset()
        f = open(arquivo, "r", encoding='utf-8')
        linhas = f.readlines()
        f.close()
        self.__lerVertices(linhas)
        self.__lerRelacoes(linhas)
        self.carregado = True


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


    def __lerRelacoes(self, linhas):
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
            v1.adicionarRelacao(aresta)
            v2.adicionarRelacao(aresta)

            self.numeroDeArestas = self.numeroDeArestas + 1

    def qtdVertices(self):
        return self.numeroDeVertices

    def qtdArestas(self):
        return self.numeroDeArestas

    def grau(self, v):
        return len(self.vertices[v - 1].relacoes)

    def rotulo(self, v):
        return self.vertices[v - 1].rotulo

    def vizinhos(self, v):
        vertice = self.vertices[v - 1]
        return list(map(lambda r: r.obterOutraParte(vertice), vertice.relacoes.values()))

    def haAresta(self, u, v):
        return self.vertices[u - 1].ehVizinhoDe(self.vertices[v - 1])

    def peso(self, u, v):
        relacao = self.vertices[u - 1].encontrarRelacao(self.vertices[v - 1])
        return relacao.peso if relacao != None else float("inf")

    # Este método foi implementado seguindo o pseudocódigo disponibilizado nas anotações da disciplina.
    # Mesmo não utilizando a estrutura de ancestrais para efeitos práticos, a mesma foi adicionada para uma implementação completa do exemplo
    def realizarBuscaEmLargura(self, s):
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

    # Procura de ciclos eulerianos utilizando algoritmo de Hierholzer
    def procuraCicloEuleriano(self):
        arestasVisitadas = [False] * self.numeroDeArestas
        # posicao inicial escolhida arbitrariamente
        posicaoInicial = random.randint(0, self.numeroDeVertices - 1)
        verticeInicial = self.vertices[posicaoInicial]

        # print("Vertice inicial:", end="")
        # print(verticeInicial.numero)

        ciclo = self.buscaSubcicloEuleriano(verticeInicial, arestasVisitadas)
        return ciclo

        print("")
        print("Resultado: ")
        if ciclo[0]:
            for vertice in ciclo[1]:
                print(vertice.numero, end=", ")
        else:
            print("Retornou nulo")
        print("")
        print("Acabou de listar o ciclo")
        print("")
        return None

    def buscaSubcicloEuleriano(self, v, arestasVisitadas):
        ciclo = []
        ciclo.append(v)
        t = v # variavel t serve como comparativo para saber se um ciclo foi fechado ou nao
        # procurar maneira de fazer do/while
        busca = True
        while(busca):
            # if False not in arestasVisitadas:
            #     return (False, None)
            # else:
            # array com vertices que tem relacao com o vertice atual, ou seja, que tem arestas relacionadas
            listaVerticesDestino = list(map(lambda r: r.obterOutraParte(v), v.relacoes.values()))
            
            # escolher chave que nao foi visitada
            keysArestasNaoVisitadas = self.buscaArestasNaoVistadas(listaVerticesDestino, arestasVisitadas, v)

            # se keysArestasNaoVisitadas estiver vazio significa que todas as arestas do vertice foram visitadas
            # se todas as arestas foram visitadas, e nao fechou o ciclo, o algoritmo nao tem para onde ir
            if not keysArestasNaoVisitadas:
                return (False, None)
            else:
                randomKey = random.choice(keysArestasNaoVisitadas)
                verticeDestinoKey = listaVerticesDestino[randomKey] # verticeDestinoKey eh do tipo Vertex

                r = v.relacoes[verticeDestinoKey] #proxima aresta a ser visitada
                # marca aresta como vistitada
                arestasVisitadas[r.uid] = True
                # v recebe vertice da outra ponta da aresta
                v = r.obterOutraParte(v)
                # ciclo recebe novo vertice
                ciclo.append(v)
            # verificacao para definir fim do loop, emulando um "do while"
            if(v == t):
                busca = False
        # fim while

        # para cada vertice no ciclo, verificar se existe aresta nao vistitada
        i = 0
        for vertice in ciclo:
            for relacao in vertice.relacoes:
                # print("Passou aqui")
                if not arestasVisitadas[vertice.relacoes[relacao].uid]:
                    subCiclo = self.buscaSubcicloEuleriano(vertice, arestasVisitadas)
                    if not subCiclo[0]:
                        return (False,None)
                    # print("Achou um sub sub ciclo", end="")
                    # print(vertice.number)
                    # print("Ciclo atual: ")
                    # for x in ciclo:
                    #     print(x.number, end=", ")
                    # print("")
                    # print("Posicao: ", end="")
                    # print(i)
                    # for x in subCiclo[1]:
                    #     print(x.number, end=", ")
                    # print("")
                    ciclo[i:i+1] = subCiclo[1]
            i += 1
        return (True, ciclo)

    def buscaArestasNaoVistadas(self, listaVerticesDestino, arestasVisitadas, vertice):
        keysNaoVisitadas = []
        keyNaoVistida = 0
        for verticeDestino in listaVerticesDestino:
            if not arestasVisitadas[Aresta.gerarIdAresta(vertice, verticeDestino)]:
                keysNaoVisitadas.append(keyNaoVistida)
            keyNaoVistida = keyNaoVistida + 1
        return keysNaoVisitadas

    def mostrarResultadoBuscaCicloEuleriano(self, resultado):

        if resultado[0]:
            print("1")
            print(resultado)
            print(", ".join(map(lambda vertice: str(vertice.numero), resultado[1])))
            # for vertice in resultado[1]:
            #     print(vertice.number, end=", ")
        else:
            print("0")



    def novaBuscaCicloEuleriano(self):
        posicaoInicial = random.randint(0, self.numeroDeVertices - 1)
        verticeInicial = self.vertices[posicaoInicial]
        arestasVisitadas = {}

        ciclo = self.__novaBuscaSubcicloEuleriano(verticeInicial, arestasVisitadas)

        if (not ciclo[0]) or (len(arestasVisitadas) != self.numeroDeArestas):
            return (False, None)
        else:
            return ciclo

    def __novaBuscaSubcicloEuleriano(self, vertice, arestasVisitadas):
        ciclo = [vertice]
        t = vertice
        parar = False
        while (not parar):
            arestasNaoVisitadas = self.__novaBuscarPorArestasNaoVisitadas(vertice, arestasVisitadas)

            if not arestasNaoVisitadas:
                return (False, None)
            else:
                arestaVisitar = random.choice(arestasNaoVisitadas)
                arestasVisitadas[arestaVisitar] = True
                vertice = vertice.relacoes[arestaVisitar].obterOutraParte(vertice)
                ciclo.append(vertice) 

            if (t == vertice):
                parar = True

        for (i, vertice) in enumerate(ciclo):
            arestasNaoVisitadas = self.__novaBuscarPorArestasNaoVisitadas(vertice, arestasVisitadas)
            if arestasNaoVisitadas:
                subciclo = self.__novaBuscaSubcicloEuleriano(vertice, arestasVisitadas)
                if not subciclo[0]:
                    return (False, None)
                ciclo[i:i+1] = subciclo[1]

        return (True, ciclo)

    def __novaBuscarPorArestasNaoVisitadas(self, vertice, arestasVisitadas):
        naoVisitadas = []
        for aresta in vertice.relacoes.values():
            if not (aresta.uid in arestasVisitadas):
                naoVisitadas.append(aresta.uid)
        return naoVisitadas


    # matriz de adjacencia Floyd-Warshal
    # para para cruzamento de mesmo vertice, colocar zero, para vertices que nao estao ligados, colocar infinito
    def criaMatrizAdjacenciaFloydWarshall(self):
        # matriz = [[0] * * self.qtdVertices()] * self.qtdVertices() # Nao funciona bem. Arrays internos funcionam como objeto, sempre todos sao alterados
        matriz = [0] * self.numeroDeVertices
        # matriz[0][0] = 78
        # matriz = []
        i = 0
        for vertice in self.vertices:
            matriz[i] = [float("inf")] * self.numeroDeVertices
            matriz[i][i] = float(0)
            for verticeDestino in vertice.relacoes:
                matriz[vertice.numero - 1][verticeDestino.numero - 1] =  vertice.relacoes[verticeDestino].peso
            i += 1
        return matriz

    def floydWarshall(self):
        matrizBase = self.criaMatrizAdjacenciaFloydWarshall()
        # return matrizBase
        matriz = copy.copy(matrizBase)
        # k = 1

        # print(len(self.vertices))
        # print(range(0, len(self.vertices)-1))
        # i = 0
        # for v in self.vertices:
        for i in range(0, len(self.vertices)):
            for linha in range(0, len(matriz)):
            # for linha from matriz:
                if linha != i:
                    for coluna in range(0, len(matriz[linha])):
                        # print("Vertice: "+str(i))
                        # print("linha: "+str(linha))
                        # print("coluna: "+str(coluna))
                        # print("Valor atual: "+str(matriz[linha][coluna]))
                        # print("matriz[linha][i]: "+str(matriz[linha][i]))
                        # print("matriz[i][coluna]: "+str(matriz[i][coluna]))
                        # print("Soma: "+ str(matriz[linha][i] + matriz[i][coluna]))
                    # for coluna in linha:
                        x = matriz[linha][i] + matriz[i][coluna]
                        if x < matriz[linha][coluna]:
                            # print("Alterou!")
                            matriz[linha][coluna] = x
                            matriz[coluna][linha] = x
                        # print("")
                    #     break
                    # break
                # print("")
            # break

        # print(matrizBase)
        # print("")
        return matriz

    def exibeFloydWarshall(self, matriz):
        # print(matriz)
        for linha in range(0, len(matriz)):
            # print(linha)
            print(linha +1 , end=": ")
            print(", ".join(map(str, matriz[linha])))


    def dijkstra(self, s):
        # utiliza o número de vértices para inicializar os itens dos arrays com os valores default
        heap = makefheap()
        ancestrais = [None] * self.numeroDeVertices
        custos = [float("inf")] * self.numeroDeVertices

        # define os valores para o vértice inicial
        custos[s - 1] = 0
        fheappush(heap, (0, s - 1))
        
        while heap.num_nodes:
            item = fheappop(heap)
            custo_u = item[0]
            u = item[1]

            # se o custo do heap é diferente do custo que já está no array, é porque
            # o vértice já foi encontrado antes
            if custo_u != custos[u]:
                continue

            # o método vizinhos() recebe o número do vértice, portando precisa somar 1 ao índice do array
            for aresta in self.vertices[u].relacoes:
                v = aresta.obterOutraParte(self.vertices[u]).numero - 1
                
                custo = custos[u] + aresta.weight
                if custos[v] > custo:
                    custos[v] = custo
                    ancestrais[v] = u

                    # adiciona o vértice na fila para visitar seus vizinhos
                    fheappush(heap, (custo, v))

        return ancestrais