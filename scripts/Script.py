
from abc import abstractmethod


class Script():

    #Returns tuples of variable names, default values, and their description
    
    @classmethod
    @abstractmethod
    def get_required_args(cls):
        pass

    #Returns string of script name
    @classmethod
    @abstractmethod
    def get_script_name(cls):
        pass
    
    @classmethod
    @abstractmethod
    def get_description(cls):
        pass


    #Returns list of StringVar() objects to store in args
    @classmethod
    @abstractmethod
    def get_options_frame(cls, notebook):
        pass

    @classmethod
    @abstractmethod
    def run(cls, var_dict, args, gui_script=False):
        pass