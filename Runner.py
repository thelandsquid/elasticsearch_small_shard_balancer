from collections import defaultdict
import re
import random
import json
import argparse

from config.Shard import Shard
from config.Move import Move
from config.Node import Node
from ActiveShards import *



def readFile(fileName):
    nodes_dict = defaultdict(list)

    with open(fileName) as fp:
        for line in fp:
            shard = Shard.parseShard(line)
            if shard is not None and shard.size < int(args.size) and shard.size >= 0: #less than 100MB
                nodes_dict[shard.node].append(shard)

    return nodes_dict_to_nodes(nodes_dict)

def nodes_dict_to_nodes(nodes_dict):
    nodes = []
    for key in nodes_dict:
        nodes.append(Node(nodes_dict[key]))
    return nodes

def get_moves(nodes):
    moves = []
    print_node_balance(nodes, 'before balancing')

    while is_unbalanced(nodes):
        moves.append(make_move(nodes))

    print_node_balance(nodes, 'after balancing')
    return moves

def print_node_balance(nodes,message=''):
    print("Small shards per node "+message)
    print("-----------------")
    for node in nodes:
        print(node.node_name.__str__()+":\t"+str(len(node.shard_list))+"\t"+str(node.get_total_disk_usage()))
    print()

def make_move(nodes):
    max_node, min_node = get_max_min_nodes(nodes)
    rand_index = random.randint(0, len(max_node.shard_list)-1)
    while my_any(max_node.shard_list[rand_index].index, min_node):
        rand_index = random.randint(0, len(max_node.shard_list)-1)
    shard = max_node.shard_list.pop(rand_index)
    min_node.shard_list.append(shard)
    return Move(shard, max_node.node_name, min_node.node_name)

def my_any(max_index, min_node):
    for x in min_node.shard_list:
        if x.index == max_index:
            return True
    return False

def get_max_min_nodes(nodes):
    maximum, minimum = -1, -1
    max_node, min_node = None, None
    for node in nodes:
        if len(node.shard_list) > maximum or maximum==-1:
            maximum = len(node.shard_list)
            max_node = node
        if len(node.shard_list) < minimum or minimum==-1:
            minimum = len(node.shard_list)
            min_node = node
    return max_node, min_node

def is_unbalanced(nodes):
    max_node, min_node = get_max_min_nodes(nodes)
    return (len(max_node.shard_list)-len(min_node.shard_list))>1

def main():
    fileName = 'demo.txt'
    #TODO change to read data in same way for each setting, remove nodes based on needed metrics
    #TODO add boolean is_active to each shard (-f option to balance factoring active shards into total size)
    #TODO Set goal? Equalize shards, equalize disk, best of both
    if args.only_active:
        nodes = nodes_dict_to_nodes(get_active_shards(fileName, print=False))
    else:
        nodes = readFile(fileName)
    moves = get_moves(nodes)
    for move in moves:
        print(move.__str__()+",")
    
    print()
    #get_active_shards(fileName, print=True)


parser = argparse.ArgumentParser(description='Output moves to balance shards')
parser.add_argument('-s', '--size', required=True, help='Maximum size of shards to move')
parser.add_argument('-o', '--only_active', action='store_true')

args = parser.parse_args()
main()