
class Index:

    def __init__(self):
        self.num_shards = 0
        self.disk_size = 0
        self.ilm_max = None
        self.name = None
    
    def get_num_shards(self):
        return self.get_num_shards
    
    def get_disk_size(self):
        return self.disk_size
    
    def get_ilm_max(self):
        return self.ilm_max

    def inc_shard_count(self):
        self.num_shards = self.num_shards+1
    
    def add_disk(self, shard_disk):
        self.disk_size = self.disk_size+shard_disk
    
    def add_shard(self, shard, name):
        if self.name is None:
            self.name = name
        self.inc_shard_count()
        self.add_disk(shard.size)