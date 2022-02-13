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
    
    def __str__(self):
        return self.index+"\t"+self.node

#Expected format of [index-name   size   node-name   isPrimary]
def parseShard(line):
    lineList = line.split()
    if len(lineList)==3: #missing size
        return Shard(lineList[0], '0b', lineList[1], lineList[2])
    elif len(lineList)==4:
        return Shard(lineList[0], lineList[1], lineList[2], lineList[3])
    return None

def readFile(fileName):
    shard_dict = defaultdict(lambda:None)

    with open(fileName) as fp:
        for line in fp:
            shard = parseShard(line)
            if shard is not None:
                index_shard = shard_dict[get_index_template(shard)]
                if index_shard is None or shard.index>index_shard.index:
                        shard_dict[get_index_template(shard)] = shard

    return shard_dict.values()

def get_index_template(shard):
    return re.sub('[0-9]+$','',shard.index)


def main():
    shards = readFile("demo.txt")
    for shard in shards:
        print(shard)

main()