import tkinter as tk
from tkinter import *
from tkinter import ttk
from modes.gui_elements.CommandInputFrame import CommandInputFrame

from modes.gui_elements.FileSelector import FileSelector


def GUI():
    root = tk.Tk()
    root.title("Tab Widget")
    tabControl = ttk.Notebook(root)

    main_page(tabControl)
    tabControl.pack(expand = 1, fill ="both")
    
    
    root.mainloop()

def main_page(notebook):
       
    tab = ttk.Frame(notebook)

    notebook.add(tab, text='Main Menu')

    tab.grid_rowconfigure(0, weight=1)
    tab.grid_rowconfigure(1, weight=1)
    tab.grid_rowconfigure(2, weight=1)
    tab.grid_columnconfigure(0, weight=1)

    info_frame = Frame(tab)
    info_frame.grid(row=0, column=0, padx=5, pady=15, sticky=NSEW)
    info_frame_title = Label(info_frame, text='Elasticsearch Assistance Scripts', font=('Arial',30))
    info_frame_title.pack()
    info_frame_description = Label(info_frame, text='A program to help diagnose issues and gather information about Elasticesarch clusters.\nRun the command below and input the output below to use the various scripts.\nSome scripts require more than one output to run.', font=('Arial',12))
    info_frame_description.pack()
    info_frame_command_block = Label(info_frame, text='GET _cat/shards?s=index,store,node&h=index,store,node,prirep', font=('Arial bold',12), fg='#ffffff', background='#856ff8')
    info_frame_command_block.pack()

    first_file = CommandInputFrame.get(tab)
    first_file.grid(row=1, column=0, padx=5, pady=5, sticky=NSEW)






    second_file = Frame(tab)
    second_file.grid(row=2, column=0, padx=5, pady=5, sticky=NSEW)

    second_file.grid_rowconfigure(0, weight=1)
    second_file.grid_rowconfigure(1, weight=4)
    second_file.grid_rowconfigure(2, weight=1)
    second_file.grid_columnconfigure(0, weight=1)

    second_file_label = Label(second_file, font=('Arial bold',12), text='Second Command Input')
    second_file_label.grid(row=0, column=0, padx=5, pady=5, sticky=W)
    second_file_T = Text(second_file)
    second_file_T.grid(row=1,column=0,padx=5,pady=5,sticky=NSEW)