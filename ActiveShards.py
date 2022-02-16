from collections import defaultdict
from platform import node
import re
import random
import json


from config.Shard import Shard

def readFileForActiveShards(fileName):
    shard_dict = defaultdict(lambda:None)

    with open(fileName) as fp:
        for line in fp:
            shard = Shard.parseShard(line)
            if shard is not None:
                index_shard = shard_dict[get_index_template(shard)]
                if index_shard is None or shard.index>index_shard.index:
                        shard_dict[get_index_template(shard)] = shard

    node_dict = defaultdict(list)
    for shard in shard_dict.values():
        node_dict[shard.node].append(shard)
    return node_dict

def get_index_template(shard):
    return re.sub('[0-9.]+$','',shard.index)

def print_active_shards(node_dict):
    for key in node_dict:
        for shard in node_dict[key]:
            print('\t'+str(shard))
    
    print('-----------------------------------')

    for key in node_dict:
        print(key+":\t"+str(len(node_dict[key])))

def get_active_shards(fileName, print=False):
    node_dict = readFileForActiveShards(fileName)
    if print:
        print_active_shards(node_dict)
    return node_dict