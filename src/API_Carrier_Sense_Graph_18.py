'''
Created on Nov 30, 2017

@author: Camilo Montero

Given a Graph and the outgoing flows of nodes in Carrier Sense
Range, this script allows to find an appropriate airtime utilization
proportion per node, so that Flow Fairness is achieved. 
'''

import networkx as nx
import matplotlib.pyplot as plt

class Vertex:
    
    """Represents the Node itself and its characteristics.
    
    This class is used by the class Graph in order to carry out 
    the calculations. Methods of this class should be invoked only
    through the methods of the class Graph. This class and its methods 
    should not be invoked directly by the user. 
    """

    def __init__(self, node, channel=0):
        self.id = node
        self.adjacent = {}
        self.channel = channel
        
    def add_neighbor(self, neighbor, weight={}):
        self.adjacent[neighbor] = weight
        comple_dict={}
        comple_dict[self.get_id()]=self.adjacent
                
    def get_connections(self):
        return self.adjacent.keys()  
    
    def proportion_calculator(self):
        cost_dict = {}
        flow_list = []
        if (len(self.get_connections())>=1):
            for w in self.get_connections():
                cost = self.get_flows(w)
                cost_dict.update(cost)
                flow_list = cost_dict.values()
                prop = float(cost[self.get_id()]) / float(sum(flow_list)) 
            return round(prop, 5)
        else: 
            return 1   
        
    def get_id(self):
        return self.id
    
    def get_flows(self, neighbor):
        return self.adjacent[neighbor]
        
class Graph:
    
    """Represents the Carrier Sense Graph.
    
    It contains methods that allows you to add Nodes(Vertices) 
    of the Graph, the edges(links) between them and calculate
    the txop proportion. This class internally call the methods
    of the class Vertex, in order to perform the calculations.
     
    """
    def __init__(self):
        """Constructor.
        
        Initialization variables
        ------------------------
        vert_dict: dictionary
        num_vertices: integer
        """
        
        self.vert_dict = {}
        self.num_vertices = 0
    
    def __iter__(self):
        """ Returns an iterator.
        
        Description
        -----------
        It iterates through each value of the dict vert_dict.
        Each value is a class Vertex instance.
        It is called with a for loop: 
        
        Example
        ------- 
        for i in self:
        """
        
        return iter(self.vert_dict.values())
        
    def add_vertex(self, node, channel=0):
        """Creates a vertex in the Graph.
        
        Parameters
        ----------
        node: string 
            vertex to add to the Graph
        channel: integer
            channel used by the node
        
        Description
        -----------
        It builds the dict "vert_dict"
        Example: {'node': class_Vertex_instance}
        
        Returns
        --------
        A class Vertex instance
            This is the value of the pair element in the dict "vert_dict"
        """
        
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(node, channel)
        self.vert_dict[node] = new_vertex
        return new_vertex

    def get_vertex(self, n):
        """ Recover the vertex if it was already created.
        Otherwise it returns None.
        
        Parameters
        ----------
        n: string 
            vertex of the Carrier Sense Graph.
        
        Returns
        --------
        A class Vertex instance
            This is the value of the pair element in the dict "vert_dict"
        """
        
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None
        
    def add_edge(self, frm, to, cost = {}):
        """ Creates an edge in the Graph.
        
        This edge represents the link between the two nodes
        in carrier sense range.
        
        Parameters
        ----------
        frm: string 
            first vertex of the edge    
        to: string 
            second vertex of the edge
        cost: dictionary
            no. of flows of first and second vertex.
        
        Example:
        --------
        'A', 'B', {'A': 1, 'B': 3}
        """
        
        if frm not in self.vert_dict:
            raise ValueError('Node not found. Please add it using add_vertex method')
        if to not in self.vert_dict:
            raise ValueError('Node not found. Please add it using add_vertex method')
        
        src_node = self.vert_dict[frm]
        dst_node = self.vert_dict[to]
        
        if src_node.channel != dst_node.channel:
            raise ValueError('Edge should be from nodes using the same channel')
        
        src_node.add_neighbor(to, cost)
        dst_node.add_neighbor(frm, cost)
    
    def calc_txop_prop(self):
        """ Return the airtime utilization proportion per node. 
        
        Return
        ------
        txop_prop: dictionary 
            Contains each node as the key and the txop_proportion
            as the value.
        
        Example:
        --------
        {'A': 0.25, 'B': 0.75}
        """
        
        txop_prop = {}
        for v in self:
            sum_flows = v.proportion_calculator()
            txop_prop[v.get_id()] = sum_flows
        return txop_prop
 
    def calc_txop_value(self, max_txop, dict_p):
        """ Return the airtime utilization value per node. 
        
        Parameters
        ----------
        max_txop: integer 
            represents the maximum allowed TxOp value in us (8160us)    
        dict_p: dictionary 
            airtime utilization proportion per node.
        
        Return
        ------
        txop_values: dictionary 
            Contains each node as the key and the txop_value
            as the value.
        
        Example:
        --------
        {'A': 2016.0, 'B': 6112.0}
        """
        
        txop_values = {}
        for key, value in dict_p.items():
            temp = max_txop*value
            txop_val = temp - (temp % 32)
            txop_values[key] = txop_val
        return txop_values
        
        
if __name__ == '__main__':
    """Different scenarios are set here as an example
       of how to use correctly the methods that the API
       provides.
    """   
    max_txop=8160
    ######################################################
    #                 SCENARIO BALANCED 1                #             
    ######################################################
    
    bal1=Graph()
    bal1.add_vertex('A', 38)
    bal1.add_vertex('B', 38)
    bal1.add_vertex('C', 40)
    bal1.add_vertex('D', 38)
    bal1.add_edge('A', 'B', {'A': 1, 'B': 3})
    bal1.add_edge('B', 'D', {'B': 3, 'D': 5})
    
    print "Scenario Balanced 1: A--B"
    print "TxOp proportion:"
    p1 = bal1.calc_txop_prop()
    print p1
    print "TxOp values:"
    print bal1.calc_txop_value(max_txop, p1)
    print '\n'
    
    bal1G=nx.Graph()
    bal1G.add_node('A')
    bal1G.add_node('B')
    bal1G.add_node('C')
    bal1G.add_node('D')
    bal1G.add_edges_from([('A','B')])
    
    plt.title('SCENARIO BALANCED 1')
    nx.draw_networkx(bal1G, with_labels=True)
    plt.draw()
    plt.show()
        
    ######################################################
    #                 SCENARIO BALANCED 2                #             
    ######################################################
    
    bal2=Graph()
    bal2.add_vertex('A')
    bal2.add_vertex('B')
    bal2.add_vertex('C')
    bal2.add_edge('A', 'B', {'A': 2, 'B': 3})
    bal2.add_edge('B', 'C', {'B': 3, 'C': 1})
    bal2.add_edge('A', 'C', {'A': 2, 'C': 1})
    
    print "Scenario Balanced 2: A--B, B--C, A--C"
    print "TxOp proportion:"
    p2 = bal2.calc_txop_prop()
    print p2
    print "TxOp values:"
    print bal2.calc_txop_value(max_txop, p2)
    print '\n'
    
    bal2G=nx.Graph()
    bal2G.add_node('A')
    bal2G.add_node('B')
    bal2G.add_node('C')
    bal2G.add_edges_from([('A','B'), ('B','C'), ('A','C')])
    
    plt.title('SCENARIO BALANCED 2')
    nx.draw_networkx(bal2G, with_labels=True)
    plt.draw()
    plt.show()
    
    ######################################################
    #                 SCENARIO BALANCED 3                #             
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
    print "TxOp proportion:"
    p3 = bal3.calc_txop_prop()
    print p3
    print "TxOp values:"
    print bal3.calc_txop_value(max_txop, p3)
    print '\n'
    
    bal3G=nx.Graph()
    bal3G.add_node('A')
    bal3G.add_node('B')
    bal3G.add_node('C')
    bal3G.add_node('D')
    bal3G.add_edges_from([('A','B'), ('A','C'), ('A','D'),
                          ('B','C'), ('B','D'), ('C','D')])
    
    plt.title('SCENARIO BALANCED 3')
    nx.draw_networkx(bal3G, with_labels=True)
    plt.draw()
    plt.show()
    
    ######################################################
    #                 SCENARIO STARVATION 1              #             
    ######################################################
    
    starv1=Graph()
    starv1.add_vertex('A')
    starv1.add_vertex('B')
    starv1.add_vertex('C')
    starv1.add_edge('A', 'B', {'A': 1, 'B': 2})
    starv1.add_edge('B', 'C', {'B': 2, 'C': 3})
        
    print "Scenario Starvation 1: A--B--C"
    print "TxOp proportion:"
    p4 = starv1.calc_txop_prop()
    print p4
    print "TxOp values:"
    print starv1.calc_txop_value(max_txop, p4)
    print '\n'
    
    starv1G=nx.Graph()
    starv1G.add_node('A')
    starv1G.add_node('B')
    starv1G.add_node('C')
    starv1G.add_edges_from([('A','B'), ('B','C')])
    
    plt.title('SCENARIO STARVATION 1')
    nx.draw_networkx(starv1G, with_labels=True)
    plt.draw()
    plt.show()

    ######################################################
    #                 SCENARIO STARVATION 2              #             
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
    print "TxOp proportion:"
    p5 = starv2.calc_txop_prop()
    print p5
    print "TxOp values:"
    print starv2.calc_txop_value(max_txop, p5)
    print '\n'
    
    starv2G=nx.Graph()
    starv2G.add_node('A')
    starv2G.add_node('B')
    starv2G.add_node('C')
    starv2G.add_node('D')
    starv2G.add_edges_from([('A','B'), ('A','C'), ('B','C'), ('C','D')])
    
    plt.title('SCENARIO STARVATION 2')
    nx.draw_networkx(starv2G, with_labels=True)
    plt.draw()
    plt.show()
    
    ######################################################
    #                 SCENARIO STARVATION 3              #             
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
    print "TxOp proportion:"
    p6 = starv3.calc_txop_prop()
    print p6
    print "TxOp values:"
    print starv3.calc_txop_value(max_txop, p6)
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
    nx.draw_networkx(starv3G, with_labels=True)
    plt.draw()
    plt.show()
    
    ######################################################
    #                 SCENARIO BACKHAUL 1                #             
    ######################################################
    
    back1=Graph()
    back1.add_vertex('Adhoc')
    back1.add_vertex('Access')
    back1.add_edge('Adhoc', 'Access', {'Adhoc': 6, 'Access': 1})
    
    print "Scenario Backaul 1: Adhoc--Access"
    print "TxOp proportion:"
    p7 = back1.calc_txop_prop()
    print p7
    print "TxOp values:"
    print back1.calc_txop_value(max_txop, p7)
    print '\n'
    
    back1G=nx.Graph()
    back1G.add_node('Adhoc')
    back1G.add_node('Access')
    back1G.add_edges_from([('Adhoc','Access')])
    
    plt.title('SCENARIO BACKHAUL 1')
    nx.draw_networkx(back1G, with_labels=True)
    plt.draw()
    plt.show()
    
    ######################################################
    #                 SCENARIO BACKHAUL 2                #             
    ######################################################
    
    back2=Graph()
    back2.add_vertex('Access1', 44)
    back2.add_vertex('Access2', 36)
    back2.add_vertex('Adhoc1', 36)
    back2.add_vertex('Adhoc2', 52)
    back2.add_vertex('Adhoc3', 56)
    back2.add_edge('Adhoc1', 'Access2', {'Adhoc1': 5, 'Access2': 1})
    
    print "Scenario Backhaul 2: Adhoc--Access"
    print "TxOp proportion:"
    p8 = back2.calc_txop_prop()
    print p8
    print "TxOp values:"
    print back2.calc_txop_value(max_txop, p8)
    print '\n'
    
    back2G=nx.Graph()
    back2G.add_node('Adhoc1')
    back2G.add_node('Access1')
    back2G.add_node('Adhoc2')
    back2G.add_node('Access2')
    back2G.add_node('Adhoc3')
    back2G.add_edges_from([('Adhoc1','Access2')])
    
    plt.title('SCENARIO BACKHAUL 2')
    nx.draw_networkx(back2G, with_labels=True)
    plt.draw()
    plt.show()
    
    