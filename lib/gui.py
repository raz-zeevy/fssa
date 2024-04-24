import ctypes
import os.path
import sys
import tkinter as tk
from lib.windows.help.help_window import HelpWindow
from tkinter import filedialog, Menu
import ttkbootstrap as ttk
from lib.components.form import NavigationButton
from lib.pages.data_page import DataPage
from lib.windows.diagram_window import DiagramWindow
from lib.windows.recode_window import RecodeWindow
from lib.pages.dimensions_page import DimensionsPage
from lib.pages.facet_dim_page import FacetDimPage
from lib.pages.facet_page import FacetPage
from lib.pages.facet_var_page import FacetVarPage
from lib.pages.hypothesis_page import HypothesisPage
from lib.pages.manual_format_page import ManualFormatPage
from lib.pages.input_page import InputPage
from lib.pages.matrix_input_page import MatrixInputPage
from lib.pages.start_page import StartPage
from lib.utils import *
from ttkbootstrap.dialogs.dialogs import Messagebox
from lib.windows.technical_options_window import TOWindow

THEME_NAME = 'sandstone'
p_ICON = 'icon.ico'


def gui_only(func, *args, **kwargs):
    def wrapper(self, *args, **kwargs):
        if IS_PRODUCTION():
            return func(self, *args, **kwargs)

    return wrapper


class GUI():
    def __init__(self):
        #
        # if 'win' in sys.platform:
        # ctypes.windll.shcore.SetProcessDpiAwareness(0)
        # ctypes.windll.user32.SetProcessDPI    Aware()
        # os.system("xrandr  | grep \* | cut -d' ' -f4")
        # Main window
        self.root = ttk.Window(themename=THEME_NAME)
        self.root.title("FSSAWIN - Faceted Smallest Space Analysis for "
                        "Windows")
        # set the icon
        self.root.iconbitmap(get_resource(p_ICON))

        # # Initialize an attribute to store images
        self.image_references = {}
        #
        # # load all png files from ./assets/toolbar to image_references
        # for file in os.listdir(get_path("assets/toolbar")):
        #     if file.endswith(".png"):
        #         self.image_references.append(get_resource(f"toolbar/{file}"))

        # Set the window to be square
        self.config_dpi_ratio()
        # WINDOW_HEIGHT = 570
        # WINDOW_HEIGHT = 800
        # WINDOW_WIDTH = 660
        # dpi+++ -> widht ++
        # dpi+++ -> height ++
        self.root.minsize(*real_size((WINDOW_WIDTH, WINDOW_HEIGHT),
                                    _round = True))
        self.root.pack_propagate(0)
        self.root.resizable(False, False)
        # set the window to be always on top
        # self.root.attributes("-topmost", True)

        # init pages
        self.current_page = None
        self.pages = {}
        for Page in (StartPage, InputPage, MatrixInputPage, ManualFormatPage,
                     DataPage,
                     DimensionsPage, FacetPage, FacetVarPage,
                     HypothesisPage,
                     FacetDimPage,):
            page_name = Page.__name__
            self.pages[page_name] = Page(self)

        # init common gui
        # self.center_window()

    ##################
    #   Functions    #
    ##################

    def config_dpi_ratio(self):
        dpi = self.root.winfo_fpixels("1i")
        dpi_ratio = dpi / 96
        os.environ["DPI_RATIO"] = str(dpi_ratio)

    def start_fss(self):
        # self.root.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')
        self.create_menu()
        self.create_icon_menu()
        self.create_help_bar()
        self.create_navigation()

    def run_process(self):
        self.root.mainloop()

    ##################
    # Initialization #
    ##################

    def center_window(self):
        self.root.update_idletasks()  # Update "requested size" from geometry
        # manager
        # Calculate x and y coordinates for the Tk root window
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        size = tuple(int(_) for _ in self.root.geometry().split('+')[0].split(
            'x'))
        x = (screen_width / 2) - (size[0] / 2)
        y = (screen_height / 2) - (size[1] / 2) - (screen_height / 10)
        self.root.geometry("+%d+%d" % (x, y))

    def create_help_bar(self):
        # Status Bar
        status_bar = ttk.Label(self.root, text="For Help, press F1",
                               relief=ttk.SUNKEN, anchor='w',
                               background='#F0F0F0')
        # pack the status bar at the bottom of the screen
        status_bar.pack(side=ttk.BOTTOM, fill='x')

    def create_icon_menu(self):
        def load_icon_images():
            icons_dir = get_path("lib/assets/toolbar")
            # load all png files from ./assets/toolbar to image_references
            sizes_dict = {'go.png' : real_size((21, 21),_round=True),
                          'help.png' : real_size((20,20),_round=True),
                          'new.png' : real_size((19,19),_round=True),
                          'open.png' : real_size((20,20),_round=True),
                          'save.jpg' : real_size((23,23),_round=True),
                          'next.jpg' : real_size((23,18),_round=True),
                          'prev.jpg' : real_size((23,18),_round=True)}
            for file in os.listdir(get_path(icons_dir)):
                if file.endswith(".png") or file.endswith(".gif") or \
                        file.endswith('.jpg'):
                    image_path = os.path.join(icons_dir, file)
                    size = sizes_dict.get(file, real_size((25, 25),_round=True))
                    image = Image.open(image_path, "r").resize(size)
                    self.image_references[file] = ImageTk.PhotoImage(image)

        def add_button(image: str, **kwargs):
            if not "width" in kwargs:
                kwargs["width"] = real_size(25)
            if not "height" in kwargs:
                kwargs["height"] = real_size(25)
            button = tk.Button(icon_menu_frame,
                               autostyle=False,
                               image=self.image_references[image],
                               bg='white', relief='raised',
                               borderwidth=1, **kwargs)
            button.pack(side=ttk.LEFT)
            return button

        # Icon Menu
        from PIL import Image, ImageTk
        icon_menu_frame = tk.Frame(self.root,
                                   autostyle=False,
                                   pady=3, padx=5)
        icon_menu_frame.pack(side=ttk.TOP, fill='x')
        load_icon_images()
        self.m_button_new = add_button("new.png")
        self.m_button_open = add_button("open.png")
        self.m_button_save = add_button("save.jpg")
        tk.Frame(icon_menu_frame, width=10).pack(side=ttk.LEFT)
        ###
        self.m_button_prev = add_button("prev.jpg")
        self.m_button_next = add_button("next.jpg")
        tk.Frame(icon_menu_frame, width=10).pack(side=ttk.LEFT)
        ###
        self.m_button_run = add_button("go.png")
        self.m_button_help = add_button("help.png")
        icon_menu_border = tk.Frame(self.root,
                                    autostyle=False,
                                    borderwidth=1, relief='flat',
                                    background='grey', pady=0)
        icon_menu_border.pack(side=ttk.TOP, fill='x')

        # tk.Label(icon_menu_border, text="asd").pack()

    def create_navigation(self):
        # Navigation Buttons Frame
        frame_navigation = ttk.Frame(self.root)
        # pack the navigation at the bottom of the screen but above the help
        # bar
        frame_navigation.pack(side=ttk.BOTTOM, fill='x', padx=10,
                              pady=(0, 20))
        center_frame = ttk.Frame(frame_navigation)
        center_frame.pack(pady=5, expand=True)
        self.button_previous = NavigationButton(center_frame,
                                                text="Previous", )
        self.button_previous.pack(side=ttk.LEFT, padx=20)
        self.button_next = NavigationButton(center_frame, text="Next", )
        self.button_next.pack(side=ttk.LEFT, padx=20, )
        self.button_run = NavigationButton(center_frame, text="Run", )
        self.button_run.pack(side=ttk.LEFT, padx=20)

    ##################
    #      Menu      #
    ##################

    def create_menu(self):
        # Menu
        self.menu_bar = Menu(self.root)
        # File Menu
        self.file_menu = Menu(self.menu_bar, background='lightblue')
        self.file_menu.add_command(label="New", accelerator="Ctrl+N")
        self.file_menu.add_command(label="Open", accelerator="Ctrl+O")
        self.file_menu.add_command(label="Save",  accelerator="Ctrl+S")
        self.file_menu.add_command(label="Save As...")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Run")
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
        self.input_data_menu.add_command(label="Variables")
        self.menu_bar.add_cascade(label="Active Data",
                                  menu=self.input_data_menu)
        # SSA Menu
        self.FSSA_menu = Menu(self.menu_bar, tearoff=0)
        self.FSSA_menu.add_command(label="Dimensions & Coeffs")
        self.FSSA_menu.add_command(label="Technical Options")
        self.menu_bar.add_cascade(label="FSSA", menu=self.FSSA_menu)
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
        self.view_menu.add_command(label="Input File",
                                   state="disabled")
        self.view_menu.add_separator()
        self.view_menu.add_command(label="Output File",
                                   state="disabled")
        self.diagram_2d_menu = Menu(self.view_menu, tearoff=0)
        self.diagram_2d_menu.add_command(label="No Facet")
        self.diagram_2d_menu.add_command(label="Facet A",
                                         state="disabled")
        self.diagram_2d_menu.add_command(label="Facet B",
                                         state="disabled")
        self.diagram_2d_menu.add_command(label="Facet C",
                                         state="disabled")
        self.diagram_2d_menu.add_command(label="Facet D",
                                         state="disabled")
        self.view_menu.add_cascade(label="2D Diagram ",
                                   menu=self.diagram_2d_menu,
                                   state="disabled")
        self.diagram_3d_menu = Menu(self.view_menu, tearoff=0)
        self.diagram_3d_menu.add_command(label="No Facet")
        self.diagram_3d_menu.add_command(label="Facet A",
                                         state="disabled")
        self.diagram_3d_menu.add_command(label="Facet B",
                                         state="disabled")
        self.diagram_3d_menu.add_command(label="Facet C",
                                         state="disabled")
        self.diagram_3d_menu.add_command(label="Facet D"
                                         , state="disabled")
        self.view_menu.add_cascade(label="3D Diagram ",
                                   menu=self.diagram_3d_menu,
                                   state="disabled")
        self.menu_bar.add_cascade(label="View", menu=self.view_menu)
        #
        self.help_menu = Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label="Contents")
        self.help_menu.add_command(label="Help on current screen",
                                   accelerator="F1")
        self.help_menu.add_command(label="Open Readme.txt")
        self.help_menu.add_separator()
        self.help_menu.add_command(label="About")
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)
        #
        self.root.config(menu=self.menu_bar)

    def set_menu_recorded_data(self):
        self.input_data_radio.set(1)
        self.input_data_menu.entryconfig("Recorded Data", state="disabled")
        self.input_data_menu.entryconfig("Coefficient Matrix",
                                         state="normal")
        self.input_data_menu.entryconfig("Variables", state="disabled")
        try:
            self.input_data_menu.index("Data")
        except tk.TclError:
            self.input_data_menu.insert_command(3, label="Data")
        self.input_data_menu.entryconfig("Data", state="disabled")

    def set_menu_matrix_data(self):
        self.input_data_radio.set(2)
        self.input_data_menu.entryconfig("Recorded Data", state="normal")
        self.input_data_menu.entryconfig("Coefficient Matrix",
                                         state="disabled")
        # delete the entry data from the input data menu
        try:
            self.input_data_menu.index("Data")
            self.input_data_menu.delete(3)
        except tk.TclError: pass
        self.input_data_menu.entryconfig("Variables", state="disabled")

    ##################
    #   Navigation   #
    ##################

    def show_page(self, page):
        self.current_page = page
        page.pack(fill='both', expand=True)

    def switch_page(self, page_name):
        if self.current_page: self.current_page.pack_forget()
        self.show_page(self.pages[page_name])
        self.current_page = self.pages[page_name]

    def option_next_config(self, **kwargs):
        self.button_next.config(**kwargs)
        self.view_menu.entryconfig("Next", **kwargs)
        self.m_button_next.config(**kwargs)

    def option_previous_config(self, **kwargs):
        self.button_previous.config(**kwargs)
        self.view_menu.entryconfig("Previous", **kwargs)
        self.m_button_prev.config(**kwargs)

    def option_run_config(self, **kwargs):
        self.button_run.config(**kwargs)
        self.file_menu.entryconfig("Run", **kwargs)
        self.m_button_run.config(**kwargs)

    #########################
    # Dialogues and Windows #
    #########################

    def show_diagram_window(self, graph_data_lst):
        self.diagram_window = DiagramWindow(self, graph_data_lst)
        self.diagram_window.bind("<F1>", lambda x: self.show_help_windw())

    def show_help_windw(self, section=None):
        self.help_window = HelpWindow(self, section)

    def show_recode_window(self):
        self.recode_window = RecodeWindow(self)
        recode_func = self.pages[DATA_PAGE_NAME].recode_variables
        self.recode_window.button_recode.config(command=lambda:
        recode_func(self.recode_window))
        self.recode_window.bind("<F1>", lambda x: self.show_help_windw())

    def show_technical_options_window(self, locality_list: list):
        self.technical_options = TOWindow(self, locality_list)

    def show_error(self, title, msg):
        # Handle the error if your data contains non-ASCII characters
        Messagebox.show_error(msg, title=title)
        # You might want to inform the user with a message box
        # messagebox.showerror("Save Error", "The file contains non-ASCII characters.")

    def show_warning(self, title, msg):
        # Handle the error if your data contains non-ASCII characters
        Messagebox.show_warning(msg, title=title)
        # You might want to inform the user with a message box
        # messagebox.showerror("Save Error", "The file contains non-ASCII characters.")

    @gui_only
    def show_msg(self, msg, title=None, yes_command=None,
                 no_command=None,
                 buttons=['Yes:primary', 'No:secondary']):
        if yes_command:
            clicked_yes = Messagebox.show_question(msg, title, buttons=[
                buttons[0], buttons[1]])
            if clicked_yes == buttons[0].split(":")[0]:
                yes_command()
            elif no_command:
                no_command()
            return clicked_yes
        else:
            Messagebox.show_info(msg, title)
    def save_file_diaglogue(self, file_types=None, default_extension=None,
                            initial_file_name=None, title=None):
        file_name = filedialog.asksaveasfilename(filetypes=file_types,
                                                 defaultextension=default_extension,
                                                 title=title,
                                                 confirmoverwrite=True,
                                                 initialfile=initial_file_name)
        return file_name

    def get_input_file_name(self) -> str:
        """
        Placeholder for the controller-planted method that returns the input
        file name
        :return:
        """
        pass

    def run_button_dialogue(self):
        default_output_file_name = self.get_input_file_name().split(".")[
                                       0] + ".fss"
        output_file_path = self.save_file_diaglogue(
            file_types=[('fss', '*.fss')],
            default_extension='.fss',
            initial_file_name=default_output_file_name,
            title="Save Output File To...")
        return output_file_path

    def save_session_dialogue(self):
        file_name = filedialog.asksaveasfilename(filetypes=[('mem', '*.mem')],
                                                 defaultextension='.mem',
                                                 title="Save FSSA Session",
                                                 confirmoverwrite=True)
        return file_name

    def open_session_dialogue(self):
        file_name = filedialog.askopenfilename(filetypes=[('mem', '*.mem')],
                                               title="Open FSSA Session")
        return file_name


if __name__ == '__main__':
    gui = GUI()
    # gui.show_technical_options_window()
    # gui.show_help_windw()
    # Create the main window
    gui.run_process()
    gui.start_fss()
