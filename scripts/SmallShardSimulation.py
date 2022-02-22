from abc import abstractmethod
import copy
import random
from re import sub
from config.DataStore import DataStore
from config.FileSizeDict import FileSizeDict


from config.Move import Move
from scripts.MoveShardSimulation import Move_Shard_Simulation

class Small_Shard_Simulation(Move_Shard_Simulation):

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

        super(Small_Shard_Simulation, self).__init__(Data.nodes, False, num_sims)

    @classmethod
    def get_script_name(cls):
        return "Move Small Shard Simulation"


    @classmethod
    def get_required_args(cls):
        args_list = []
        args_list.append(("file_name", "demo1.txt", "File to read the data in from"))
        args_list.append(("size_threshold", "100mb", "Maximum size of a shard to move"))
        return args_list

    def create_subset(self):
        subset_nodes = []
        for node in self.nodes:
            subset_nodes.append(node.get_subset_node(lambda x: x.size<self.size_threshold))
        return subset_nodes
    
    def get_shard_index(self, max_node):
        return random.randint(0, len(max_node.shard_list)-1)