import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import *

from modes.gui_elements.gui_options.TextOption import TextOption



class OptionsFrame(tk.Frame):

    def __init__(self,notebook, arg_list):
        super(OptionsFrame, self).__init__(notebook)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=10)
        self.grid_columnconfigure(0, weight=1)

        options_label = Label(self, font=('Arial bold',15),text='Options')
        options_label.grid(row=0,column=0,padx=5,pady=5,sticky=SW)

        options_frame = tk.Frame(self)
        options_frame.grid(row=1,column=0,sticky=NW)

        options_frame.grid_columnconfigure(0, weight=1)
        options_frame.grid_columnconfigure(1, weight=1)
        
        self.options = []
        for i in range(0,len(arg_list)//2+1,2):
            options_frame.grid_rowconfigure(i, weight=1)
            
            self.options.append(arg_list[i][0](options_frame,arg_list[i]))
            self.options[i].grid(row=i//2,column=0,padx=5,pady=5,sticky=NW)

            if i+1<len(arg_list):
                self.options.append(arg_list[i+1][0](options_frame,arg_list[i+1]))
                self.options[i+1].grid(row=i//2,column=1,padx=5,pady=5,sticky=NW)

    def get(self):
        opt_list = []
        for option in self.options:
            opt_list.append(option.get_value())
        return opt_list