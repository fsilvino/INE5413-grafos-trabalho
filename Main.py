from Graph import Graph

g = Graph()
g.ler("fln_pequena.net")

def mostrarQtdVertices():
    qtdVertex = g.qtdVertices()
    print()
    print("O grafo tem "+str(qtdVertex)+" vertices.")

def mostrarQtdArestas():
    qtdArestas = g.qtdArestas()
    print()
    print("O grafo tem "+str(qtdArestas)+" arestas.")

def buscaLargura():
    buscado = int(input("Digite o valor buscado:"))
    inicio = int(input("Digite o numero do vertice inicial:"))
    result = g.busca_largura(inicio, buscado)
    print("O resultado da busca em largura será mostrado abaixo:")
    g.show_result_busca_largura(result)

def mostrarGrafo():
    g.show_graph()

# lista com funcoes que serao execudatas
acoes = [
    mostrarGrafo,
    mostrarQtdVertices,
    mostrarQtdArestas,
    buscaLargura
]

user_input = -1
while user_input != 0:
    print("Qual operação você deseja realizar:")
    print("1 - Mostrar grafo")
    print("2 - Ver a quantidade de Vertices")
    print("3 - Ver a quantidade de Arestas")
    print("4 - Realizar busca em largura")
    print("0 - Finalizar o algoritmo")
    try:
        user_input = int(input("Digite a opção desejada:"))
        if user_input > 0 and user_input <= len(acoes):
            acoes[user_input - 1]()
            print()
        else:
            user_input = 0
    except:
        print()
        print("Você não digitou uma opção válida")
        print()
        continue


print()
print("Algoritmo finalizado")
