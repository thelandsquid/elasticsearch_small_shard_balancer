from collections import defaultdict

class FileSizeDict:

    fileSizeDict = defaultdict(lambda:-1)

    def __init__(self):
        self.fileSizeDict['b']=1
        self.fileSizeDict['kb']=1000
        self.fileSizeDict['mb']=1000000
        self.fileSizeDict['gb']=1000000000

    def get(self,fileSize):
        return self.fileSizeDict[fileSize]