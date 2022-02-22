from collections import defaultdict
from pydoc import ispackage
from tkinter import N
from config.DataStore import DataStore

from config.FileSizeDict import FileSizeDict

class ShardGrowth:

    def __init__(self,file_name_1,file_name_2,use_primary,limit):
        Data1 = DataStore()
        if Data1.setup(file_name_1)==-1:
            return

        Data2 = DataStore()
        if Data2.setup(file_name_2)==-1:
            return

        use_primary = use_primary.lower()
        if use_primary=='t' or use_primary=='true':
            use_primary=True
        elif use_primary=='f' or use_primary=='false':
            use_primary=False
        else:
            print('Invalid value for \"use_only_primary_shards\"')
            return
        
        if not limit.isdigit():
            print('Invalid limit')
            return

        self.simulate(Data1,Data2,use_primary,int(limit))

    @classmethod
    def get_script_name(cls):
        return "Shard Growth Script"


    @classmethod
    def get_required_args(cls):
        args_list = []
        args_list.append(("file_name1", "demo1.txt", "File to read the past data in from"))
        args_list.append(("file_name2", "demo2.txt", "File to read the current data in from"))
        args_list.append(("use_only_primary_shards", "T", "Whether to use only primary shards or not (T or F)"))
        args_list.append(("limit", "20", "Limit on how many indices to print (per node)"))
        return args_list

    def simulate(self,datastore1,datastore2,use_primary,limit):
        print("FIND FASTEST GROWING SHARDS PER NODE")
        print("--------------------------------------------")
        for node1 in sorted(datastore1.nodes, key=lambda x:x.node_name):
            node2 = None
            for n in datastore2.nodes:
                if node1.node_name==n.node_name:
                    node2=n
                    break
            self.print_single_node(node1, node2, use_primary, limit)
            print("--------------------------------------------")
            print('\n\n')
    
    def print_single_node(self, node1, node2, use_primary, limit):
        print("NODE: "+node1.node_name)

        total_growth = 0
        shard_dict_temp = defaultdict(lambda:-1)
        shard_dict = defaultdict(lambda:0)
        for shard in node1.shard_list:
            if not use_primary or shard.is_primary:
                shard_dict_temp[shard.index] = shard.size
        
        for shard in node2.shard_list:
            if shard_dict_temp[shard.index]>=0: #Should relocating shards from appearing
                shard_dict[shard.index] = shard.size - shard_dict_temp[shard.index]

        total_growth = sum([x for x in shard_dict.values()])
        
        print("TOTAL GROWTH: ",FileSizeDict().size_to_text(total_growth))
        print("--------------------------------------------")
        print("{:<50} {:<20}".format("Index","Growth"))

        i = 0
        for k, v in sorted(shard_dict.items(), key=lambda x:x[1], reverse=True):
            if v is None or v == 0:
                break
            print("{:<50} {:<20}".format(k,str(FileSizeDict().size_to_text(v))))
            i+=1
            if(i is not None and i>=limit):
                break