import tkinter as tk
from tkinter import filedialog, Menu
from tkinter.simpledialog import askstring
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview
from PIL import Image, ImageTk
import os
from lib.pages.start_page import StartPage
from lib.pages.data_page import DataPage
from lib.pages.dimensions_page import DimensionsPage
from lib.pages.facet_page import FacetPage
from lib.utils import *
from ttkbootstrap.dialogs.dialogs import Messagebox

THEMENAME = 'flatly'


# Get the directory of the current script file
script_dir = os.path.dirname(os.path.realpath(__file__))

# Construct the path to the image relative to the script's directory
p_ICON = 'assets/placeholder_icon.gif'

class GUI():
    def __init__(self):
        # Main window
        self.root = ttk.Window(themename=THEMENAME)
        self.root.title("Fssawin Windows Application - Fssa")

        # Initialize an attribute to store images
        self.image_references = []

        # Set the window to be square
        self.root.geometry(f'{WINDOW_WIDTH}x{WINDOW_HIGHT}')

        # init pages
        self.current_page = None
        self.pages = {}
        for Page in (StartPage, DataPage, DimensionsPage,
                     FacetPage):
            page_name = Page.__name__
            self.pages[page_name] = Page(self)

        # Load the image and keep a reference in the list to prevent garbage
        # collection
        im = Image.open(p_ICON)
        ph = ImageTk.PhotoImage(im)
        self.image_references.append(ph)  # Storing the reference to the

        # init common gui
        self.create_menu()
        self.create_help_bar()

    def create_help_bar(self):
        # Status Bar
        status_bar = ttk.Label(self.root, text="For Help, press F1",
                               relief=ttk.SUNKEN, anchor='w')
        # pack the status bar at the bottom of the screen
        status_bar.pack(side=ttk.BOTTOM, fill='x')

    def create_menu(self):
        # Menu
        menu_bar = Menu(self.root)

        # File Menu
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New", accelerator="Ctrl+N", )
        file_menu.add_command(label="Open...", accelerator="Ctrl+O")
        file_menu.add_command(label="Save", accelerator="Ctrl+S", )
        file_menu.add_command(label="Save As...")
        file_menu.add_separator()  # Adds a separator line between menu items
        file_menu.add_command(label="Run")
        file_menu.add_command(label="Recent File", state="disabled")
        file_menu.add_separator()
        file_menu.add_command(label="Exit")
        menu_bar.add_cascade(label="File", menu=file_menu)
        #
        input_data_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Input Data", menu=input_data_menu)
        SSA_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="SSA", menu=SSA_menu)
        facet_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Facet", menu=facet_menu)
        # View Menu
        view_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="View", menu=view_menu)
        help_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        self.root.config(menu=menu_bar)

    def show_page(self, page):
        self.current_page = page
        page.pack(fill='both', expand=True)

    def switch_page(self, page_name):
        if self.current_page: self.current_page.pack_forget()
        self.show_page(self.pages[page_name])

    def run_process(self):
        self.root.mainloop()

    def show_error(self, title, msg):
        # Handle the error if your data contains non-ASCII characters
        Messagebox.show_error(msg, title=title)
        # You might want to inform the user with a message box
        # messagebox.showerror("Save Error", "The file contains non-ASCII characters.")

    def save_file(self, file_types=None, default_extension=None,):
        file_name = filedialog.asksaveasfilename(filetypes=file_types,
                                                 defaultextension=default_extension,)
        return file_name

class FFSAPage(ttk.Frame):
    pass

if __name__ == '__main__':
    gui = GUI()
    gui.run_process()
