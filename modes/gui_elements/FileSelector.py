
class FileSelector:

    @classmethod
    def select_file(cls):
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