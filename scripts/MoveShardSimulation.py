from abc import abstractmethod
import copy
import random
from re import sub
from abc import abstractmethod
from config.FileSizeDict import FileSizeDict

from config.Move import Move
from scripts.Script import Script

class Move_Shard_Simulation(Script):

    def __init__(self, nodes, condition_on_initial, num_sims):
        self.nodes = nodes
        self.subset_nodes = self.create_subset()
        self.condition_on_initial = condition_on_initial
        self.simulate(num_sims)

    
    def simulate(self, num_sims):
        best_score, best_moves, best_nodes = -1, None, None
        self.print_node_balance(self.subset_nodes, self.nodes, 'BEFORE BALANCING')

        for i in range(num_sims):
            temp_nodes = copy.deepcopy(self.subset_nodes)
            temp_moves = self.get_moves(temp_nodes)
            temp_score = self.disk_score(Move.apply_moves(self.nodes) if self.condition_on_initial else temp_nodes)
            if best_moves is None or temp_score<best_score:
                best_score = temp_score
                best_moves = temp_moves
                best_nodes = temp_nodes
        
        moved_final_nodes = Move.apply_moves(self.nodes, best_moves)
        self.print_node_balance(best_nodes, moved_final_nodes, 'AFTER BALANCING')

        self.best_moves, self.best_nodes = best_moves, best_nodes
        self.print_best_moves()

    @classmethod
    def disk_score(cls,nodes):
        max_disk = max([node.get_total_disk_usage() for node in nodes])
        min_disk = min([node.get_total_disk_usage() for node in nodes])
        return max_disk-min_disk

    @classmethod
    def get_moves(cls,nodes):
        moves = []
        while cls.is_unbalanced(nodes):
            moves.append(cls.make_move(nodes))

        return moves

    
    @classmethod
    def print_node_balance(cls,print_nodes,initial_nodes,message=''):
        initial_node_dict = {}
        for i_node in initial_nodes:
            initial_node_dict[i_node.node_name] = i_node

        output = "SHARDS PER NODE "+message+'\n'
        output += "{:<20} {:<15} {:<20} {:<15} {:<20}\n".format("Node","Subset_Shards","Subset_Disk_Usage","Total_Shards","Total_Disk_Usage")
        for node in print_nodes:
            output += "{:<20} {:<15} {:<20} {:<15} {:<20}\n".format(str(node.node_name),node.get_size(),FileSizeDict().size_to_text(node.get_total_disk_usage()),initial_node_dict[node.node_name].get_size(),FileSizeDict().size_to_text(initial_node_dict[node.node_name].get_total_disk_usage()))
        return output+'\n'
    
    
    @classmethod
    def print_best_moves(cls, best_moves):
        output = ''
        for move in best_moves:
            output += str(move)+",\n"
        return output+'\n'

    @classmethod
    @abstractmethod
    def make_moves(cls,nodes):
        pass

    # def make_move(self,nodes):
    #     max_node, min_node = self.get_max_min_nodes(nodes)
    #     picked_index = self.get_shard_index(max_node)

    #     while max_node.shard_list[picked_index].active or self.my_any(max_node.shard_list[picked_index].index, min_node):
    #         picked_index = random.randint(0, len(max_node.shard_list)-1)
    #     shard = max_node.shard_list.pop(picked_index)
    #     min_node.shard_list.append(shard)

    #     return Move(shard, max_node.node_name, min_node.node_name)

    @classmethod
    def my_any(cls,max_index, min_node):
        for x in min_node.shard_list:
            if x.index == max_index:
                return True
        return False

    @classmethod
    def get_max_min_nodes(cls,nodes):
        max_node = max(nodes, key=lambda node: node.get_size())
        min_node = min(nodes, key=lambda node: node.get_size())
        return max_node, min_node

    @classmethod
    def is_unbalanced(cls,nodes):
        max_node, min_node = cls.get_max_min_nodes(nodes)
        return (max_node.get_size()-min_node.get_size())>1
    
    @classmethod
    @abstractmethod
    def get_shard_index(self, max_node):
        pass

    @classmethod
    @abstractmethod
    def create_subset(self):
        pass