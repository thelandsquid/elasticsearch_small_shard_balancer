import tkinter as tk
from tkinter import *
from tkinter import ttk

from modes.gui_elements.FileSelector import FileSelector


class CommandInputFrame(tk.Frame):

    def __init__(self,notebook,title="Command Input"):
            super(CommandInputFrame, self).__init__(notebook)
            first_file = ttk.Frame(notebook)

            first_file.grid_rowconfigure(0, weight=1)
            first_file.grid_rowconfigure(1, weight=4)
            first_file.grid_rowconfigure(2, weight=1)
            first_file.grid_columnconfigure(0, weight=1)

            first_file_label = Label(first_file, font=('Arial bold',12), text='First Command Input')
            first_file_label.grid(row=0, column=0, padx=5, pady=5, sticky=W)
            first_file_T = Text(first_file)
            first_file_T.grid(row=1,column=0,padx=5,pady=5,sticky=NSEW)

            first_button_frame = Frame(first_file, bg='red')
            first_button_frame.grid(row=2,column=0,padx=5,pady=5,sticky=NSEW)
            first_button_frame.grid_columnconfigure(0, weight=1)
            first_button_frame.grid_columnconfigure(1, weight=1)

            open_button = ttk.Button(
                first_button_frame,
                text='Open a File',
                command=FileSelector.select_file
            )
            open_button.grid(row=0, column=0, padx=5, pady=5, sticky=W)
            open_button2 = ttk.Button(
                first_button_frame,
                text='Open a File',
                command=FileSelector.select_file
            )
            open_button2.grid(row=0, column=1, padx=5, pady=5, sticky=E)

            return first_file
