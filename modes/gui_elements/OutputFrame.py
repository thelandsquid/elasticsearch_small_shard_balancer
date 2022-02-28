import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import *

from modes.gui_elements.FileSelector import FileSelector


class OutputFrame(tk.Frame):

    def __init__(self,notebook,script,args):
        super(OutputFrame, self).__init__(notebook)
        self.parent_frame = notebook
        self.grid_rowconfigure(0, weight=2)
        self.grid_rowconfigure(1, weight=6)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.script=script
        self.args=args

        self.self_label = Label(self, font=('Arial bold',15), text="Output")
        self.self_label.grid(row=0, column=0, padx=5, pady=5, sticky=SW)

        self.self_T = ScrolledText(self, height=10)
        self.self_T.bind("<Key>", lambda e: "break")
        self.self_T.grid(row=1,column=0,padx=5,pady=5,sticky=NSEW)

        self.run_program_button = ttk.Button(
            self,
            text = "Run Program",
            command = self.parent_frame.run_program
        )
        self.run_program_button.grid(row=2,column=0,padx=5,pady=5,sticky=NSEW)

    def set_output(self,output_str):
        self.self_T.delete("1.0", END)
        self.self_T.insert(END,output_str)