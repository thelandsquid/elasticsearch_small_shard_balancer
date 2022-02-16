import json

class Move:
    def __init__(self, shard, from_node, to_node):
        self.shard=shard
        self.from_node=from_node
        self.to_node=to_node

    def __str__(self):
        #TODO make it support replicas by adding shard number to input
        return json.dumps({"move":{"index":self.shard.index,"shard":0,"from_node":self.from_node,"to_node":self.to_node}})
