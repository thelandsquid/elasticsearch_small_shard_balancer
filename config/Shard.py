from .FileSizeDict import FileSizeDict
import re

class Shard:

    def __init__(self, index, size, node, is_primary, active=False):
        self.index=index
        self.size=self.convertSize(size)
        self.node=node
        self.is_primary = is_primary=='p'
        self.active=active;

    def convertSize(self,sizeStr):
        fileSize = re.sub('[0-9.]+','',sizeStr)
        size = float(re.sub('[a-z]+','',sizeStr))
        return size * self.convertFileSizeToMult(fileSize)

    def convertFileSizeToMult(self,fileSize):
        return FileSizeDict().get(fileSize)

    def __str__(self):
        return self.index+"\t"+self.node

    def setActive(self):
        self.active=True

    def __eq__(self, obj):
        return isinstance(obj, Shard) and obj.index == self.index and obj.node == self.node

    #Expected format of [index-name   size   node-name   isPrimary]
    @classmethod
    def parseShard(cls, line):
        lineList = line.split()
        if len(lineList)==3: #missing size
            return Shard(lineList[0], '0b', lineList[1], lineList[2])
        elif len(lineList)==4:
            return Shard(lineList[0], lineList[1], lineList[2], lineList[3])
        return None