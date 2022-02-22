
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
    