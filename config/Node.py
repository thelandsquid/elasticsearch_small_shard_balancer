class Node:

    def __init__(self, shard_list):
        self.shard_list=sorted(shard_list, key=lambda x: x.size)
        self.node_name = self.shard_list[0].node

    def get_total_disk_usage(self):
        return sum([x.size for x in self.shard_list])