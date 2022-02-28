import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import *

from modes.gui_elements.FileSelector import FileSelector
from modes.gui_elements.OutputFrame import OutputFrame


class ScriptFrame(tk.Frame):

    def __init__(self,notebook,var_dict,script):
        super(ScriptFrame, self).__init__(notebook)
        self.script=script
        self.var_dict=var_dict
        notebook.add(self, text=self.script.get_script_name())

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=6)
        self.grid_columnconfigure(0, weight=1)

        self.header_frame()
        self.options_frame = script.get_options_frame(self)
        self.options_frame.grid(row=1, column=0, padx=5, pady=15, sticky=NSEW)
        self.output_frame = OutputFrame(self,self.script,'temp args')
        self.output_frame.grid(row=2, column=0, padx=5, pady=15, sticky=NSEW)

    def header_frame(self):
        self.info_frame = Frame(self)
        self.info_frame.grid(row=0, column=0, padx=5, pady=15, sticky=NSEW)
        self.info_frame_title = Label(self.info_frame, text=self.script.get_script_name(), font=('Arial',30))
        self.info_frame_title.pack()
        self.info_frame_description = Label(self.info_frame, text=self.script.get_description(), font=('Arial',12))
        self.info_frame_description.pack()
    
    def run_program(self):
        self.output_frame.set_output(self.script.run(self.options_frame.get(),self.var_dict,gui_script=True))