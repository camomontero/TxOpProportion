'''
Created on Aug 2, 2017

@author: camilo
'''

import networkx as nx
import matplotlib.pyplot as plt

class Vertex:
    '''
        This class represents the Node itself and his caracteristics.
    '''

    def __init__(self, node):
        '''
        Constructor
        '''
        self.id = node
        self.adjacent = {}
        self.flows = {}

    def add_neighbor(self, neighbor, weight={}):
        self.adjacent[neighbor] = weight
        print 'ADJACENT DICTIONARY: %s' %self.adjacent 
        #Just to verify the whole dictionary, with node as key and the
        #neighbors and weight as value 
        comple_dict={}
        comple_dict[self.get_id()]=self.adjacent
        print "Complete Dictionary: %s" %comple_dict
        
    def get_connections(self):
        #print "KEYS SON: %s" %self.adjacent.keys()
        return self.adjacent.keys()  
    
    def proportion_calculator(self):
        ranges = []
        for w in self.get_connections():
            flows = self.get_flows(w)
            print "FLOWS A VER: %s" %flows
            #print "SELF GET ID: %s" %self.get_id()
            #print "TYPE OF SELF GET ID: %s" %type(self.get_id())
            #suma = float(flows['D']) / float(sum(flows.values()))
            #total_add = flows[self.get_id()]
            suma = float(flows[self.get_id()]) / float(sum(flows.values()))
            ranges.append(suma)
        return min(ranges)
        
    def get_id(self):
        return self.id
    
    def get_flows(self, neighbor):
        #print "TYPE OF W OF GET_FLOWS: %s" %neighbor
        return self.adjacent[neighbor]
        
class Graph:
    '''
    This class represents the whole Graph.
    '''
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0
    
    def __iter__(self):
        return iter(self.vert_dict.values())

    def add_vertex(self, node):
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(node)
        self.vert_dict[node] = new_vertex
        return new_vertex

    def get_vertex(self, n): # call the __str__ method of class Vertex
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None
        
    def add_edge(self, frm, to, cost = {}):
        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)
        
        #COMMENTING THE NEXT TW LINE: SO I DID WITH LUCHO
        #self.vert_dict[frm].add_neighbor(self.vert_dict[to], cost)
        #self.vert_dict[to].add_neighbor(self.vert_dict[frm], cost)
        
        #I realize no need to pass the value, but the key as the neighbor parameter
        self.vert_dict[frm].add_neighbor(to, cost)
        self.vert_dict[to].add_neighbor(frm, cost)
    
    def calc_txop_prop(self):
        txop_prop = {}
        for v in self:
            sum_flows = v.proportion_calculator()
            if v.get_id() in txop_prop.keys():
                if sum_flows < txop_prop[v.get_id()]:
                    txop_prop[v.get_id()] = sum_flows
            else:
                txop_prop[v.get_id()] = sum_flows
        return txop_prop
 
if __name__ == '__main__':
    
    ######################################################
    #                     SCENARIO 1                     #             
    ######################################################
    
    dictMap = {}
    dictMap[40]=Graph()
    dictMap[40].add_vertex('A',3)
    
    g = Graph()
    g.add_vertex('A')
    g.add_vertex('B')
    g.add_vertex('C')
    
    g.add_edge('A', 'B', {'A': 3, 'B': 1})
    g.add_edge('B', 'C', {'B': 1, 'C': 5})
    
    print "Scenario 1: A--B--C"
    print "TxOp proportion"
    print g.calc_txop_prop()
    print '\n'
    
    G=nx.Graph()
    G.add_node('A')
    G.add_node('B')
    G.add_node('C')
    G.add_edges_from([('A','B'), ('B', 'C')])
    nx.draw(G, with_labels=True)
    plt.draw()
    plt.show()
    
    ######################################################
    #                     SCENARIO 2                     #             
    ######################################################
    
    gr = Graph()
    
    gr.add_vertex('A')
    gr.add_vertex('B')
    gr.add_vertex('C')
    gr.add_vertex('D')
    
    gr.add_edge('A', 'B', {'A': 1, 'B': 4})
    gr.add_edge('B', 'C', {'B': 4, 'C': 2})
    gr.add_edge('A', 'C', {'A': 1, 'C': 2})
    gr.add_edge('C', 'D', {'C': 2, 'D': 3})
    
    print "Scenario 2: A--B--C--D"
    print "            A-----C"
    print "TxOp proportion"
    print gr.calc_txop_prop()
    print '\n'
    
    Gr=nx.Graph()
    Gr.add_node('A')
    Gr.add_node('B')
    Gr.add_node('C')
    Gr.add_node('D')
    Gr.add_edges_from([('A','B'), ('B', 'C'), ('C', 'A'), ('C', 'D')])
    nx.draw(Gr, with_labels=True)
    plt.draw()
    plt.show()
    
    ######################################################
    #                     SCENARIO 3                     #             
    ######################################################
    
    gra = Graph()
    
    gra.add_vertex('A')
    gra.add_vertex('B')
        
    gra.add_edge('A', 'B', {'A': 9, 'B': 1})
    print "Scenario 3: A--B"
    print "TxOp proportion"
    print gra.calc_txop_prop()
    print '\n'
    
    Gra=nx.Graph()
    Gra.add_node('A')
    Gra.add_node('B')
    Gra.add_edges_from([('A','B')])
    nx.draw(Gra, with_labels=True)
    plt.draw()
    plt.show()
    
    