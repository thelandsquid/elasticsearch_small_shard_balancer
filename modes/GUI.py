import tkinter as tk
from tkinter import *
from tkinter import ttk

from modes.gui_elements.FileSelector import FileSelector
from modes.gui_elements.ScriptFrame import ScriptFrame
from modes.gui_pages.MainMenuPage import MainMenuPage

from scripts.LargestIndices import LargestIndicesScript
from scripts.QuickShardEqualizer import QuickShardEqualizer

class GUI():

    def __init__(self):
        self.GUI()

    def GUI(self):
        self.root = tk.Tk()
        
        self.root.title("Elasticsearch Assistance Scripts")
        
        self.tab_control = ttk.Notebook(self.root)

        self.text_file_1 = StringVar()
        self.text_file_2 = StringVar()
        self.var_dict = {"file1":self.text_file_1,"file2":self.text_file_2}

        self.main_page = MainMenuPage(self.tab_control,self.text_file_1,self.text_file_2)
        self.tab1 = ScriptFrame(self.tab_control, self.var_dict, LargestIndicesScript)
        self.tab2 = ScriptFrame(self.tab_control, self.var_dict, QuickShardEqualizer)
        self.tab_control.pack(expand = 1, fill ="both")
        self.root.geometry("800x1000")
        
        self.root.mainloop()
