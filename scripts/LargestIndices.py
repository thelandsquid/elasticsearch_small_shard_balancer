import tkinter as tk
from tkinter import *
from tkinter import ttk

from config.DataStore import DataStore
from config.FileSizeDict import FileSizeDict
from modes.gui_elements.gui_options.OptionsFrame import OptionsFrame
from modes.gui_elements.gui_options.TextOption import TextOption

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
    
    def print_largest_indices(self, datastore, limit=None):
        fsd, i = FileSizeDict(), 0
        print("LARGEST INDICES")
        print("{:<50} {:<20}".format("Index","Size"))
        for index in sorted(datastore.indices_dict.values(),key=lambda x:x.get_disk_size(), reverse=True):   
            print("{:<50} {:<20}".format(index.name, fsd.size_to_text(index.disk_size)))
            i+=1
            if(i is not None and i>=limit):
                break

    @classmethod
    def get_script_name(cls):
        return "Largest Indices"


    @classmethod
    def get_required_args(cls, only_gui=False):
        args_list = []
        if not only_gui:
            args_list.append((TextOption, "file_name", "demo1.txt", "File to read the data in from"))
        args_list.append((TextOption, "limit", "20", "Limit on how many indices to print"))
        return args_list

    @classmethod
    def get_description(cls):
        return "Determine largest indices across Elasticsearch cluster."

    @classmethod
    def get_options_frame(cls,notebook):
        return OptionsFrame(notebook, cls.get_required_args(True))


    @classmethod
    def run(cls, var_dict, args, gui_script=False):
        Data = DataStore()
        if Data.setup_text(var_dict['file1'].get())==-1:
            return 'Invalid input file'
        if not args[0].isdigit():
            return 'Invalid limit option'
        return cls.get_largest_indices(Data,int(args[0]))

    
    @classmethod
    def get_largest_indices(cls, datastore, limit=None):
        fsd, i = FileSizeDict(), 0
        output_str = "LARGEST INDICES\n"
        output_str += "{:<50} {:<20}\n".format("Index","Size")
        for index in sorted(datastore.indices_dict.values(),key=lambda x:x.get_disk_size(), reverse=True):   
            output_str += "{:<50} {:<20}\n".format(index.name, fsd.size_to_text(index.disk_size))
            i+=1
            if(i is not None and i>=limit):
                break
        return output_str
