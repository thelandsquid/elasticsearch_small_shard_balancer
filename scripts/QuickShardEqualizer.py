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
        return "Quickly Equalize Shards"

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
        return args_list
    
    @classmethod
    def run(cls, args, var_dict, gui_script=False):
        if gui_script:
            Data = DataStore()
            if Data.setup_text(var_dict['file1'].get())==-1:
                return 'Invalid input file'
            return cls.simulate(Data.nodes)
    
    @classmethod
    def simulate(cls, nodes):
        best_score, best_moves, best_nodes = -1, None, None
        subset_nodes = cls.create_subset(nodes)
        output = cls.print_node_balance(subset_nodes, nodes, 'BEFORE BALANCING')

        temp_nodes = copy.deepcopy(subset_nodes)
        temp_moves = cls.get_moves(temp_nodes)
        temp_score = cls.disk_score(Move.apply_moves(nodes) if False else temp_nodes)
        if best_moves is None or temp_score<best_score:
            best_score = temp_score
            best_moves = temp_moves
            best_nodes = temp_nodes
        
        moved_final_nodes = Move.apply_moves(nodes, best_moves)
        output += cls.print_node_balance(best_nodes, moved_final_nodes, 'AFTER BALANCING')

        best_moves, best_nodes = best_moves, best_nodes
        return output + cls.print_best_moves(best_moves)

    @classmethod
    def create_subset(cls, nodes):
        return copy.deepcopy(nodes)
    
    @classmethod
    def get_shard_index(cls, max_node):
        return random.randint(0, len(max_node.shard_list)-1)

    @classmethod
    def make_move(cls,nodes):
        max_node, min_node = cls.get_max_min_nodes(nodes)

        max_node_shard_list = sorted(max_node.shard_list, key=lambda x:x.size)
        picked_index = 0
        while max_node_shard_list[picked_index].size==0 or cls.my_any(max_node_shard_list[picked_index].index, min_node):
            picked_index+=1

        shard = max_node.shard_list.pop(picked_index)
        min_node.shard_list.append(shard)


        return Move(shard, max_node.node_name, min_node.node_name)
    
    @classmethod
    def print_node_balance(cls,print_nodes,initial_nodes,message=''):
        initial_node_dict = {}
        for i_node in initial_nodes:
            initial_node_dict[i_node.node_name] = i_node

        output = "SHARDS PER NODE "+message+'\n'
        output += "{:<20} {:<15} {:<20}\n".format("Node","Total_Shards","Total_Disk_Usage")
        for node in print_nodes:
            output += "{:<20} {:<15} {:<20}\n".format(str(node.node_name),initial_node_dict[node.node_name].get_size(),FileSizeDict().size_to_text(initial_node_dict[node.node_name].get_total_disk_usage()))
        return output+'\n'
    
    @classmethod
    def print_best_moves(cls, best_moves):
        output = ''
        for move in best_moves:
            output += str(move)+ ("" if move==best_moves[-1] else ",") + "\n"
        return output+'\n'