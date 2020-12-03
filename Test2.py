import networkx as nx
import matplotlib.pyplot as plt
import numpy

data = open('fig42.csv', "r")
Graphtype = nx.DiGraph()
G = nx.parse_edgelist(data, delimiter=';', create_using=Graphtype,nodetype=str, data=(('capacity', int),))

pos = nx.random_layout(G)
node_colors=[ 'lightgrey' for _ in G.nodes() ]
# attention ici je connais les indices des sommets 's' et 't'
node_colors[0]='lightgreen' 
node_colors[G.order()-1]='lightblue' 

nx.draw_networkx(G, pos=pos, node_color=node_colors)

for e in G.edges:
    G[e[0]][e[1]]['flow'] = 0

labels={ e : '{}|{}'.format(G[e[0]][e[1]]['flow'],G[e[0]][e[1]]['capacity']) for e in G.edges}
nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=labels)

plt.show()