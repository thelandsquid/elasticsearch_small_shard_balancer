from abc import abstractmethod
import tkinter as tk
from tkinter import *
from tkinter import ttk
from turtle import title

from idlelib.tooltip import Hovertip

class Option(tk.Frame):

    def __init__(self,notebook,args):
        super(Option, self).__init__(notebook, borderwidth=1, relief=RIDGE)
        self.grid_columnconfigure(0, weight=5)
        self.grid_columnconfigure(1, weight=10)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.title = args[1]
        self.desc = args[3]

        self.title_L = Label(self, font=('Arial',12),text=self.title)
        self.title_L.grid(row=0,column=0,padx=10,sticky=W)

        self.option_element = self.get_option_element()
        self.option_element.grid(row=0,column=1,padx=5,sticky=E)

        self.desc_button = ttk.Button(
            self,
            text = "?",
            state = "disabled"
        )
        self.desc_button.grid(row=0,column=2,pady=5,padx=5,sticky=E)
        self.hover_tip = Hovertip(self.desc_button, self.desc, hover_delay=100)
        self.set_default_value(args[2])


    @abstractmethod
    def set_default_value(self, default_value):
        pass

    @abstractmethod
    def get_option_element(self):
        pass

    @abstractmethod
    def get_value(self):
        pass