from abc import abstractmethod
import copy
import random
from re import sub
from config.DataStore import DataStore
from config.FileSizeDict import FileSizeDict


from config.Move import Move
from modes.gui_elements.gui_options.OptionsFrame import OptionsFrame
from modes.gui_elements.gui_options.TextOption import TextOption
from scripts.MoveShardSimulation import Move_Shard_Simulation

class QuickShardEqualizer(Move_Shard_Simulation):

    def __init__(self, file_name, size_threshold, num_sims=10):
        Data = DataStore()
        if Data.setup(file_name)==-1:
            return

        try:
            if not size_threshold.isdigit():
                self.size_threshold = FileSizeDict().convertSize(size_threshold)
            else:
                self.size_threshold = int(size_threshold)
        except:
            print('Error parsing size_threshold')
            return

        super(QuickShardEqualizer, self).__init__(Data.nodes, False, num_sims)

    @classmethod
    def get_script_name(cls):
        return "Quickly Move Shards Simulation"

    @classmethod
    def get_description(cls):
        output = "Move smallest shards between nodes until each have equal number of shards.\n"
        output += "Use output with reroute API to move shards in your cluster"
        return output

    @classmethod
    def get_options_frame(cls,notebook):
        return OptionsFrame(notebook, cls.get_required_args(True))
        
    @classmethod
    def get_required_args(cls, only_gui=False):
        args_list = []
        if not only_gui:
            args_list.append((TextOption, "file_name", "demo1.txt", "File to read the data in from"))
        args_list.append((TextOption, "size_threshold", "100mb", "Maximum size of a shard to move"))
        return args_list
    
    @classmethod
    def run(cls, var_dict, args, gui_script=False):
        Data = DataStore()
        if Data.setup_text(var_dict['file1'].get())==-1:
            return 'Invalid input file'
        
        try:
            if not args[0].isdigit():
                args[0] = FileSizeDict().convertSize(args[0])
            else:
                args[0] = int(args[0])
        except:
            return 'Cannot parse size_threshold option'
        return 'Work in progress'

    def simulate(self,num_sims):
        super(QuickShardEqualizer, self).simulate(1)

    def create_subset(self):
        return copy.deepcopy(self.nodes)
    
    def get_shard_index(self, max_node):
        return random.randint(0, len(max_node.shard_list)-1)

    def make_move(self,nodes):
        #TODO Optimize to remove random index selection
        max_node, min_node = self.get_max_min_nodes(nodes)

        max_node_shard_list = sorted(max_node.shard_list, key=lambda x:x.size)
        picked_index = 0
        while max_node_shard_list[picked_index].size==0 or self.my_any(max_node_shard_list[picked_index].index, min_node):
            picked_index+=1

        shard = max_node.shard_list.pop(picked_index)
        min_node.shard_list.append(shard)


        return Move(shard, max_node.node_name, min_node.node_name)