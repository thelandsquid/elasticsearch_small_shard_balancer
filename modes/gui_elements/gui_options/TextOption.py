
from abc import abstractmethod
from tkinter import *

from modes.gui_elements.gui_options.Option import Option


class TextOption(Option):

    def __init__(self,notebook,args):
        super(TextOption, self).__init__(notebook,args)
        
    def get_option_element(self):
        return Entry(self)
    
    def get_value(self):
        return self.option_element.get()
    
    def set_default_value(self, default_value):
        self.option_element.delete(0,END)
        self.option_element.insert(0,default_value)