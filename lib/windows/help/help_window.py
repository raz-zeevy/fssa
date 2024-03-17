import os
import ttkbootstrap as ttk
import tkinter as tk
from lib.moduls.help_content import *
from lib.components.window import Window
from lib.utils import get_resource
from lib.windows.help.screens import ScreensGenerator

###################################
############ SECTIONS #############
###################################


# Help Contents
s_CONTENTS = 'contents'
s_WHAT_IS_FSSA = 'what_is_fssa'

# menus
s_HELP_MENU = "help_menu"
s_VIEW_MENU = "view_menu"
s_FACETS_MENU = "facets_menu"
s_FILE_MENU = 'file_menu'
s_INPUT_DATA_MENU = "input_data_menu"
s_SSA_menu = "ssa_menu"

# screens
s_VARIABLE_ELEMENTS_FACETS_SCREEN = "variable_elements_in_facets_screen"
s_RECORDED_DATA_SCREEN = "recorded_data_screen"
s_DATA_SCREEN = "data_screen"
s_FACETS_DEFINITION_SCREEN = "facets_definition_screen"
s_VARIABLE_DEFINITION_SCREEN = "variable_definition_screen"
s_FACET_DIAGRAMS_SCREEN = "facet_diagrams_screen"
s_HYPOTHESES_SCREEN = "hypotheses_screen"

###################################
############ COMMANDS #############
###################################

# File menu commands
s_NEW_command = "new_command"
s_OPEN_command = "open_command"
s_SAVE_command = "save_command"
s_SAVE_AS_command = "save_as_command"
s_RUN_command = "run_command"
s_EXIT_command = "exit_command"

# Input data menu commands
s_RECORDED_DATA_command = "recorded_data_command"
s_COEFFICIENT_MATRIX_COMMAND = "coefficient_matrix_command"
s_VARIABLES_COMMAND = "variables_command"
# SSA menu commands
s_TECHNICAL_OPTIONS_COMMAND = "technical_options_command"
s_DIMENSIONS_AND_COEFFS_COMMAND = "dimensions_and_coeffs_command"
# Facet menu commands
s_ELEMENT_LABELS_COMMAND = "element_labels_command"
s_VARIABLE_ELEMENTS_COMMAND = "variable_elements_command"
s_DIAGRAMS_COMMAND = "diagrams_command"
s_HYPOTHESES_COMMAND = "hypotheses_command"
# View menu commands
s_PREVIOUS_COMMAND = "previous_command"
s_NEXT_COMMAND = "next_command"
s_OUTPUT_FILE = "output_file"
s_INPUT_FILE = "input_file"
# help menu commands
s_ABOUT_COMMAND = "about_command"

######### TBD ############

s_COEFFICIENT_MATRIX_SCREEN = None
s_INPUT_FILE_COMMAND = "input_file_command"
s_OUTPUT_FILE_COMMAND = "output_file_command"
s_TECHNICAL_OPTIONS_DIALOG = "technical_options_dialog"

# add to the data screen
# self.add_heading("Selecting and unselecting variables", tag="h2")
# self.add_paragraph("You can select or unselect a variable by hiding "
#                    "or showing the variable column in the main. You "
#                    "can do so by right-clicking on the variable column"
#                    " and selecting 'hide co"

###################################
############ GUI ##################
###################################

SECTION_FUNC_PREFIX = "section_"
LINK_PREFIX = 'clickable_'
TEXT = 'text'
TEXT_SMALL = 'text_small'
H2 = 'h2'
H1 = 'h1'

FONT = "Candara"
h1_font = (FONT, 13, "bold")
h2_font = (FONT, 12, "bold")
text_font = (FONT, 11)
text_small_font = (FONT, 10)
link_font = (FONT, 11, "underline")

TABLE_PRE_PAD = " " * 3


class HelpWindow(Window):
    def __init__(self, parent, section=None, **kwargs):
        """
        graph_data: list of dictionaries containing the data to be plotted
        should contain "x", "y", "annotations", "title", "legend",
         "captions", "geom" keys
        """
        super().__init__(**kwargs, geometry="1240x900")
        self.title("FSSA For Windows Help")
        self.iconbitmap(get_resource("help.ico"))
        # sets the geometry of toplevel
        self.center_window()
        # set the content
        self.col_width = 45
        # History
        self.history = []
        self.history_index = 0
        # init
        self.init_menu()
        self.init_main_frame()
        # Bind key presses to the respective methods
        self.bind("<BackSpace>", lambda x: None)
        self.bind("<Right>", lambda x: self.next_section())
        self.bind("<BackSpace>", lambda x: self.back_section())
        self.bind("<Left>", lambda x: self.back_section())
        self.bind("<Escape>", lambda x: self.exit())
        #
        section = section if section else s_CONTENTS
        self.screen_generator = ScreensGenerator(self)
        self.start_on(section)
        # self.showcase_fonts()

    def center_window(self):
        self.update_idletasks()  # Update "requested size" from geometry manager
        # Calculate x and y coordinates for the Tk root window
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        size = tuple(int(_) for _ in self.geometry().split('+')[0].split('x'))
        x = (screen_width / 2) - (size[0] / 2)
        y = 0
        self.geometry("+%d+%d" % (x, y))

    def start_on(self, section_name):
        self.history.append(section_name)
        self.switch_to_section(section_name)

    def init_main_frame(self):
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        default_bg = self.cget('bg')
        self.text_widget = tk.Text(self.main_frame, bd=0,
                                   wrap='word',
                                   borderwidth=0,
                                   highlightthickness=0, bg=default_bg)
        self.text_widget.pack(expand=True, fill='both')
        self.text_widget.tag_config(H1, font=h1_font)
        self.text_widget.tag_config(TEXT_SMALL, font=text_small_font)
        self.text_widget.tag_config(H2, font=h2_font)
        self.text_widget.tag_config(TEXT, font=text_font)

    def init_menu(self):
        self.menu = tk.Menu(self)
        self.menu.add_command(label="Contents", command=lambda:
        self.process_click(LINK_PREFIX + s_CONTENTS))
        self.menu.add_command(label="Back", command=self.back_section)
        self.menu.add_command(label="Next", command=self.next_section)
        self.menu.add_command(label="Exit", command=self.exit)
        self.config(menu=self.menu)

    def next_section(self):
        if self.history_index == len(self.history) - 1:
            return
        else:
            self.history_index += 1
            self.switch_to_section(self.history[self.history_index])

    def back_section(self):
        if self.history_index == 0:
            return
        else:
            self.history_index -= 1
            self.switch_to_section(self.history[self.history_index])

    #######

    def on_click(self, event):
        # Get the index of the mouse click
        index = self.text_widget.index(f"@{event.x},{event.y}")
        # Check if the click was on a tagged word
        for tag in self.text_widget.tag_names(index):
            if tag.startswith(LINK_PREFIX):
                print(f"You clicked on the entry: {tag}")
                self.process_click(tag)
                break

    def process_click(self, tag):
        # Here you can define what to do for each entry
        dest = tag[len(LINK_PREFIX):]
        # Navigation
        if dest == self.history[self.history_index]: return
        if self.history_index < len(self.history) - 1:
            self.history = self.history[:self.history_index + 1]
        self.history_index += 1
        self.history.append(dest)
        # Switch page
        self.switch_to_section(dest)

    def on_enter(self, event):
        self.text_widget.config(cursor="hand2")

    def on_leave(self, event):
        self.text_widget.config(cursor="")

    def exit(self):
        self.destroy()

    #####################

    def add_link(self, txt, tag):
        self.text_widget.insert('end', txt, f'clickable_{tag}')

    def add_txt(self, txt, tag='text'):
        self.text_widget.insert('end', txt, tag)

    def add_paragraph(self, txt, tag='text'):
        self.text_widget.insert('end', txt + "\n" + "\n", tag)

    def add_heading(self, txt, tag='h1'):
        self.text_widget.insert('end', txt + "\n", tag)

    def add_line_break(self):
        self.text_widget.insert('end', "\n")

    def add_row(self, left, right, left_link=None, offset=0):
        self.add_txt(TABLE_PRE_PAD)
        if left_link:
            self.add_link(left, left_link)
        else:
            self.add_txt(left)
        pad_count = self.col_width - len(left) * 2 - len(TABLE_PRE_PAD) + \
                    offset
        pad = pad_count * " "
        self.add_txt(pad + right + "\n\n")

    def switch_to_section(self, section_name):
        if self.history_index < len(self.history) - 1:
            self.menu.entryconfig("Next", state="normal")
        else:
            self.menu.entryconfig("Next", state="disabled")
        if self.history_index > 0:
            self.menu.entryconfig("Back", state="normal")
        else:
            self.menu.entryconfig("Back", state="disabled")
        print(self.history, self.history_index)
        #
        self.text_widget.config(state='normal')
        self.text_widget.delete('1.0', 'end')
        self.screen_generator.section(section_name)
        self.text_widget.config(state='disabled')
        self.bind_links()

    def bind_links(self):
        for tag in self.text_widget.tag_names():
            if tag.startswith("clickable_"):
                self.text_widget.tag_config(tag, font=link_font)
                self.text_widget.tag_bind(tag, '<Button-1>',
                                          self.on_click)  # Bind left mouse click
                # Bind mouse events to the tag
                self.text_widget.tag_bind(tag, '<Enter>',
                                          self.on_enter)  # Change cursor to hand
                self.text_widget.tag_bind(tag, '<Leave>',
                                          self.on_leave)  # Change cursor back to the

    ##########################
