import tkinter as tk
from tkinter import *
from tkinter import ttk


def GUI():
    root = tk.Tk()
    root.title("Tab Widget")
    tabControl = ttk.Notebook(root)

    tab1 = ttk.Frame(tabControl)
    tab2 = ttk.Frame(tabControl)

    tabControl.add(tab1, text ='Tab 1')
    tabControl.add(tab2, text ='Tab 2')
    main_page(tabControl)
    tabControl.pack(expand = 1, fill ="both")
    
    ttk.Label(tab1, 
            text ="Welcome to \
            GeeksForGeeks").grid(column = 0, 
                                row = 0,
                                padx = 30,
                                pady = 30)  
    ttk.Label(tab2,
            text ="Lets dive into the\
            world of computers").grid(column = 0,
                                        row = 0, 
                                        padx = 30,
                                        pady = 30)
    
    root.mainloop()

def main_page(notebook):
       
    tab = ttk.Frame(notebook)

    notebook.add(tab, text='User Input')
    # open_button = ttk.Button(
    #     tab,
    #     text='Open a File',
    #     command=select_file
    # )
    # open_button.pack()

    tab.grid_rowconfigure(0, weight=1)
    tab.grid_rowconfigure(1, weight=1)
    tab.grid_columnconfigure(0, weight=1)

    first_file = Frame(tab, background='yellow')
    first_file.grid(row=0, column=0, padx=5, pady=5, sticky=NSEW)
    first_file_label = Label(first_file, text='First Command Input')
    first_file_label.pack()

    second_file = Frame(tab, background='red')
    second_file.grid(row=1, column=0, padx=5, pady=5, sticky=NSEW)
    second_file_label = Label(second_file, text='First Command Input')
    second_file_label.pack()



def select_file():
    from tkinter import filedialog as fd
    from tkinter.messagebox import showinfo

    filetypes = (
        ('text files', '*.txt'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)
    
    return filename

def script_tab(notebook):
    tab = ttk.Frame(notebook)

