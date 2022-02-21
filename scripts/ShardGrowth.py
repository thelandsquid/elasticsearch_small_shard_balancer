from collections import defaultdict
from tkinter import N

from config.FileSizeDict import FileSizeDict

class ShardGrowth:

    def __init__(self,datastore1,datastore2,limit=None):
        self.simulate(datastore1,datastore2,limit)

    def simulate(self,datastore1,datastore2,limit):
        print("FIND FASTEST GROWING SHARDS PER NODE")
        print("--------------------------------------------")
        for node1 in datastore1.nodes:
            node2 = None
            for n in datastore2.nodes:
                if node1.node_name==n.node_name:
                    node2=n
                    break
            self.print_single_node(node1, node2, limit)
            print("--------------------------------------------")
    
    def print_single_node(self, node1, node2, limit):
        print("NODE: "+node1.node_name)
        print("{:<50} {:<20}".format("Index","Growth"))

        shard_dict_temp = defaultdict(lambda:0)
        shard_dict = defaultdict(lambda:0)
        for shard in node1.shard_list:
            shard_dict_temp[shard.index] = shard.size
        
        for shard in node2.shard_list:
            shard_dict[shard.index] = shard.size - shard_dict_temp[shard.index]
        
        i = 0
        for k, v in sorted(shard_dict.items(), key=lambda x:x[1], reverse=True):
            print("{:<50} {:<20}".format(k,str(FileSizeDict().size_to_text(v))))
            i+=1
            if(i is not None and i>=limit):
                break