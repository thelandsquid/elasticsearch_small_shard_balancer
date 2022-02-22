from collections import defaultdict
import re

class FileSizeDict:

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(FileSizeDict, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.fileSizeDict = {'b':1, 'kb':1000, 'mb':1000000, 'gb':1000000000, 'tb':1000000000000}
        self.inv_fileSizeDict = {v: k for k, v in self.fileSizeDict.items()}

    def get(self,fileSize):
        return self.fileSizeDict[fileSize]
    
    def size_to_text(self,size):
        for value in sorted(self.inv_fileSizeDict.keys(), reverse=True):
            if size >= value:
                return str(round(size/value,2))+self.inv_fileSizeDict[value]

    def convertSize(self,sizeStr):
        fileSize = re.sub('[0-9.]+','',sizeStr)
        size = float(re.sub('[a-z]+','',sizeStr))
        return size * self.fileSizeDict[fileSize]