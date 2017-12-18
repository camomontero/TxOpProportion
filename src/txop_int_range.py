'''
Created on Jul 27, 2017

@author: camilo
'''

class Vertex:
    '''
        This class represents the a Node itself and its caracteristics.
    '''

    def __init__(self, node):
        
        self.id = node
        self.adjacent = {}
        
    def __str__(self):
        return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])
    
    def add_neighbor(self, neighbor, weigth={}):
        self.adjacent[neighbor] = weigth
        
    def get_connections(self):
        return self.adjacent.keys()  

    def get_id(self):
        return self.id

    def get_weight(self, neighbor):
        return self.adjacent[neighbor]
    
    def get_channel(self, neighbor):
        return self.adjacent[neighbor]["channel"]
    
    def get_flows(self, neighbor):
        return self.adjacent[neighbor]["flows"]

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
    
    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None
        
    def add_edge(self, frm, to, cost={}):
        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)
        
        self.vert_dict[frm].add_neighbor(self.vert_dict[to], cost)
        self.vert_dict[to].add_neighbor(self.vert_dict[frm], cost)

    def get_vertices(self):
        return self.vert_dict.keys()
    
    def list_channels(self):
        visited_channel={}
        for v in self:
            for w in v.get_connections():
                channel = v.get_channel(w)
                node_obj = {"id": w.get_id(), "flows": v.get_flows(w)}
                if channel not in visited_channel:
                    visited_channel[channel] = [node_obj]
                else:
                    visited_channel[channel].append(node_obj)

        print "List of channels: %s"  %visited_channel
        return visited_channel
        
    def compare_channels(self):
        to_compare = self.list_channels()
        conflict_channels = []
        
        for channel in to_compare.keys():
            if len(to_compare[channel]) > 2:
                conflict_channels.append(channel)
        print "List of channels in Conflict: %s"  %conflict_channels  
        return conflict_channels     
    
    def flow_path(self):
        for v in self:
            for w in v.get_connections():
                print "QUE ES W: %s" %w

if __name__=='__main__':
    
    g = Graph()
    
    g.add_vertex('A_d')
    g.add_vertex('A_u')
    
    g.add_vertex('ASta')
    
    g.add_vertex('B_d')
    g.add_vertex('B_u')
    
    g.add_vertex('BSta')
    
    g.add_vertex('C_d')
    g.add_vertex('C_u')
    
    g.add_vertex('CSta')
    
    g.add_edge('ASta', 'A_d', {'channel': 36, 'flows': 1, 'int_range': ['B_d']})
    g.add_edge('BSta', 'B_d', {'channel': 36, 'flows': 1, 'int_range': ['A_d', 'C_d']})
    g.add_edge('CSta', 'C_d', {'channel': 36, 'flows': 1, 'int_range': ['B_d']})
    
    g.compare_channels()
    g.flow_path()
    
    for v in g:
        for w in v.get_connections():
            #print "AQUIIII CARAJO"
            #print w
            vid = v.get_id()
            wid = w.get_id()
            print 'Channel: ( %s , %s, %3d)'  % ( vid, wid, v.get_channel(w))
            print 'Flows: ( %s , %s, %3d)'  % ( vid, wid, v.get_flows(w))

    for v in g:
        print 'g.vert_dict[%s]=%s' %(v.get_id(), g.vert_dict[v.get_id()])
    