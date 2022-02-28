import tkinter as tk
from tkinter import *
from tkinter import ttk
from modes.gui_elements.CommandInputFrame import CommandInputFrame

class MainMenuPage(tk.Frame):

    def __init__(self,notebook,file1,file2):
        super(MainMenuPage, self).__init__(notebook)

        notebook.add(self, text='Main Menu')

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=5)
        self.grid_rowconfigure(2, weight=5)
        self.grid_columnconfigure(0, weight=1)

        self.info_frame = Frame(self)
        self.info_frame.grid(row=0, column=0, padx=5, pady=15, sticky=NSEW)
        self.info_frame_title = Label(self.info_frame, text='Elasticsearch Assistance Scripts', font=('Arial',30))
        self.info_frame_title.pack()
        self.info_frame_description = Label(self.info_frame, text='A program to help diagnose issues and gather information about Elasticesarch clusters.\nRun the command below and input the output below to use the various scripts.\nSome scripts require more than one output to run.', font=('Arial',12))
        self.info_frame_description.pack()
        self.info_frame_command_block = Label(self.info_frame, text='GET _cat/shards?s=index,store,node&h=index,store,node,prirep', font=('Arial bold',12), fg='#ffffff', background='#856ff8')
        self.info_frame_command_block.pack()

        self.first_file = CommandInputFrame(self, file1, "First Command Input")
        self.first_file.grid(row=1, column=0, padx=5, pady=5, sticky=NSEW)

        self.second_file = CommandInputFrame(self, file2,"Second Command Input")
        self.second_file.grid(row=2, column=0, padx=5, pady=5, sticky=NSEW)