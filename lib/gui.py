import tkinter as tk
from tkinter import filedialog, Menu
import ttkbootstrap as ttk
from PIL import Image, ImageTk
from lib.components.form import NavigationButton
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
p_ICON = '../assets/icon.ico'

def gui_only(func, *args, **kwargs):
    def wrapper(self, *args, **kwargs):
        if IS_PRODUCTION():
            func(self, *args, **kwargs)
    return wrapper

class GUI():
    def __init__(self):
        # Main window
        self.root = ttk.Window(themename=THEME_NAME)
        self.root.title("Fssawin Windows Application - Fssa")

        # set the icon
        self.root.iconbitmap(os.path.join(script_dir, p_ICON))

        # Initialize an attribute to store images
        self.image_references = []

        # Set the window to be square
        self.root.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')
        self.root.resizable(False, False)
        # init pages
        self.current_page = None
        self.pages = {}
        for Page in (StartPage, ManualFormatPage, DataPage,
                     DimensionsPage,FacetPage, FacetVarPage,
                     HypothesisPage,
                     FacetDimPage):
            page_name = Page.__name__
            self.pages[page_name] = Page(self)

        # Load the image and keep a reference in the list to prevent garbage
        # collection
        base_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(base_dir, p_ICON)
        im = Image.open(os.path.abspath(icon_path))
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
        self.menu_bar = Menu(self.root)

        # File Menu
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="New", accelerator="Ctrl+N", )
        self.file_menu.add_command(label="Open...", accelerator="Ctrl+O")
        self.file_menu.add_command(label="Save", accelerator="Ctrl+S", )
        self.file_menu.add_command(label="Save As...")
        self.file_menu.add_separator()  # Adds a separator line between menu
        # items
        self.file_menu.add_command(label="Run")
        self.file_menu.add_command(label="Recent File", state="disabled")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit")
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        #
        self.input_data_menu = Menu(self.menu_bar, tearoff=0)
        self.input_data_radio = tk.StringVar()
        self.input_data_radio.set(1)
        self.input_data_menu.add_radiobutton(label='Recorded Data',
                                             variable=self.input_data_radio,
                                             value=1)
        self.input_data_menu.add_radiobutton(label='Coefficient Matrix',
                                             variable=self.input_data_radio,
                                             value=2)
        self.input_data_menu.add_separator()
        self.input_data_menu.add_command(label="Data")
        self.input_data_menu.add_command(label="Variables")
        self.menu_bar.add_cascade(label="Input Data",
                                  menu=self.input_data_menu)
        # SSA Menu
        self.SSA_menu = Menu(self.menu_bar, tearoff=0)
        self.SSA_menu.add_command(label="Dimensions & Coeffs")
        self.SSA_menu.add_command(label="Technical Options")
        self.menu_bar.add_cascade(label="SSA", menu=self.SSA_menu)
        self.facet_menu = Menu(self.menu_bar, tearoff=0)
        self.facet_menu.add_command(label="Element Labels")
        self.facet_menu.add_command(label="Variable Elements")
        self.facet_menu.add_command(label="Hypotheses")
        self.facet_menu.add_command(label="Diagrams")
        self.menu_bar.add_cascade(label="Facet", menu=self.facet_menu)
        # View Menu
        self.view_menu = Menu(self.menu_bar, tearoff=0)
        self.view_menu.add_command(label="Next")
        self.view_menu.add_command(label="Previous")
        self.view_menu.add_separator()
        self.toolbar_radio = tk.StringVar()
        self.toolbar_radio.set(1)
        self.view_menu.add_radiobutton(label="Toolbar",
                                       variable=self.toolbar_radio,
                                       value=1)
        self.status_bar_radio = tk.StringVar()
        self.status_bar_radio.set(1)
        self.view_menu.add_radiobutton(label="Toolbar",
                                       variable=self.status_bar_radio,
                                       value=1)
        self.view_menu.add_separator()
        self.view_menu.add_command(label="Input File",
                                   state="disabled")
        self.view_menu.add_separator()
        self.view_menu.add_command(label="Output File",
                                   state="disabled")
        self.menu_bar.add_cascade(label="View", menu=self.view_menu)
        #
        self.help_menu = Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label="Contents")
        self.help_menu.add_command(label="Help on current screen")
        self.help_menu.add_command(label="Open Readme.txt")
        self.help_menu.add_separator()
        self.help_menu.add_command(label="About")
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)
        #
        self.root.config(menu=self.menu_bar)

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

    @gui_only
    def show_msg(self,msg, title=None, yes_commend = None,
                 buttons = ['Yes:primary', 'No:secondary']):
        # Handle the error if your data contains non-ASCII characters
        if yes_commend:
            clicked_yes = Messagebox.show_question(msg, title, buttons=[
                buttons[0], buttons[1]])
            if clicked_yes == buttons[0].split(":")[0]:
                yes_commend()
        else:
            Messagebox.show_info(msg, title)

    def save_file(self, file_types=None, default_extension=None,
                  initial_file_name=None, title=None):
        file_name = filedialog.asksaveasfilename(filetypes=file_types,
                                                defaultextension=default_extension,
                                                 title=title,
                                                 confirmoverwrite=True,
                                                 initialfile = initial_file_name)
        return file_name

    def create_navigation(self):
        # Navigation Buttons Frame
        frame_navigation = ttk.Frame(self.root)
        # pack the navigation at the bottom of the screen but above the help
        # bar
        frame_navigation.pack(side=ttk.BOTTOM, fill='x', padx=10,
                              pady=(0, 40))
        center_frame = ttk.Frame(frame_navigation)
        center_frame.pack(pady=5, expand=True)
        self.button_previous = NavigationButton(center_frame, text="Previous",)
        self.button_previous.pack(side=ttk.LEFT, padx=20)
        self.button_next = NavigationButton(center_frame, text="Next",)
        self.button_next.pack(side=ttk.LEFT, padx=20, )
        self.button_run = NavigationButton(center_frame, text="Run",)
        self.button_run.pack(side=ttk.LEFT, padx=20)

    def button_next_config(self, **kwargs):
        self.button_next.config(**kwargs)
        self.view_menu.entryconfig("Next", **kwargs)

    def button_previous_config(self, **kwargs):
        self.button_previous.config(**kwargs)
        self.view_menu.entryconfig("Previous", **kwargs)

    def get_input_file_name(self):
        pass
    def run_button_click(self):
        default_output_file_name = self.get_input_file_name().split(".")[0] + ".fss"
        output_file_path = self.save_file(file_types=[('fss', '*.fss')],
                                              default_extension='.fss',
                                              initial_file_name=default_output_file_name,
                                              title="Save Output File To...")
        return output_file_path




class FFSAPage(ttk.Frame):
    pass

if __name__ == '__main__':
    gui = GUI()
    gui.run_process()
