from Graph import Graph

g = Graph()

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

def carregarArquivo():
    arquivoPadrao = "grafo.teste.net"
    arquivo = input("Digite o nome do arquivo (em branco carrega " + arquivoPadrao + "): ")
    try:
        if arquivo == "":
            arquivo = arquivoPadrao

        g.ler(arquivo)
        print("Arquivo " + arquivo + " carregado com sucesso.")
    except Exception as ex:
        print("Não foi possível ler o arquivo!")
        print(ex)


def mostrarQtdVertices():
    qtdVertex = g.qtdVertices()
    print("O grafo tem " + str(qtdVertex) + " vertices.")

def mostrarQtdArestas():
    qtdArestas = g.qtdArestas()
    print("O grafo tem " + str(qtdArestas) + " arestas.")

def buscaLargura():
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
        g.show_graph()
    except Exception as ex:
        print(ex)

def buscaCicloEuleriano():
    try:
        print("Resultado da busca por ciclo euleriano:")
        result = g.procuraCicloEuleriano()
        g.mostrarResultadoBuscaCicloEuleriano(result)
    except Exception as ex:
        print(ex)
    # print(result)

# lista com funcoes que serao executadas
acoes = [
    {"texto": "Carregar um arquivo", "funcao": carregarArquivo},
    {"texto": "Mostrar o grafo", "funcao": mostrarGrafo},
    {"texto": "Ver a quantidade de Vértices", "funcao": mostrarQtdVertices},
    {"texto": "Ver a quantidade de Arestas", "funcao": mostrarQtdArestas},
    {"texto": "Realizar busca em largura", "funcao": buscaLargura},
    {"texto": "Procurar ciclo euleriano", "funcao": buscaCicloEuleriano}
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
