
import networkx as nx
import matplotlib.pyplot as plt
import numpy
import sys

"""
# Implementer une classe FlowNet
# Creer un reseau a partir de fichier .csv
# creer un reseau a partir d’un graphe oriente NetworkX dans lequel les capacites sont des attributs
# capacity des arcs,
# — obtenir le flot maximal (c’est un simple accesseur),
# — mettre a jour la capacit´e d’un arc (1 seul arc `a la fois pourra ˆetre modifi´e),
# — afficher le r´eseau,
# — enregistrer le r´eseau sous forme d’image,
# — calculer le flot maximal.
"""

"""
# DOING: ETAPE 3 dans sujet DM:
# TODO LIST:
#   -- Implementer Etape 3, Etape 4
"""
class FlowNet():

    def __init__(self, file_path):
        data = open(file_path, "r")
        Graphtype = nx.DiGraph()
        self.G = nx.parse_edgelist(data, delimiter=';', create_using=Graphtype,nodetype=str, data=(('capacity', int),))
        if not self.is_network_satisfied(self.G):
            sys.exit("Error: Network is not satisfied")
            
        self.init_format_show()
        self.source = list(self.G.nodes)[0]
        self.sink = list(self.G.nodes)[len(self.G.nodes)-1]
        self.current_max_flow = -1
        self.arc_updated = False
        self.is_calcule_maxflow_first_time = False
        self.INF = 10**10

    """ Notez que :
    # [Done] — la capacit´e d’un arc est un entier positif
    # [Done] — si il existe un arc entre un sommet u et un sommet v, il ne peut y avoir d’arc entre v et u
    # [Done - Using self.is_calcule_maxflow_first_time] — on ne pourra pas mettre `a jour la capacit´e d’un arc avant d’avoir calcul´e un premier flot maximal,
    # [To Do] — la mise `a jour de la capacit´e d’un arc implique le recalcul de flot maximal.
    """
    def is_network_satisfied(self, G):
        for e in G.edges:
            if G[e[0]][e[1]]['capacity'] < 0:
                return False
            if (e[1], e[0]) in G.edges:
                return False
        return True

    """
    List API of Class FlowNet:
    - compute_max_flow()
    - get_flow()
    - update(node1, node2, capacity(integer))
    - show()
    - export(target_file_path) 
    """
    def export(self, file_path):        

        labels={ e : '{}|{}'.format(self.G[e[0]][e[1]]['flow'],self.G[e[0]][e[1]]['capacity']) for e in self.G.edges}
        
        nx.draw_networkx(self.G, pos=self.pos, node_color=self.node_colors)
        nx.draw_networkx_edge_labels(self.G, pos=self.pos, edge_labels=labels)

        plt.show()
        plt.savefig(file_path)

    def show(self): 

        labels={ e : '{}|{}'.format(self.G[e[0]][e[1]]['flow'],self.G[e[0]][e[1]]['capacity']) for e in self.G.edges}
        
        nx.draw_networkx(self.G, pos=self.pos, node_color=self.node_colors)
        nx.draw_networkx_edge_labels(self.G, pos=self.pos, edge_labels=labels)

        plt.show()

    def compute_max_flow(self):
        for e in self.G.edges:
            self.G[e[0]][e[1]]['flow'] = 0
        self.current_max_flow = self.Edmonds_Karp(self.source, self.sink)
        self.is_calcule_maxflow_first_time = True

    def get_flow(self):
        if not self.is_calcule_maxflow_first_time:
            sys.exit("Error: Need to compute max flow before get max flow value")
        return self.current_max_flow

    def update(self, node1, node2, capacity):
        self.G[node1][node2]['capacity'] = capacity
        self.compute_max_flow()

    """
    End of API List!
    """

    def init_format_show(self):
        self.pos = nx.random_layout(self.G)
        self.node_colors=[ 'lightgrey' for _ in self.G.nodes() ]
        self.node_colors[0]='lightgreen' 
        self.node_colors[self.G.order()-1]='lightblue' 
        for e in self.G.edges:
            self.G[e[0]][e[1]]['flow'] = 0  

    def get_capacity_left(self, node1, node2):
        if self.G.nodes.get(node1) == None or self.G.nodes.get(node1) == None:
            return 0
        return self.G[node1][node2]['capacity'] - self.G[node1][node2]['flow']  

    def get_bottle_neck(self,path):
        if path == None:
            return 0
        min = self.INF
        i = 0
        while i < len(path)-1:
            tmp = self.get_capacity_left(path[i], path[i+1])
            if min > tmp:
                min = tmp
            i += 1
        return min

    def update_flow(self, path, bottle_neck):       
        i = 0
        while i < len(path)-1:
            self.G[path[i]][path[i+1]]['flow'] += bottle_neck
            i += 1

    def find_shortest_path(self, start, end, path=[]):
        path = path + [start]
        if start == end:
            return path
        if self.G.nodes.get(start) == None:
            return None
        shortest = None
        for node in self.G.successors(start):
            if not(node in path) and self.get_capacity_left(start, node) > 0:
                newpath = self.find_shortest_path(node, end, path)
                if newpath and (not shortest or len(newpath) < len(shortest)):
                    shortest = newpath
        return shortest

    def Edmonds_Karp(self, start, end):
        i = 0
        max_flow = 0
        while i < 10:
            path = self.find_shortest_path(start, end)
            if path == None:
                break
            bottle_neck = self.get_bottle_neck(path)
            self.update_flow(path, bottle_neck)
            max_flow += bottle_neck
            i += 1
            print(path)

        return max_flow

    