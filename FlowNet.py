
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
#
# DOING: Testing and Improving performance
# 
"""
class FlowNet():

    def __init__(self, file_path):
        data = open(file_path, "r")
        Graphtype = nx.DiGraph()
        self.G = nx.parse_edgelist(data, delimiter=';', create_using=Graphtype,nodetype=str, data=(('capacity', int),))
        data.close()
        if not self.is_network_satisfied(self.G):
            sys.exit("Error: Network is not satisfied")
            
        self.init_format_show()
        self.source = list(self.G.nodes)[0]
        self.sink = list(self.G.nodes)[len(self.G.nodes)-1]
        self.current_max_flow = -1
        self.is_calcule_maxflow_first_time = False
        self.INF = 10**10

    """ Notez que :
    # [Done] — la capacit´e d’un arc est un entier positif
    # [Done] — si il existe un arc entre un sommet u et un sommet v, il ne peut y avoir d’arc entre v et u
    # [Done] — on ne pourra pas mettre `a jour la capacit´e d’un arc avant d’avoir calcul´e un premier flot maximal,
    # [Done] — la mise `a jour de la capacit´e d’un arc implique le recalcul de flot maximal.
    """
    def is_network_satisfied(self, G):
        for e in G.edges:
            if G[e[0]][e[1]]['capacity'] < 0 or (e[1], e[0]) in G.edges:
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

    def show(self):
        self.init_show_export()
        plt.show()
    
    def export(self, file_path):
        self.init_show_export()
        plt.savefig(file_path)

    def compute_max_flow(self):
        if (self.current_max_flow == -1):
            self.current_max_flow = self.Edmonds_Karp(self.source, self.sink)
        else:
            self.current_max_flow += self.Edmonds_Karp(self.source, self.sink)

    def get_flow(self):
        if self.current_max_flow == -1:
            sys.exit("Error: Need to compute max flow before get max flow value")
        return self.current_max_flow

    def update(self, node1, node2, capacity):
        if node1 == node2 or self.G.nodes.get(node1) == None or self.G.nodes.get(node2) == None or capacity < 0\
            or not ((node1, node2) in self.G.edges):
            sys.exit("Error: invalid nodes or capacity")

        if self.G[node1][node2]['capacity'] < capacity:
            self.update_step_3(node1, node2, capacity)
        elif self.G[node1][node2]['capacity'] > capacity:
            self.update_step_4(node1, node2, capacity)

    def set_source(self, source, sink):
        if self.G.nodes.get(source) == None or self.G.nodes.get(sink) == None:
            sys.exit("Error: Invalid Source/Sink")
        self.source = source
        self.sink = sink

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

    def init_show_export(self):
        labels={ e : '{}|{}'.format(self.G[e[0]][e[1]]['flow'],self.G[e[0]][e[1]]['capacity']) for e in self.G.edges}        
        nx.draw_networkx(self.G, pos=self.pos, node_color=self.node_colors)
        nx.draw_networkx_edge_labels(self.G, pos=self.pos, edge_labels=labels)

    def get_capacity_left(self, node1, node2):
        if self.G.nodes.get(node1) == None or self.G.nodes.get(node1) == None:
            return 0
        return self.G[node1][node2]['capacity'] - self.G[node1][node2]['flow']  

    def update_step_2(self, node1, node2, capacity):
        self.G[node1][node2]['capacity'] = capacity
        for e in self.G.edges:
            self.G[e[0]][e[1]]['flow'] = 0
        self.compute_max_flow()

    def update_step_3(self, node1, node2, capacity):
        self.G[node1][node2]['capacity'] = capacity
        self.compute_max_flow()

    def flow_reduced(self, start, end, rm):
        path = self.find_shortest_path2(start, end)
        if path == None:
            return None
        i = 0
        while i < len(path)-1:
            if self.G[path[i]][path[i+1]]['flow'] >= rm:
                self.G[path[i]][path[i+1]]['flow'] -= rm
            i += 1

    def update_step_4(self, node1, node2, capacity):
        if capacity >= self.G[node1][node2]['flow']:
            self.G[node1][node2]['capacity'] = capacity
            return None

        rm = self.G[node1][node2]['flow'] - capacity
        self.current_max_flow -= rm
        self.G[node1][node2]['capacity'], self.G[node1][node2]['flow'] = capacity, capacity

        self.flow_reduced(self.source, node1, rm)
        self.flow_reduced(node2, self.sink, rm)
        
        path = self.find_shortest_path(self.source, self.sink)
        if path != None:        
            bottle_neck = self.get_bottle_neck(path)
            self.update_flow(path, bottle_neck)
            self.current_max_flow += bottle_neck
            # print(path)

    def get_bottle_neck(self,path):
        if path == None:
            return 0
        minf = self.INF
        i = 0
        while i < len(path)-1:
            tmp = self.get_capacity_left(path[i], path[i+1])
            if minf > tmp:
                minf = tmp
            i += 1
        return minf

    def update_flow(self, path, bottle_neck):       
        i = 0
        while i < len(path)-1:
            self.G[path[i]][path[i+1]]['flow'] += bottle_neck
            i += 1

    def find_shortest_path2(self, start, end, path=[]):
        path = path + [start]
        if start == end:
            return path
        if self.G.nodes.get(start) == None:
            return None
        shortest = None
        for node in self.G.successors(start):
            if not(node in path):
                newpath = self.find_shortest_path2(node, end, path)
                if newpath and (not shortest or len(newpath) < len(shortest)):
                    shortest = newpath
        return shortest

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
        while True:
            path = self.find_shortest_path(start, end)
            if path == None:
                break
            bottle_neck = self.get_bottle_neck(path)
            self.update_flow(path, bottle_neck)
            max_flow += bottle_neck
            i += 1
            # print(path)
        return max_flow
    