from collections import defaultdict
import re
import random
import json

class Move:
    def __init__(self, shard, from_node, to_node):
        self.shard=shard
        self.from_node=from_node
        self.to_node=to_node

    def __str__(self):
        #TODO make it support replicas by adding shard number to input
        return json.dumps({"move":{"index":self.shard.index,"shard":0,"from_node":self.from_node,"to_node":self.to_node}})

class Node:

    def __init__(self, shard_list):
        self.shard_list=sorted(shard_list, key=lambda x: x.size)
        self.node_name = self.shard_list[0].node

class FileSizeDict:

    fileSizeDict = defaultdict(lambda:-1)

    def __init__(self):
        self.fileSizeDict['b']=1000
        self.fileSizeDict['kb']=1000000
        self.fileSizeDict['mb']=1000000000
        self.fileSizeDict['gb']=1000000000000

    def get(self,fileSize):
        return self.fileSizeDict[fileSize]


class Shard:

    def __init__(self, index, size, node, is_primary):
        self.index=index
        self.size=self.convertSize(size)
        self.node=node
        self.isPrimary = is_primary=='p'

    def convertSize(self,sizeStr):
        fileSize = re.sub('[0-9.]+','',sizeStr)
        size = float(re.sub('[a-z]+','',sizeStr))
        return size * self.convertFileSizeToMult(fileSize)

    def convertFileSizeToMult(self,fileSize):
        return FileSizeDict().get(fileSize)

#Expected format of [index-name   size   node-name   isPrimary]
def parseShard(line):
    lineList = line.split()
    if len(lineList)==3: #missing size
        return Shard(lineList[0], '0b', lineList[1], lineList[2])
    elif len(lineList)==4:
        return Shard(lineList[0], lineList[1], lineList[2], lineList[3])
    return None

def readFile(fileName):
    nodes_dict = defaultdict(list)

    with open(fileName) as fp:
        for line in fp:
            shard = parseShard(line)
            if shard is not None and shard.size < 1000000000 and shard.size >= 0: #less than 100MB
                nodes_dict[shard.node].append(shard)

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
        print(node.node_name.__str__()+": "+str(len(node.shard_list)))
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
    nodes = readFile("demo.txt")
    moves = get_moves(nodes)
    for move in moves:
        print(move.__str__()+",")

main()