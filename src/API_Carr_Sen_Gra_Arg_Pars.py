'''
Created on Nov 30, 2017

@author: camilo
'''

import networkx as nx
import matplotlib.pyplot as plt
import argparse
import json
import sys

#def arg_type(argument):
#    if argument[1]=='{':
        

#parser = argparse.ArgumentParser(description='Calculate the appropriate TxOp' 
#                                            'of nodes in Carrier Sense Range')
#parser.add_argument("nodefrom", type=str, help="node source")
#parser.add_argument("nodeto", type=str, help="node destiny")
#parser.add_argument('weight', type=str, help='Flows traversing the link from-to')
#args = parser.parse_args()
#print args

parser = argparse.ArgumentParser(description='Calculate the appropriate TxOp' 
                                            'of nodes in Carrier Sense Range')
parser.add_argument("--node", type=str, help="node", nargs="+")
parser.add_argument('--weight', type=json.loads, help='Flows traversing the link from-to', nargs="+")
args = parser.parse_args()
print args


class Vertex:
    """
        This class represents the Node itself and its characteristics.
        Neighbors of the Node can be added, flows of each node can be
        gotten, TxOp proportion can be calculated.
        
    """

    def __init__(self, node):
        '''
        Constructor
        '''
        self.id = node
        self.adjacent = {}
        
    def add_neighbor(self, neighbor, weight={}):
        self.adjacent[neighbor] = weight
        comple_dict={}
        comple_dict[self.get_id()]=self.adjacent
                
    def get_connections(self):
        return self.adjacent.keys()  
    
    def proportion_calculator(self):
        cost_dict = {}
        flow_list = []
        for w in self.get_connections():
            print "W: %s" %w
            cost = self.get_flows(w)
            print "COST: %s" %cost
            cost_dict.update(cost)
            flow_list = cost_dict.values()
            print "FLOW_LIST: %s" %flow_list
            print "SUM FLOW_LIST: %s" %sum(flow_list)
            print "COST VERTEX: %s" %cost[self.get_id()]
            prop = float(cost[self.get_id()]) / float(sum(flow_list)) 
        return round(prop, 5)   
        
    def get_id(self):
        return self.id
    
    def get_flows(self, neighbor):
        return self.adjacent[neighbor]
        
class Graph:
    """
    This class represents the whole Graph. Nodes(Vertices) of the Graph
    can be added, the edges(links) also. From here can be called the
    methods of the class Vertex. 
    """
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

    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None
        
    def add_edge(self, frm, to, cost = {}):
        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)
        self.vert_dict[frm].add_neighbor(to, cost)
        self.vert_dict[to].add_neighbor(frm, cost)
    
    def calc_txop_prop(self):
        txop_prop = {}
        for v in self:
            print "V: %s" %v.get_id()
            sum_flows = v.proportion_calculator()
            txop_prop[v.get_id()] = sum_flows
        return txop_prop
 
if __name__ == '__main__':
    
    ######################################################
    #                SCENARIO TEST ARGUMENTS             #             
    ######################################################
    
    #bal1=Graph()
    #bal1.add_vertex(args.nodefrom)
    #bal1.add_vertex(args.nodeto)
    
    #my_dictionary = json.loads(args.weight)
    #print "Type of Dictionary: %s" %type(my_dictionary)
    #bal1.add_edge(args.nodefrom, args.nodeto, my_dictionary)
    
    #print "Scenario Balanced 1: A--B"
    #print "TxOp proportion:"
    #print bal1.calc_txop_prop()
    #print '\n'
    
    #bal1G=nx.Graph()
    #bal1G.add_node(args.nodefrom)
    #bal1G.add_node(args.nodeto)
    #bal1G.add_edges_from([(args.nodefrom,args.nodeto)])
    
    #plt.title('SCENARIO BALANCED 1')
    #nx.draw(bal1G, with_labels=True)
    #plt.draw()
    #plt.show()
    

    ######################################################
    #                SCENARIO TEST ARGUMENTS 2           #             
    ######################################################
    
    print "NAME OF THE SCRIPT: ", sys.argv[0]
    print "Number of arguments: ", len(sys.argv)
    print "The arguments are: " , str(sys.argv)
    print "The arguments without the name of the file are: " , str(sys.argv[1:]) 
    
    print "A VER QUE: %s" %args.node[0:]
    print "A VER NO MAS: %s" %args.weight[0:]
    
    bal1=Graph()
    for i in args.node:
        bal1.add_vertex(i)
    #bal1.add_vertex(args.node[3])
    
    #my_dictionary = args.weight[0:]
    #print "Type of Dictionary: %s" %type(my_dictionary)
    #bal1.add_edge(args.node[2], args.node[3], my_dictionary)
    
    
    my_dictionary = args.weight[0:]
    print "Lista de Dictionary: %s" %my_dictionary
    for j in range(len(my_dictionary)):
        bal1.add_edge(my_dictionary[j].keys()[0], my_dictionary[j].keys()[1], my_dictionary)
        print my_dictionary[j].keys()[0]
        print my_dictionary[j].keys()[1]
        print my_dictionary[j]
    
    print "Scenario Balanced 1: A--B"
    print "TxOp proportion:"
    print bal1.calc_txop_prop()
    print '\n'
    
    #bal1G=nx.Graph()
    #bal1G.add_node(args.nodefrom)
    #bal1G.add_node(args.nodeto)
    #bal1G.add_edges_from([(args.nodefrom,args.nodeto)])
    
    #plt.title('SCENARIO BALANCED 1')
    #nx.draw(bal1G, with_labels=True)
    #plt.draw()
    #plt.show()

    