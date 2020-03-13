from Graph import Graph

g = Graph()
g.ler("fln_pequena.net")
# g.show_graph()
# g.busca_largura(8, 1)
#     print(v.relationships)
# print(g.vertices)
user_input = -1
while user_input != 0:
    print("Qual operação você deseja realizar:")
    print("1 - Ver a quantidade de Vertices")
    print("2 - Ver a quantidade de Arestas")
    print("0 - Finalizar o algoritmo")
    try:
        user_input = int(input("Digite a opção desejada:"))
    except:
        print()
        print("Você não digitou uma opção válida")
        print()
        continue

    if user_input == 1:
        qtdVertex = g.qtdVertices()
        print()
        print("O grafo tem "+str(qtdVertex)+" vertices.")
        print()
    if user_input == 2:
        qtdArestas = g.qtdArestas()
        print()
        print("O grafo tem "+str(qtdArestas)+" arestas.")
        print()
    if user_input >= 3:
        user_input = 0

print()
print("Algoritmo finalizado")
