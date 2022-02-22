from collections import defaultdict
from http.client import CONTINUE
import re
import random
import json
import argparse
import copy
from config.DataStore import DataStore

from ActiveShards import *
from scripts.ShardGrowth import ShardGrowth
from scripts.SmallShardSimulation import Small_Shard_Simulation
from scripts.LargestIndices import LargestIndicesScript
from config.FileSizeDict import FileSizeDict

def user_commands():
    scripts = [LargestIndicesScript, ShardGrowth, Small_Shard_Simulation]
    
    print('----------------------------------------')
    print('    ELASTICSEARCH ASSISTANCE SCRIPTS    ')
    print('----------------------------------------')

    while(True):
        print('Select script by number: ')
        for i in range(len(scripts)):
            print('['+str(i+1)+']',scripts[i].get_script_name())
        print('[0] EXIT PROGRAM')

        choice = input()
        if not choice.isdigit():
            print('CHOICE MUST BE A NUMERICAL VALUE')
            continue
        choice = int(choice)

        if choice==0:
            exit(0)
        else:
            required_args = scripts[choice-1].get_required_args()
            args_list = []
            for (var_name, default, desc) in required_args:
                print("Set \""+var_name+"\" --- "+desc+"  ["+str(default)+"]")
                user_input = input()
                if user_input=='':
                    user_input = default
                args_list.append(user_input)
            scripts[choice-1](*args_list)
            print('\n\n')



def main():
    # fileName = 'demo1.txt'
    # fileName2 = 'demo2.txt'
    # Data = DataStore()
    # Data.setup(fileName)
    # Data2 = DataStore()
    # Data2.setup(fileName2)

    # Small_Shard_Simulation(Data.nodes, args.size, 10).print_best_moves()
    # print_largest_indices(Data,20)    
    # print()
    # ShardGrowth(Data, Data2, True, 10)
    user_commands()


parser = argparse.ArgumentParser(description='Output moves to balance shards')
parser.add_argument('-s', '--size', required=True, help='Maximum size of shards to move')
parser.add_argument('-o', '--only_inactive', action='store_true')

args = parser.parse_args()

global file_size_dict
file_size_dict = FileSizeDict()
main()