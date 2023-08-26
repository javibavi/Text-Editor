from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

# This is the object that will be used to create new tabs in our notebook
class Tab():

    # Notebook takes the notebook that we want to add this tab to
    def __init__(self, notebook):
        
        try:
            # Uses file dialog to find the file that the user wants to open
            self.file_path = filedialog.askopenfilename(
                                            title="Open a File/Create New File",
                                            filetypes=(("text files", "*.txt"),("all files", "*.*")))
            
            # Reads the contents of the file
            self.file_contents = open(self.file_path, 'r')

            # Creates our tab and adds it to the notebook
            self.tab = Frame(notebook)
            notebook.add(self.tab, text=self.file_path)

            # Creates a text box for us to use and inserts the contents of our file into the text box
            self.text_box = Text(self.tab, width=185, height=50)
            self.text_box.insert('1.0',self.file_contents.read())
            self.text_box.place(x=0,y=0)

            # Closes the file
            self.file_contents.close()

        except FileNotFoundError as e:
            messagebox.showerror(title='Error', message=e)
        
    # Function for saving the file 
    def save_file(self):

        # Asks the user where they want to save this file
        file = filedialog.asksaveasfile(title='Save File', defaultextension=".txt",
                                    filetypes=[
                                        ("Text File", "*.txt"),
                                        ("Html File", "*.html"),
                                        ("All Files", "*.*"),
                                    ])
                                    
        
        
        # Saves the text from our text box
        file_text = self.text_box.get('1.0', END)

        # This writes the text from our gui to the file we selected
        file.write(file_text)

        # Closes the file
        file.close()

    # This function is used for shortcuts like cut, copy and paste
    def shortcuts(self, option):
            self.text_box.event_generate(f'<<{option}>>')

