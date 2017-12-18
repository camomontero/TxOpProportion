'''
Created on Nov 30, 2017

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
        print 'VERTEX FLOW: %s' %self.adjacent[neighbor][self.get_id()] 
        #Just to verify the whole dictionary, with node as key and the
        #neighbors and weight as value 
        comple_dict={}
        comple_dict[self.get_id()]=self.adjacent
        print "Complete Dictionary: %s" %comple_dict
        
    def get_connections(self):
        #print "KEYS SON: %s" %self.adjacent.keys()
        return self.adjacent.keys()  
    
    def proportion_calculator(self):
        r = {}
        rr={}
        #rrr={}
        for w in self.get_connections():
            cost = self.get_flows(w)
            print "SELF GET ID: %s" %self.get_id()
            print "FLOWS A VER: %s" %cost
            
            r.update(cost)
            rr = r.values()
            prop = float(cost[self.get_id()]) / float(sum(rr)) 
            print 'prop: %s' %prop
         
        return prop   
        
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
        for v in self: # calling the method _iter_ internally
            sum_flows = v.proportion_calculator()
            txop_prop[v.get_id()] = sum_flows
        return txop_prop
 
if __name__ == '__main__':
    
    ######################################################
    #                     SCENARIO BALANCED 1            #             
    ######################################################
    
    bal1=Graph()
    bal1.add_vertex('A')
    bal1.add_vertex('B')
    bal1.add_edge('A', 'B', {'A': 1, 'B': 3})
    
    print "Scenario Balanced 1: A--B"
    print "TxOp proportion"
    print bal1.calc_txop_prop()
    print '\n'
    
    bal1G=nx.Graph()
    bal1G.add_node('A')
    bal1G.add_node('B')
    bal1G.add_edges_from([('A','B')])
    
    plt.title('SCENARIO BALANCED 1')
    nx.draw(bal1G, with_labels=True)
    plt.draw()
    plt.show()
        
    ######################################################
    #                     SCENARIO BALANCED 2            #             
    ######################################################
    
    bal2=Graph()
    bal2.add_vertex('A')
    bal2.add_vertex('B')
    bal2.add_vertex('C')
    bal2.add_edge('A', 'B', {'A': 2, 'B': 3})
    bal2.add_edge('B', 'C', {'B': 3, 'C': 1})
    bal2.add_edge('A', 'C', {'A': 2, 'C': 1})
    
    print "Scenario Balanced 2: -A--B--C-"
    print "TxOp proportion"
    print bal2.calc_txop_prop()
    print '\n'
    
    bal2G=nx.Graph()
    bal2G.add_node('A')
    bal2G.add_node('B')
    bal2G.add_node('C')
    bal2G.add_edges_from([('A','B'), ('B','C'), ('A','C')])
    
    plt.title('SCENARIO BALANCED 2')
    nx.draw(bal2G, with_labels=True)
    plt.draw()
    plt.show()
    
    ######################################################
    #                     SCENARIO BALANCED 3            #             
    ######################################################
    
    bal3=Graph()
    bal3.add_vertex('A')
    bal3.add_vertex('B')
    bal3.add_vertex('C')
    bal3.add_vertex('D')
    bal3.add_edge('A', 'B', {'A': 1, 'B': 2})
    bal3.add_edge('A', 'C', {'A': 1, 'C': 3})
    bal3.add_edge('A', 'D', {'A': 1, 'D': 4})
    bal3.add_edge('B', 'C', {'B': 2, 'C': 3})
    bal3.add_edge('B', 'D', {'B': 2, 'D': 4})
    bal3.add_edge('C', 'D', {'C': 3, 'D': 4})
    
    
    print "Scenario Balanced 3: A--B, A--C, A--D, B--C, B--D, C--D"
    print "TxOp proportion"
    print bal3.calc_txop_prop()
    print '\n'
    
    bal3G=nx.Graph()
    bal3G.add_node('A')
    bal3G.add_node('B')
    bal3G.add_node('C')
    bal3G.add_node('D')
    bal3G.add_edges_from([('A','B'), ('A','C'), ('A','D'),
                          ('B','C'), ('B','D'), ('C','D')])
    
    plt.title('SCENARIO BALANCED 3')
    nx.draw(bal3G, with_labels=True)
    plt.draw()
    plt.show()
    
    ######################################################
    #                     SCENARIO STARVATION 1          #             
    ######################################################
    
    starv1=Graph()
    starv1.add_vertex('A')
    starv1.add_vertex('B')
    starv1.add_vertex('C')
    starv1.add_edge('A', 'B', {'A': 1, 'B': 2})
    starv1.add_edge('B', 'C', {'B': 2, 'C': 3})
        
    print "Scenario Balanced 1: A--B--C"
    print "TxOp proportion"
    print starv1.calc_txop_prop()
    print '\n'
    
    starv1G=nx.Graph()
    starv1G.add_node('A')
    starv1G.add_node('B')
    starv1G.add_node('C')
    starv1G.add_edges_from([('A','B'), ('B','C')])
    
    plt.title('SCENARIO STARVATION 1')
    nx.draw(starv1G, with_labels=True)
    plt.draw()
    plt.show()

    ######################################################
    #                     SCENARIO STARVATION 2          #             
    ######################################################
    
    starv2=Graph()
    starv2.add_vertex('A')
    starv2.add_vertex('B')
    starv2.add_vertex('C')
    starv2.add_vertex('D')
    starv2.add_edge('A', 'B', {'A': 1, 'B': 4})
    starv2.add_edge('A', 'C', {'A': 1, 'C': 2})
    starv2.add_edge('B', 'C', {'B': 4, 'C': 2})
    starv2.add_edge('C', 'D', {'C': 2, 'D': 3})
        
    print "Scenario Starvation 2: A--B, A--C, B--C, C--D"
    print "TxOp proportion"
    print starv2.calc_txop_prop()
    print '\n'
    
    starv2G=nx.Graph()
    starv2G.add_node('A')
    starv2G.add_node('B')
    starv2G.add_node('C')
    starv2G.add_node('D')
    starv2G.add_edges_from([('A','B'), ('A','C'), ('B','C'), ('C','D')])
    
    plt.title('SCENARIO STARVATION 2')
    nx.draw(starv2G, with_labels=True)
    plt.draw()
    plt.show()
    
    ######################################################
    #                     SCENARIO STARVATION 3          #             
    ######################################################
    
    starv3=Graph()
    starv3.add_vertex('A')
    starv3.add_vertex('B')
    starv3.add_vertex('C')
    starv3.add_vertex('D')
    starv3.add_vertex('E')
    starv3.add_edge('A', 'B', {'A': 1, 'B': 3})
    starv3.add_edge('A', 'D', {'A': 1, 'D': 1})
    starv3.add_edge('A', 'E', {'A': 1, 'E': 4})
    starv3.add_edge('B', 'C', {'B': 3, 'C': 2})
    starv3.add_edge('B', 'D', {'B': 3, 'D': 1})
    starv3.add_edge('C', 'D', {'C': 2, 'D': 1})
    starv3.add_edge('D', 'E', {'D': 1, 'E': 4})
        
    print "Scenario Starvation 3: A--B, A--D, A--E, B--C, B--D, C--D, D--E"
    print "TxOp proportion"
    print starv3.calc_txop_prop()
    print '\n'
    
    starv3G=nx.Graph()
    starv3G.add_node('A')
    starv3G.add_node('B')
    starv3G.add_node('C')
    starv3G.add_node('D')
    starv3G.add_node('E')
    starv3G.add_edges_from([('A','B'), ('A','D'), ('A','E'), ('B','C'),
                            ('B','D'), ('C','D'), ('D','E')])
    
    plt.title('SCENARIO STARVATION 3')
    nx.draw(starv3G, with_labels=True)
    plt.draw()
    plt.show()
    
    ######################################################
    #                     SCENARIO BACKHAUL 1            #             
    ######################################################
    
    back1=Graph()
    back1.add_vertex('Adhoc')
    back1.add_vertex('Access')
    back1.add_edge('Adhoc', 'Access', {'Adhoc': 6, 'Access': 1})
    
    print "Scenario Backaul 1: Adhoc--Access"
    print "TxOp proportion"
    print back1.calc_txop_prop()
    print '\n'
    
    back1G=nx.Graph()
    back1G.add_node('Adhoc')
    back1G.add_node('Access')
    back1G.add_edges_from([('Adhoc','Access')])
    
    plt.title('SCENARIO BACKHAUL 1')
    nx.draw(back1G, with_labels=True)
    plt.draw()
    plt.show()
    
    ######################################################
    #                     SCENARIO BACKHAUL 2            #             
    ######################################################
    
    back2=Graph()
    back2.add_vertex('Adhoc')
    back2.add_vertex('Access')
    back2.add_edge('Adhoc', 'Access', {'Adhoc': 5, 'Access': 1})
    
    print "Scenario Backhaul 2: Adhoc--Access"
    print "TxOp proportion"
    print back2.calc_txop_prop()
    print '\n'
    
    back2G=nx.Graph()
    back2G.add_node('Adhoc')
    back2G.add_node('Access')
    back2G.add_edges_from([('Adhoc','Access')])
    
    plt.title('SCENARIO BACKHAUL 2')
    nx.draw(back2G, with_labels=True)
    plt.draw()
    plt.show()
    
    