from abc import abstractmethod
import copy
import random
from re import sub


from config.Move import Move
from scripts.MoveShardSimulation import Move_Shard_Simulation

class Small_Shard_Simulation(Move_Shard_Simulation):

    def __init__(self, initial_nodes, size_threshold, num_sims=10):
        self.size_threshold = int(size_threshold)
        super(Small_Shard_Simulation, self).__init__(initial_nodes, False, num_sims)

    def create_subset(self):
        subset_nodes = []
        for node in self.nodes:
            subset_nodes.append(node.get_subset_node(lambda x: x.size<self.size_threshold))
        return subset_nodes
    
    def get_shard_index(self, max_node):
        return random.randint(0, len(max_node.shard_list)-1)