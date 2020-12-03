
import networkx as nx
import matplotlib.pyplot as plt
import numpy
import sys

# Implementer une classe FlowNet
# Creer un reseau a partir de fichier .csv
# creer un reseau a partir d’un graphe oriente NetworkX dans lequel les capacites sont des attributs
# capacity des arcs,
# — obtenir le flot maximal (c’est un simple accesseur),
# — mettre a jour la capacit´e d’un arc (1 seul arc `a la fois pourra ˆetre modifi´e),
# — afficher le r´eseau,
# — enregistrer le r´eseau sous forme d’image,
# — calculer le flot maximal.

#
# DOING: ETAPE 1 dans sujet DM:
#   -- creer une version de la classe demandee sans qu’on puisse modifier les capacites (bonus : verifier que
#      le reseau satisfait les contraintes du sujet),
# TODO LIST:
#   -- Implementer Etape 2
#
class FlowNet():

    def __init__(self, file_path):
        data = open(file_path, "r")
        Graphtype = nx.DiGraph()
        self.G = nx.parse_edgelist(data, delimiter=';', create_using=Graphtype,nodetype=str, data=(('capacity', int),))
        if not self.is_network_satisfied(self.G):
            sys.exit("Error: Network is not satisfied")
            
        self.init_format_show()
        self.is_calcule_maxflow_first_time = False

    # Notez que :
    # [Done] — la capacit´e d’un arc est un entier positif
    # [Done] — si il existe un arc entre un sommet u et un sommet v, il ne peut y avoir d’arc entre v et u
    # [Using self.is_calcule_maxflow_first_time] — on ne pourra pas mettre `a jour la capacit´e d’un arc avant d’avoir calcul´e un premier flot maximal,
    # [To Do] — la mise `a jour de la capacit´e d’un arc implique le recalcul de flot maximal.
    def is_network_satisfied(self, G):
        for e in G.edges:
            if G[e[0]][e[1]]['capacity'] < 0:
                return False
            if (e[1], e[0]) in G.edges:
                return False
        return True

    def init_format_show(self):
        self.pos = nx.random_layout(self.G)
        self.node_colors=[ 'lightgrey' for _ in self.G.nodes() ]
        self.node_colors[0]='lightgreen' 
        self.node_colors[self.G.order()-1]='lightblue' 

    def export(self, file_path):

        for e in self.G.edges:
            self.G[e[0]][e[1]]['flow'] = 0

        labels={ e : '{}|{}'.format(self.G[e[0]][e[1]]['flow'],self.G[e[0]][e[1]]['capacity']) for e in self.G.edges}
        
        nx.draw_networkx(self.G, pos=self.pos, node_color=self.node_colors)
        nx.draw_networkx_edge_labels(self.G, pos=self.pos, edge_labels=labels)

        plt.show()
        plt.savefig(file_path)

    def show(self):
        for e in self.G.edges:
            self.G[e[0]][e[1]]['flow'] = 0

        labels={ e : '{}|{}'.format(self.G[e[0]][e[1]]['flow'],self.G[e[0]][e[1]]['capacity']) for e in self.G.edges}
        
        nx.draw_networkx(self.G, pos=self.pos, node_color=self.node_colors)
        nx.draw_networkx_edge_labels(self.G, pos=self.pos, edge_labels=labels)

        plt.show()