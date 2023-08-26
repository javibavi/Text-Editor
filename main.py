# This is going to be a text editor app with all sorts of features

from tkinter import *
from tkinter import ttk
from tabs import *
from tkinter import messagebox
import threading
import time
from os import getcwd

# List to store our tab objects
tab_list = list()

# Variables to be able to keep track of program uptime
second_count = 0
minute_count = 0
hour_count = 0


# This adds a brand new tab object to our list
def create_tab():
    tab_list.append(Tab(tab_holder))

# This function is used to save the file and close the tab
def save():

    try:
        # If the id of the tab is the same as the currently selected tab
        for item in tab_holder.winfo_children():
            if str(item) == (tab_holder.select()):
                # Store the index of the tab
                object_index = tab_holder.index(tab_holder.select())

                # use the index to save the file of the tab and destroy the tab object
                tab_list[object_index].save_file()
                tab_list.remove(tab_list[object_index])

                # Destroys our tab and exits out of the function
                item.destroy() 
                return
    except Exception as e:
        messagebox.showerror(title='Error', message=e)




# These functions use the function 'shortcuts' to automate these shortcuts
def copy():
    try:
        tab_list[tab_holder.index(tab_holder.select())].shortcuts('Copy')
    except Exception:
        pass
def paste():
    try:
        tab_list[tab_holder.index(tab_holder.select())].shortcuts('Paste')
    except Exception:
        pass   
def cut():
    try:
        tab_list[tab_holder.index(tab_holder.select())].shortcuts('Cut')
    except Exception:
        pass

# This function is used to count the uptime and display it in the about section
# It will be handled by a daemon thread
def uptime():

    # This runs while the app is running
    while True:
        # This ensures that we use the global variables we created earlier
        global second_count
        global minute_count
        global hour_count

        # This counts for 1 second and then increases the second count
        time.sleep(1)
        second_count += 1
        # If the second count or minute count reach 60, reset them and increase either the minute or hour count by 1
        if second_count == 60:
            second_count = 0
            minute_count += 1
        if minute_count == 60:
            minute_count = 0
            hour_count += 1

        # This is all within a try statement because if the about screen is not open it throws an error
        try:
            # If the second cout and minute count are both below 10, it adds an extra zero in front of the number
            if second_count < 10 and minute_count < 10:
                about_var.set(f'This is a basic text editor app that allows you to open and edit multiple files in separate tabs\
                            \nUptime: {hour_count}:0{minute_count}:0{second_count}')
                
            # If its just the second count that has this issue, it only adds the extra zero in front of the second count
            elif second_count < 10:
                about_var.set(f'This is a basic text editor app that allows you to open and edit multiple files in separate tabs\
                            \nUptime: {hour_count}:{minute_count}:0{second_count}')
                
            # If its just the minute count that has this issue, it adds a zero in front of the minute count
            elif minute_count < 10:
                about_var.set(f'This is a basic text editor app that allows you to open and edit multiple files in separate tabs\
                            \nUptime: {hour_count}:0{minute_count}:{second_count}')
                
            # Update the screen
            about_message.update_idletasks()
        except Exception:
            pass

def exit_program():
    root.destroy()
        




# These functions display info
def about():

    # This ensures that these two objects will be available globally
    global about_message
    global about_var
    

    
# This creates a separate window that displays info about the app and the uptime of the app
    about_var = StringVar()
    about_message = Toplevel()
    about_message.title('About')
    about_label = Label(about_message, text=f'This is a basic text editor app that allows you to open and edit multiple files in separate tabs\
                            \nUptime: {hour_count}:{minute_count}:{second_count}', textvariable=about_var)
    about_label.pack()
    # These set the new window to be the top window
    about_message.attributes('-topmost', 'true')
    about_message.lift()

    # This piece of code makes it so that focus stays on this window until it is closed
    about_message.grab_set()
    

# Displays a help screen
def help_screen():
    messagebox.showinfo(title='Help', message='You know how to use a text editor')


def main():
    # Creating main window
    global root
    root = Tk()
    root.title("Text Editor")
    # This sets the height and width of the window to the size of the screen
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.geometry(f'{width}x{height}')
    root.iconphoto(True, PhotoImage(file=f'{getcwd()}\\notepad.png'))


    # Creating the root menu bar
    menubar = Menu(root)

    # Adding the menubar to our window
    root.config(menu=menubar)

    # Creating the options file, edit, and help at the top of the screen
    file_menu = Menu(menubar, tearoff=0)
    edit_menu = Menu(menubar, tearoff=0)
    help_menu = Menu(menubar, tearoff=0)

    # Adding the labels to the top of the screen
    menubar.add_cascade(label='File', menu=file_menu)
    menubar.add_cascade(label='Edit', menu=edit_menu)
    menubar.add_cascade(label='Help', menu=help_menu)

    # Creating the options within the file menu
    file_menu.add_command(label='New Tab', command=create_tab)
    file_menu.add_command(label='Save', command=save)
    file_menu.add_separator()
    file_menu.add_command(label='Quit', command=exit_program)

    # Creating the options in the edit menu
    edit_menu.add_command(label='Cut', command=cut)
    edit_menu.add_command(label='Copy', command=copy)
    edit_menu.add_command(label='Paste', command=paste)

    # Creating the options for the help menu
    help_menu.add_command(label='About', command=about)
    help_menu.add_command(label='Help', command=help_screen)


    # Widget to be able to hold multiple files open at one time
    global tab_holder
    tab_holder = ttk.Notebook(root)
    tab_holder.pack(expand=TRUE, fill=BOTH)

    # Daemon thread that counts the uptime of the app in the background
    uptime_thread = threading.Thread(target=uptime, daemon=True)
    uptime_thread.start()


    # looping main window
    root.mainloop()

if __name__ == '__main__':
    main()