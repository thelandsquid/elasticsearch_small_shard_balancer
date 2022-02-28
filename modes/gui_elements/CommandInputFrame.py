import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import *

from modes.gui_elements.FileSelector import FileSelector


class CommandInputFrame(tk.Frame):

    def __init__(self,notebook,file,title="Command Input"):
        super(CommandInputFrame, self).__init__(notebook)
        self.file=file

        self.grid_rowconfigure(0, weight=2)
        self.grid_rowconfigure(1, weight=5)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.self_label = Label(self, font=('Arial bold',12), text=title)
        self.self_label.grid(row=0, column=0, padx=5, pady=5, sticky=SW)
        self.self_T = ScrolledText(self, height=4)
        self.self_T.grid(row=1,column=0,padx=5,pady=5,sticky=NSEW)

        self.button_frame = Frame(self, borderwidth=1, relief=RIDGE)
        self.button_frame.grid(row=2,column=0,padx=5,pady=5,sticky=NSEW)
        self.button_frame.grid_rowconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(1, weight=1)
        self.button_frame.grid_columnconfigure(2, weight=1)

        self.open_button = ttk.Button(
            self.button_frame,
            text='Open a File',
            command=self.select_file
        )
        self.open_button.grid(row=0, column=0, padx=5, pady=5, sticky=NSEW)

        self.console_label = Label(self.button_frame, font=('Arial',12), bg=self.button_frame['bg'])
        self.console_label.grid(row=0, column=1, padx=5, pady=5)

        self.save_text = ttk.Button(
            self.button_frame,
            text='Save Text',
            command=self.set_value
        )
        self.save_text.grid(row=0, column=2, padx=5, pady=5, sticky=NSEW)

    def select_file(self):
        from tkinter import filedialog as fd
        from tkinter.messagebox import showinfo
        import os

        filetypes = (
            ('text files', '*.txt'),
            ('All files', '*.*')
        )

        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)
        
        if os.path.isfile(filename):
            text_file = open(filename, "r")
            data = text_file.read()
            text_file.close()

        if not data:
            self.set_console_label('Error reading input file')
        else:
            import re
            data = re.sub('[ \t]+', ' ', data)
            self.self_T.delete("1.0", END)
            self.self_T.insert(END,data)
            self.file.set(self.self_T.get("1.0", END))
            self.set_console_label()
        

    def set_value(self):
        import re
        data = re.sub('[ \t]+', ' ', self.self_T.get("1.0", END))
        self.self_T.delete("1.0", END)
        self.self_T.insert(END,data)
        self.file.set(data)
        self.set_console_label()
            
    
    def set_console_label(self,msg='Command value set!'):
        self.console_label.config(text = msg)
        self.after(5000, self.remove_console_label)
    
    def remove_console_label(self):
        self.console_label.config(text='')