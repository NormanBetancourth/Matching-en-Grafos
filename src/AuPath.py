from networkx.algorithms.bipartite import sets as bipartite_sets
import networkx as nx
from networkx.algorithms.bipartite.basic import is_bipartite

#G = nx.read_graphml('Sample1.graphml')
#G = nx.read_graphml('Sample2.graphml')
G = nx.Graph([(1,6),(1,7),(1,8),(2,6),(2,9),(2,10),(3,6),(3,7),(4,8),(4,9),(4,10),(5,6)])
M = {x: None for x in G.nodes}  #Diccionario para acceder a los matches de un nodo determinado
X, Y = bipartite_sets(G)#guardamos los sets del Grafo
mark = {x: False for x in G.nodes()}# usaremos para verificar si un nodo fue usado en el algoritmo de creacion del augmentingPath
R = [x for x in X if mark[x] == False]
T = [] 
predecessor = {x:None for x in G.nodes()}#usado para construir nuestro augmentingPath relativo a un match


def getAugmentingPath(y):  # este metodo pasa por el predecessor, el cual guarda los predecesores de x numero
    result = []
    def pathing(result, y):
        result.insert(0,y)
        if predecessor[y] == None:
            return result
        else:
            return pathing(result, predecessor[y])
    return pathing(result,y)

def Addmatch(x,y):#anade de manere reciproca valores para 2 matches
    M[x]=y
    M[y]=x


def Matcher(M,R,G,T,mark):
    while len(R) > 0:#mientras hayan elementos en el primer set que no esten matcheados o elementos que se desean mover
        x= R.pop(0)
        mark[x]=True
        for y in list(G[x]):#repetimos esto para todos las aristas de un nodo especifico
            if y not in T:
                #T guarda los elementos del segundo set Y, que usamos en nuestra iteracion, 
                #T se vuelve a construir cada vez que llamamos la funcion
                predecessor[y]=x #Esto guarda el predecesor del un nodo si este no se ha usado, vital para crear el AugmentingPath path
                T.append(y)
                if M[y] is None:# si y no esta en el match => crea el augmentingPath de y
                    return getAugmentingPath(y)
                if M[y] is not None:
                    aux = M[y] #Si y esta en el match => guardamos el match de y, para meterlo en R y vinculamos como predecesor de este el nodo y
                    R.append(aux)
                    predecessor[aux]=y
    return []  # en caso que no se haya podido construir un AugmentingPath regresamos una lista vacia

x = []
x = Matcher(M, R, G, [], mark)  # asignamos el AugmentingPath a x
while len(x) > 0:  # mientras el exista AugmentingPath
    R = [x for x in X if mark[x] == False]  # cada que se llama la funcion
    if len(x) < 3:
        # agregamos el augmentingPath a resultante a nuestro match
        Addmatch(x[0], x[1])
    aux = x
    x = Matcher(M, R, G, [], mark)
print(aux)
print(M)
z = {}
for i in range(0, len(aux)-1):  # pasamos nuestro AugmentingPath de lista a diccionario
    z[aux[i]] = aux[i+1]
counter = 0
for key in z.keys():  # aplicamos el concepto de AugmentingPath, agregando los elementos en nivel par y quitando los de nivel impar de nuestro matching
    counter += 1
    if counter == 0 or counter % 2 != 0:
        Addmatch(key, z[key])


k = [(x, M[x]) for x in X if M[x] is not None]
print(k)

