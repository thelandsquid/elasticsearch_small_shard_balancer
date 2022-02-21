from collections import defaultdict
import re
import random
import json
import argparse
import copy
from config.DataStore import DataStore

from ActiveShards import *
from scripts.ShardGrowth import ShardGrowth
from scripts.SmallShardSimulation import Small_Shard_Simulation
from scripts.LargestIndices import print_largest_indices
from config.FileSizeDict import FileSizeDict

def main():
    fileName = 'demo.txt'
    fileName2 = 'demo2.txt'
    #TODO change to read data in same way for each setting, remove nodes based on needed metrics
    #TODO add boolean is_active to each shard (-f option to balance factoring active shards into total size)
    #TODO Set goal? Equalize shards, equalize disk, best of both
    Data = DataStore()
    Data.setup(fileName)
    Data2 = DataStore()
    Data2.setup(fileName2)

    Small_Shard_Simulation(Data.nodes, args.size, 10)
    print_largest_indices(Data,20)    
    print()
    ShardGrowth(Data, Data2, 10)


parser = argparse.ArgumentParser(description='Output moves to balance shards')
parser.add_argument('-s', '--size', required=True, help='Maximum size of shards to move')
parser.add_argument('-o', '--only_inactive', action='store_true')

args = parser.parse_args()

global file_size_dict
file_size_dict = FileSizeDict()
main()