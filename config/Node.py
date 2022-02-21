class Node:

    def __init__(self, shard_list):
        self.shard_list=sorted(shard_list, key=lambda x: x.size)
        self.node_name = self.shard_list[0].node

    def add_shard(self, shard):
        self.shard_list.append(shard)
    
    def remove_shard(self, shard):
        self.shard_list.remove(shard)

    def get_total_disk_usage(self):
        return sum([x.size for x in self.shard_list])

    def get_subset_node(self,function):
        return Node([shard for shard in self.shard_list if function(shard)])

    def get_size(self):
        return len(self.shard_list)
    
    def get_size_inactive_shards(self):
        return len(self.get_shard_subset(lambda shard: not shard.active))
        