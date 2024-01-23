import tkinter as tk
from tkinter import filedialog, Menu
from tkinter.simpledialog import askstring
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview
from PIL import Image, ImageTk
import os

from lib.components.buttons import NavigationButton
from lib.pages import *
from lib.pages.data_page import DataPage
from lib.pages.dimensions_page import DimensionsPage
from lib.pages.facet_dim_page import FacetDimPage
from lib.pages.facet_page import FacetPage
from lib.pages.facet_var_page import FacetVarPage
from lib.pages.hypothesis_page import HypothesisPage
from lib.pages.manual_format_page import ManualFormatPage
from lib.pages.start_page import StartPage
from lib.utils import *
from ttkbootstrap.dialogs.dialogs import Messagebox

THEME_NAME = 'flatly'

# Get the directory of the current script file
script_dir = os.path.dirname(os.path.realpath(__file__))

# Construct the path to the image relative to the script's directory
p_ICON = '../assets/placeholder_icon.gif'

class GUI():
    def __init__(self):
        # Main window
        self.root = ttk.Window(themename=THEME_NAME)
        self.root.title("Fssawin Windows Application - Fssa")

        # Initialize an attribute to store images
        self.image_references = []

        # Set the window to be square
        self.root.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')

        # init pages
        self.current_page = None
        self.pages = {}
        for Page in (StartPage, DataPage, DimensionsPage,
                     FacetPage, ManualFormatPage, FacetVarPage,
                     HypothesisPage, FacetDimPage):
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
        self.create_navigation()

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
        # SSA Menu
        SSA_menu = Menu(menu_bar, tearoff=0)
        SSA_menu.add_command(label="Dimensions & Coeffs")
        SSA_menu.add_command(label="Technical Options")
        menu_bar.add_cascade(label="SSA", menu=SSA_menu)
        facet_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Facet", menu=facet_menu)
        # View Menu
        view_menu = Menu(menu_bar, tearoff=0)
        view_menu.add_command(label="Next")
        view_menu.add_command(label="Previous")
        view_menu.add_separator()
        view_menu.add_command(label="Toolbar")
        view_menu.add_command(label="Status Bar")
        view_menu.add_separator()
        view_menu.add_command(label="Input File")
        view_menu.add_separator()
        view_menu.add_command(label="Output File")
        menu_bar.add_cascade(label="View", menu=view_menu)
        #
        help_menu = Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="Contents")
        help_menu.add_command(label="Help on current screen")
        help_menu.add_command(label="Open Readme.txt")
        help_menu.add_separator()
        help_menu.add_command(label="About")
        menu_bar.add_cascade(label="Help", menu=help_menu)
        #
        self.root.config(menu=menu_bar)

    def show_page(self, page):
        self.current_page = page
        page.pack(fill='both', expand=True)

    def switch_page(self, page_name):
        if self.current_page: self.current_page.pack_forget()
        self.show_page(self.pages[page_name])
        self.current_page = self.pages[page_name]
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

    def create_navigation(self):
        # Navigation Buttons Frame
        frame_navigation = ttk.Frame(self.root)
        # pack the navigation at the bottom of the screen but above the help
        # bar
        frame_navigation.pack(side=ttk.BOTTOM, fill='x', padx=10,
                              pady=(0, 50))
        center_frame = ttk.Frame(frame_navigation)
        center_frame.pack(pady=5, expand=True)
        self.button_previous = NavigationButton(center_frame, text="Previous",)
        self.button_previous.pack(side=ttk.LEFT, padx=20)
        self.button_next = NavigationButton(center_frame, text="Next",)
        self.button_next.pack(side=ttk.LEFT, padx=20, )
        self.button_run = NavigationButton(center_frame, text="Run",)
        self.button_run.pack(side=ttk.LEFT, padx=20)


class FFSAPage(ttk.Frame):
    pass

if __name__ == '__main__':
    gui = GUI()
    gui.run_process()
