import networkx as nx
import matplotlib.pyplot as plt
import numpy

G = nx.DiGraph()
G.add_edge("s", "a", capacity=16, flow=11)
G.add_edge("s", "b", capacity=13, flow=11)
G.add_edge("a", "c", capacity=12, flow=11)
G.add_edge("b", "a", capacity=4, flow=11)
G.add_edge("c", "b", capacity=9, flow=11)
G.add_edge("b", "d", capacity=14, flow=11)
G.add_edge("d", "c", capacity=7, flow=11)
G.add_edge("c", "t", capacity=20, flow=11)
G.add_edge("d", "t", capacity=4, flow=11)

pos = nx.random_layout(G)
node_colors=[ 'lightgrey' for _ in G.nodes() ]
# attention ici je connais les indices des sommets 's' et 't'
node_colors[0]='lightgreen' 
node_colors[G.order()-1]='lightblue' 

nx.draw_networkx(G, pos=pos, node_color=node_colors)

labels={ e : '{}|{}'.format(G[e[0]][e[1]]['flow'],G[e[0]][e[1]]['capacity']) for e in G.edges}
nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=labels)

plt.show()