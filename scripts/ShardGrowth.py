from collections import defaultdict
from pydoc import ispackage
from tkinter import N
from config.DataStore import DataStore

from config.FileSizeDict import FileSizeDict
from modes.gui_elements.gui_options.OptionsFrame import OptionsFrame
from modes.gui_elements.gui_options.TextOption import TextOption

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
        return "Shard Growth"

    @classmethod
    def run(cls, args, var_dict=None, gui_script=False):
        if gui_script:
            Data1 = DataStore()
            if Data1.setup_text(var_dict['file1'].get())==-1:
                return "Error reading file input"

            Data2 = DataStore()
            if Data2.setup_text(var_dict['file2'].get())==-1:
                return "Error reading file input"

            args[0] = args[0].lower()
            if args[0]=='t' or args[0]=='true':
                args[0]=True
            elif args[0]=='f' or args[0]=='false':
                args[0]=False
            else:
                return 'Invalid value for \"use_only_primary_shards\"'
            
            if not args[1].isdigit():
                return 'Invalid limit'

            return cls.simulate(Data1,Data2,args[0],int(args[1]))
        else:
            Data1 = DataStore()
            if Data1.setup(args[0])==-1:
                return

            Data2 = DataStore()
            if Data2.setup(args[1])==-1:
                return

            args[2] = args[2].lower()
            if args[2]=='t' or args[2]=='true':
                args[2]=True
            elif args[2]=='f' or args[2]=='false':
                args[2]=False
            else:
                print('Invalid value for \"use_only_primary_shards\"')
                return
            
            if not args[3].isdigit():
                print('Invalid limit')
                return

            return cls.simulate(Data1,Data2,args[2],int(args[3]))

    @classmethod
    def get_options_frame(cls,notebook):
        return OptionsFrame(notebook, cls.get_required_args(True))

    @classmethod
    def get_required_args(cls, only_gui=False):
        args_list = []
        if not only_gui:
            args_list.append((TextOption, "file_name1", "demo1.txt", "File to read the past data in from"))
            args_list.append((TextOption, "file_name2", "demo2.txt", "File to read the current data in from"))
        args_list.append((TextOption, "use_only_primary_shards", "T", "Whether to use only primary shards or not (T or F)"))
        args_list.append((TextOption, "limit", "20", "Limit on how many indices to print (per node)"))
        return args_list

    @classmethod
    def get_description(cls):
        return "Shows growth of shards over time by comparing the size of shards in file-1 and file-2."

    @classmethod
    def simulate(cls,datastore1,datastore2,use_primary,limit):
        output = "FIND FASTEST GROWING SHARDS PER NODE\n"
        output += "--------------------------------------------\n"
        for node1 in sorted(datastore1.nodes, key=lambda x:x.node_name):
            node2 = None
            for n in datastore2.nodes:
                if node1.node_name==n.node_name:
                    node2=n
                    break
            output += cls.print_single_node(node1, node2, use_primary, limit)
            output += "--------------------------------------------\n"
            output += '\n\n\n'
        return output
    
    @classmethod
    def print_single_node(cls, node1, node2, use_primary, limit):
        output = ("NODE: "+node1.node_name+"\n")

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
        
        output += "TOTAL GROWTH: \t"+str(FileSizeDict().size_to_text(total_growth))
        output += "\n--------------------------------------------\n"
        output += "{:<50} {:<20}\n".format("Index","Growth")

        i = 0
        for k, v in sorted(shard_dict.items(), key=lambda x:x[1], reverse=True):
            if v is None or v == 0:
                break
            output += "{:<50} {:<20}\n".format(k,str(FileSizeDict().size_to_text(v)))
            i+=1
            if(i is not None and i>=limit):
                break
        return output