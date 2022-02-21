import json
import copy

class Move:
    def __init__(self, shard, from_node, to_node):
        self.shard=shard
        self.from_node=from_node
        self.to_node=to_node

    def __str__(self):
        #TODO make it support replicas by adding shard number to input
        return json.dumps({"move":{"index":self.shard.index,"shard":0,"from_node":self.from_node,"to_node":self.to_node}})

    @classmethod
    def apply_moves(cls, nodes, moves):
        copied_nodes = copy.deepcopy(nodes)

        node_dict = {}
        for node in copied_nodes:
            node_dict[node.node_name] = node
        
        for move in moves:
            node_dict[move.from_node].remove_shard(move.shard)
            node_dict[move.to_node].add_shard(move.shard)
        
        return copied_nodes