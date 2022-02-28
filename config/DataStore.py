
from collections import defaultdict
from config.Index import Index
from config.Node import Node
from config.Shard import Shard
import re

class DataStore:

    def __init__(self):
        self.nodes = None
        self.indices_dict = None
    
    def setup(self, fileName):
        return self.readFile(fileName)
    
    def setup_text(self, file_text):
        self.nodes_dict = defaultdict(list)

        try:
            for line in file_text.splitlines():
                shard = Shard.parseShard(line)
                if shard is not None:
                    self.nodes_dict[shard.node].append(shard)

            nodes_list = self.nodes_dict_to_nodes()
            self.setup_active_shards(nodes_list)
        except:
            print('Error reading file')
            return -1

        self.nodes = nodes_list
        return 0

    def readFile(self, fileName):
        self.nodes_dict = defaultdict(list)

        try:
            with open(fileName) as fp:
                for line in fp:
                    shard = Shard.parseShard(line)
                    if shard is not None:
                        self.nodes_dict[shard.node].append(shard)

            nodes_list = self.nodes_dict_to_nodes()
            self.setup_active_shards(nodes_list)
        except:
            print('Error reading file')
            return -1

        self.nodes = nodes_list
        return 0

    def nodes_dict_to_nodes(self):
        nodes = []
        for key in self.nodes_dict:
            nodes.append(Node(self.nodes_dict[key]))
        return nodes

    def setup_active_shards(self, nodes_list):
        shard_dict = defaultdict(lambda:None)
        self.indices_dict = defaultdict(lambda:Index())

        for node in nodes_list:
            for shard in node.shard_list:
                index_template = self.get_index_template(shard)

                self.indices_dict[index_template].add_shard(shard, index_template)

                index_shard = shard_dict[index_template]
                if index_shard is None or shard.index>index_shard.index:
                    shard_dict[index_template] = shard


        #Set flag on active shards
        for shard in shard_dict.values():
            shard.setActive()
    
    def get_index_template(self,shard):
        return re.sub('-?[0-9.]+$','',shard.index)
        