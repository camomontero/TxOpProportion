'''
Created on Jul 23, 2017

@author: camilo
'''
print("Hello World")
class Vertex:
    '''
    This class represents the Node itself and his caracteristics.
    '''

    def __init__(self, node):
        
        self.id = node
        self.adjacent = {}
        
    def __str__(self):
        return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])

    def add_neighbor(self, neighbor, weight={}):
        self.adjacent[neighbor] = weight

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
    
    def get_int_range(self, neighbor):
        return self.adjacent[neighbor]["int_range"]
    
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

    def add_edge(self, frm, to, cost = {}):
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
                node_obj = {"id_from": v.get_id(), "id_to": w.get_id(), 
                            "flows": v.get_flows(w), "int_range": v.get_int_range(w)}
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
    
    def decide_int_range(self):
        int_range_channel = {}
        to_decide = self.compare_channels()
        channel_inf = self.list_channels()
        for chan in to_decide:
            nodes = channel_inf[chan]
            for inf in nodes:
                if inf["int_range"]:
                    if chan in int_range_channel.keys():
                        int_range_channel[chan].append(inf)
                    else:
                        int_range_channel[chan] = [inf]
        print int_range_channel
    
    def flow_path(self):
        for v in self:
            for w in v.get_connections():
                print "QUE ES W: %s" %w
                
                
    
if __name__ == '__main__':

    ######################################################
    #                     SCENARIO 1                     #             
    ######################################################
    
    g = Graph()
    #g.add_vertex('S')
    si = g.add_vertex('MB')
    print "ADD_VERTEX: %s" %si
    g.add_vertex('SB')
    g.add_vertex('MA')
    g.add_vertex('SA')
    g.add_vertex('MS')
    g.add_vertex("SS")

    g.add_edge('MB', 'SB', {"channel": 56, "flows": 1, "int_range": False})  
    g.add_edge('MB', 'MA', {"channel": 36, "flows": 4, "int_range": True})
    g.add_edge('SB', 'SA', {"channel": 52, "flows": 1, "int_range": False})
    g.add_edge('MA', 'MS', {"channel": 44, "flows": 4, "int_range": False})
    g.add_edge('SA', 'SS', {"channel": 36, "flows": 1, "int_range": True})
    
    #g.compare_channels()
    g.decide_int_range()
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
    
    ######################################################
    #                     SCENARIO 2                     #             
    ######################################################
    print "\n" + "SCENARIO 2" + "\n"
    
    p = Graph()
    #g.add_vertex('S')
    si = p.add_vertex('S1')
    print "ADD_VERTEX: %s" %si
    p.add_vertex('S2')
    p.add_vertex('S3')
    p.add_vertex('STA1')
    p.add_vertex('STA2')
    p.add_vertex("STA3")

    p.add_edge('S1', 'STA1', {"channel": 36, "flows": 1, "int_range": True})  
    p.add_edge('S2', 'STA2', {"channel": 36, "flows": 3, "int_range": True})
    p.add_edge('S3', 'STA3', {"channel": 36, "flows": 5, "int_range": True})
        
    #p.compare_channels()
    p.decide_int_range()
    p.flow_path()
    
    for v in p:
        for w in v.get_connections():
            #print "AQUIIII CARAJO"
            #print w
            vid = v.get_id()
            wid = w.get_id()
            print 'Channel: ( %s , %s, %3d)'  % ( vid, wid, v.get_channel(w))
            print 'Flows: ( %s , %s, %3d)'  % ( vid, wid, v.get_flows(w))

    for v in p:
        print 'p.vert_dict[%s]=%s' %(v.get_id(), p.vert_dict[v.get_id()])


