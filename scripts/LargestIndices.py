from config.DataStore import DataStore
from config.FileSizeDict import FileSizeDict
from scripts.Script import Script

class LargestIndicesScript(Script):

    def __init__(self, file_name, limit):
        Data = DataStore()
        if Data.setup(file_name)==-1:
            return
        if not limit.isdigit():
            print('Invalid limit')
            return
        self.print_largest_indices(Data,int(limit))
    
    @classmethod
    def get_script_name(cls):
        return "Largest Indices Script"



    @classmethod
    def get_required_args(cls):
        args_list = []
        args_list.append(("file_name", "demo1.txt", "File to read the data in from"))
        args_list.append(("limit", "20", "Limit on how many indices to print"))
        return args_list

    def print_largest_indices(self, datastore, limit=None):
        fsd, i = FileSizeDict(), 0
        print("LARGEST INDICES")
        print("{:<50} {:<20}".format("Index","Size"))
        for index in sorted(datastore.indices_dict.values(),key=lambda x:x.get_disk_size(), reverse=True):   
            print("{:<50} {:<20}".format(index.name, fsd.size_to_text(index.disk_size)))
            i+=1
            if(i is not None and i>=limit):
                break