from Grafo import Grafo

g = Grafo()

def solicitarOpcao(texto, min, max, maxTentativas = 3):
    tentativas = 1
    while tentativas <= maxTentativas:
        try:
            opcao = int(input(texto))
            if opcao >= min and opcao <= max:
                return opcao
            else:
                raise Exception()
        except:
            print("Opção inválida. Digite um valor entre " + str(min) + " e " + str(max))

        tentativas += 1

    return min - 1

def solicitarVertice(texto="Digite o número do vertice: "):
    try:
        v = solicitarOpcao(texto, 1, g.qtdVertices())
        if v > 0:
            return v
        else:
            print("Você não digitou um vértice válido")
    except Exception as ex:
        print(ex)
        return 0

def carregarArquivo():
    arquivoPadrao = "grafo.teste.net"
    arquivo = input("Digite o nome do arquivo (em branco carrega " + arquivoPadrao + "): ")
    try:
        if arquivo == "":
            arquivo = arquivoPadrao

        g.lerArquivo(arquivo)
        print("Arquivo " + arquivo + " carregado com sucesso.")
    except Exception as ex:
        print("Não foi possível ler o arquivo!")
        print(ex)


def mostrarQtdVertices():
    numVertices = g.qtdVertices()
    print("O grafo tem " + str(numVertices) + " vertices.")

def mostrarQtdArestas():
    numArestas = g.qtdArestas()
    print("O grafo tem " + str(numArestas) + " arestas.")

def verGrau():
    v = solicitarVertice()
    if v > 0:
        grau = g.grau(v)
        print(f'Grau do vértice {v}:', grau)

def verRotulo():
    v = solicitarVertice()
    if v > 0:
        rotulo = g.rotulo(v)
        print(f'Rótulo do vértice {v}:', rotulo)

def verVizinhos():
    v = solicitarVertice()
    if v > 0:
        vizinhos = g.vizinhos(v)
        print(f'Vizinhos do vértice {v}:', ", ".join(map(lambda v: str(v.numero), vizinhos)))

def verificarSeHaAresta():
    v = solicitarVertice("Digite o número do primeiro vértice: ")
    u = solicitarVertice("Digite o número do segundo vértice: ")
    if v > 0 and u > 0:
        haAresta = g.haAresta(u, v)
        nao = "" if haAresta else " não"
        print(f'O vértice {v}{nao} possui uma aresta para {u}')

def buscarEmLargura():
    try:
        inicio = solicitarOpcao("Digite o numero do vertice inicial: ", 1, g.qtdVertices())
        if inicio > 0:
            resultado = g.realizarBuscaEmLargura(inicio)
            print("Resultado da busca em largura:")
            g.mostrarResultadoBuscaEmLargura(resultado)
        else:
            print("Você não digitou um vértice inicial válido")
    except Exception as ex:
        print(ex)

def mostrarGrafo():
    try:
        print('Mostrando o grafo:')
        g.mostrarGrafo()
    except Exception as ex:
        print(ex)

def buscarCicloEuleriano():
    try:
        print("Resultado da busca por ciclo euleriano:")
        result = g.buscarCicloEuleriano()
        g.mostrarResultadoBuscaCicloEuleriano(result)
    except Exception as ex:
        print(ex)

def buscarComDijkstra():
    v = solicitarVertice()
    if v > 0:
        resultado = g.buscarCaminhoMinimoComDijkstra(v)
        for item in resultado:
            print(f'{item[1][-1]}:', ",".join(map(str, item[1])) + "; d=" + str(item[0]))

def buscarComFloydWarshall():
    matriz = g.buscarComFloydWarshall()
    g.exibirFloydWarshall(matriz)

# lista com funcoes que serao executadas
acoes = [
    {"texto": "Carregar um arquivo", "funcao": carregarArquivo},
    {"texto": "Mostrar o grafo", "funcao": mostrarGrafo},
    {"texto": "Ver a quantidade de Vértices", "funcao": mostrarQtdVertices},
    {"texto": "Ver a quantidade de Arestas", "funcao": mostrarQtdArestas},
    {"texto": "Grau do vértice", "funcao": verGrau},
    {"texto": "Rótulo do vértice", "funcao": verRotulo},
    {"texto": "Vizinhos do vértice", "funcao": verVizinhos},
    {"texto": "Verificar se há aresta", "funcao": verificarSeHaAresta},
    {"texto": "Realizar busca em largura", "funcao": buscarEmLargura},
    {"texto": "Procurar ciclo euleriano", "funcao": buscarCicloEuleriano},
    {"texto": "Realizar busca de caminhos mínimos com Dijkstra", "funcao": buscarComDijkstra},
    {"texto": "Floyd Warshall", "funcao": buscarComFloydWarshall}
]

user_input = -1
while user_input != 0:
    print()
    print("Menu: ")
    for i, acao in enumerate(acoes):
        print(str(i + 1) +" - " + acao["texto"])
    print("0 - Finalizar o programa")
    print()

    user_input = solicitarOpcao("Digite a opção desejada: ", 0, len(acoes))
    print()
    if user_input > 0:
        acoes[user_input - 1]["funcao"]()
        print()
        input('Pressione ENTER para continuar...')
    else:
        user_input = 0

# fim while
print()
print("Programa finalizado")
