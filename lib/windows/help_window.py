import os
import ttkbootstrap as ttk
import tkinter as tk
from tkhtmlview import *
from lib.moduls.help_content import *
from lib.components.window import Window
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
s_VARIABLE_DEFINITION = "variable_definition"
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
s_VARIABLES_SCREEN = None
s_DIMENSIONS_AND_COEFFS_SCREEN = "dimensions_and_coefficients_screen"
s_TECHNICAL_OPTIONS_DIALOG = "technical_options_dialog"

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
h2_font = (FONT, 13, "bold")
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
        self.iconbitmap(os.path.abspath("../assets/help.ico"))
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
        self.process_click(LINK_PREFIX+s_CONTENTS))
        self.menu.add_command(label="Back", command=self.back_section)
        self.menu.add_command(label="Next", command=self.next_section)
        self.menu.add_command(label="Exit", command=self.exit)
        self.config(menu=self.menu)

    def showcase_fonts(self):
        fonts = """System
Terminal
Fixedsys
Modern
Roman
Script
Courier
MS Serif
MS Sans Serif
Small Fonts
Bell Gothic Std Black
Bell Gothic Std Light
Eccentric Std
Stencil Std
Tekton Pro
Tekton Pro Cond
Tekton Pro Ext
Trajan Pro
Rosewood Std Regular
Prestige Elite Std
Poplar Std
Orator Std
OCR A Std
Nueva Std Cond
Minion Pro SmBd
Minion Pro Med
Minion Pro Cond
Mesquite Std
Lithos Pro Regular
Kozuka Mincho Pro R
@Kozuka Mincho Pro R
Kozuka Mincho Pro M
@Kozuka Mincho Pro M
Kozuka Mincho Pro L
@Kozuka Mincho Pro L
Kozuka Mincho Pro H
@Kozuka Mincho Pro H
Kozuka Mincho Pro EL
@Kozuka Mincho Pro EL
Kozuka Mincho Pro B
@Kozuka Mincho Pro B
Kozuka Gothic Pro R
@Kozuka Gothic Pro R
Kozuka Gothic Pro M
@Kozuka Gothic Pro M
Kozuka Gothic Pro L
@Kozuka Gothic Pro L
Kozuka Gothic Pro H
@Kozuka Gothic Pro H
Kozuka Gothic Pro EL
@Kozuka Gothic Pro EL
Kozuka Gothic Pro B
@Kozuka Gothic Pro B
Hobo Std
Giddyup Std
Cooper Std Black
Charlemagne Std
Chaparral Pro
Brush Script Std
Blackoak Std
Birch Std
Adobe Garamond Pro
Adobe Garamond Pro Bold
Adobe Kaiti Std R
@Adobe Kaiti Std R
Adobe Heiti Std R
@Adobe Heiti Std R
Adobe Fangsong Std R
@Adobe Fangsong Std R
Adobe Caslon Pro
Adobe Caslon Pro Bold
Adobe Arabic
Adobe Devanagari
Adobe Hebrew
Adobe Ming Std L
@Adobe Ming Std L
Adobe Myungjo Std M
@Adobe Myungjo Std M
Adobe Song Std L
@Adobe Song Std L
Kozuka Gothic Pr6N B
@Kozuka Gothic Pr6N B
Kozuka Gothic Pr6N EL
@Kozuka Gothic Pr6N EL
Kozuka Gothic Pr6N H
@Kozuka Gothic Pr6N H
Kozuka Gothic Pr6N L
@Kozuka Gothic Pr6N L
Kozuka Gothic Pr6N M
@Kozuka Gothic Pr6N M
Kozuka Gothic Pr6N R
@Kozuka Gothic Pr6N R
Kozuka Mincho Pr6N B
@Kozuka Mincho Pr6N B
Kozuka Mincho Pr6N EL
@Kozuka Mincho Pr6N EL
Kozuka Mincho Pr6N H
@Kozuka Mincho Pr6N H
Kozuka Mincho Pr6N L
@Kozuka Mincho Pr6N L
Kozuka Mincho Pr6N M
@Kozuka Mincho Pr6N M
Kozuka Mincho Pr6N R
@Kozuka Mincho Pr6N R
Letter Gothic Std
Minion Pro
Myriad Hebrew
Myriad Pro
Myriad Pro Cond
Myriad Pro Light
Rosewood Std Fill
Marlett
Arial
Arabic Transparent
Arial Baltic
Arial CE
Arial CYR
Arial Greek
Arial TUR
Batang
@Batang
BatangChe
@BatangChe
Gungsuh
@Gungsuh
GungsuhChe
@GungsuhChe
Courier New
Courier New Baltic
Courier New CE
Courier New CYR
Courier New Greek
Courier New TUR
DaunPenh
DokChampa
Estrangelo Edessa
Euphemia
Gautami
Vani
Gulim
@Gulim
GulimChe
@GulimChe
Dotum
@Dotum
DotumChe
@DotumChe
Impact
Iskoola Pota
Kalinga
Kartika
Khmer UI
Lao UI
Latha
Lucida Console
Malgun Gothic
@Malgun Gothic
Mangal
Meiryo
@Meiryo
Meiryo UI
@Meiryo UI
Microsoft Himalaya
Microsoft JhengHei
@Microsoft JhengHei
Microsoft YaHei
@Microsoft YaHei
MingLiU
@MingLiU
PMingLiU
@PMingLiU
MingLiU_HKSCS
@MingLiU_HKSCS
MingLiU-ExtB
@MingLiU-ExtB
PMingLiU-ExtB
@PMingLiU-ExtB
MingLiU_HKSCS-ExtB
@MingLiU_HKSCS-ExtB
Mongolian Baiti
MS Gothic
@MS Gothic
MS PGothic
@MS PGothic
MS UI Gothic
@MS UI Gothic
MS Mincho
@MS Mincho
MS PMincho
@MS PMincho
MV Boli
Microsoft New Tai Lue
Nyala
Microsoft PhagsPa
Plantagenet Cherokee
Raavi
Segoe Script
Segoe UI
Segoe UI Semibold
Segoe UI Light
Segoe UI Symbol
Shruti
SimSun
@SimSun
NSimSun
@NSimSun
SimSun-ExtB
@SimSun-ExtB
Sylfaen
Microsoft Tai Le
Times New Roman
Times New Roman Baltic
Times New Roman CE
Times New Roman CYR
Times New Roman Greek
Times New Roman TUR
Tunga
Vrinda
Shonar Bangla
Microsoft Yi Baiti
Tahoma
Microsoft Sans Serif
Angsana New
Aparajita
Cordia New
Ebrima
Gisha
Kokila
Leelawadee
Microsoft Uighur
MoolBoran
Symbol
Utsaah
Vijaya
Wingdings
Andalus
Arabic Typesetting
Simplified Arabic
Simplified Arabic Fixed
Sakkal Majalla
Traditional Arabic
Aharoni
David
FrankRuehl
Levenim MT
Miriam
Miriam Fixed
Narkisim
Rod
FangSong
@FangSong
SimHei
@SimHei
KaiTi
@KaiTi
AngsanaUPC
Browallia New
BrowalliaUPC
CordiaUPC
DilleniaUPC
EucrosiaUPC
FreesiaUPC
IrisUPC
JasmineUPC
KodchiangUPC
LilyUPC
DFKai-SB
@DFKai-SB
Lucida Sans Unicode
Arial Black
Calibri
Cambria
Cambria Math
Candara
Comic Sans MS
Consolas
Constantia
Corbel
Franklin Gothic Medium
Gabriola
Georgia
Palatino Linotype
Segoe Print
Trebuchet MS
Verdana
Webdings
Haettenschweiler
MS Outlook
Book Antiqua
Century Gothic
Bookshelf Symbol 7
MS Reference Sans Serif
MS Reference Specialty
Bradley Hand ITC
Freestyle Script
French Script MT
Juice ITC
Kristen ITC
Lucida Handwriting
Mistral
Papyrus
Pristina
Tempus Sans ITC
Garamond
Monotype Corsiva
Agency FB
Arial Rounded MT Bold
Blackadder ITC
Bodoni MT
Bodoni MT Black
Bodoni MT Condensed
Bookman Old Style
Calisto MT
Castellar
Century Schoolbook
Copperplate Gothic Bold
Copperplate Gothic Light
Curlz MT
Edwardian Script ITC
Elephant
Engravers MT
Eras Bold ITC
Eras Demi ITC
Eras Light ITC
Eras Medium ITC
Felix Titling
Forte
Franklin Gothic Book
Franklin Gothic Demi
Franklin Gothic Demi Cond
Franklin Gothic Heavy
Franklin Gothic Medium Cond
Gigi
Gill Sans MT
Gill Sans MT Condensed
Gill Sans Ultra Bold
Gill Sans Ultra Bold Condensed
Gill Sans MT Ext Condensed Bold
Gloucester MT Extra Condensed
Goudy Old Style
Goudy Stout
Imprint MT Shadow
Lucida Sans
Lucida Sans Typewriter
Maiandra GD
OCR A Extended
Palace Script MT
Perpetua
Perpetua Titling MT
Rage Italic
Rockwell
Rockwell Condensed
Rockwell Extra Bold
Script MT Bold
Tw Cen MT
Tw Cen MT Condensed
Tw Cen MT Condensed Extra Bold
Algerian
Baskerville Old Face
Bauhaus 93
Bell MT
Berlin Sans FB
Berlin Sans FB Demi
Bernard MT Condensed
Bodoni MT Poster Compressed
Britannic Bold
Broadway
Brush Script MT
Californian FB
Centaur
Chiller
Colonna MT
Cooper Black
Footlight MT Light
Harlow Solid Italic
Harrington
High Tower Text
Jokerman
Kunstler Script
Lucida Bright
Lucida Calligraphy
Lucida Fax
Magneto
Matura MT Script Capitals
Modern No. 20
Niagara Engraved
Niagara Solid
Old English Text MT
Onyx
Parchment
Playbill
Poor Richard
Ravie
Informal Roman
Showcard Gothic
Snap ITC
Stencil
Viner Hand ITC
Vivaldi
Vladimir Script
Wide Latin
Century
Wingdings 2
Wingdings 3
Arial Unicode MS
@Arial Unicode MS
Arial Narrow
Rupee Foradian
Rupee
DevLys 010
Calibri Light
Monoton
Ubuntu Medium
Ubuntu
Ubuntu Light
Yatra One
HelvLight
Lato
Great Vibes"""
        text_widget = tk.Text(self.main_frame)
        text_widget.pack()
        # self.canvas = tk.Canvas(self)
        fonts = fonts.split("\n")
        for i, font_name in enumerate(fonts):
            text_widget.tag_config(font_name, font=(font_name, 16))
            text_widget.insert('end', font_name + " * ", font_name)
        text_widget.config(state='disabled')

    #######

    def next_section(self):
        if self.history_index == len(self.history) - 1:
            raise ("No next section")
        else:
            self.history_index += 1
            self.switch_to_section(self.history[self.history_index])

    def back_section(self):
        if self.history_index == 0:
            raise ("No back section")
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
        if dest == self.history[-1]: return
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
        # swtich to section:
        # Construct the method name as a string
        method_name = SECTION_FUNC_PREFIX + section_name
        # Use getattr to get the method by name
        method = getattr(self, method_name, None)
        if method:
            method()
        else:
            raise Exception(f"Method {method_name} not found.")
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


    ###################
    ##### SCREENS #####
    ###################

    def section_contents(self):
        # default
        self.add_heading("FSSA for Windows Help Index", H1)
        self.add_line_break()
        self.add_link("What is FSSA ?\n", s_WHAT_IS_FSSA)
        self.add_line_break()
        self.add_heading("How To ...", 'h2')
        self.add_link("Move between screens\n", 'move_between_screens')
        self.add_link("Use the keyboard\n", 'use_keyboard')
        self.add_link("Use facets\n", 'use_facets')
        self.add_link("Not use facets\n", 'not_use_facets')
        self.add_line_break()
        self.add_heading("Commands", 'h2')
        self.add_link("File menu\n", 'file_menu')
        self.add_link("Input Data menu\n", 'input_data_menu')
        self.add_link("SSA menu\n", 'ssa_menu')
        self.add_link("Facets menu\n", 'facets_menu')
        self.add_link("View menu\n", 'view_menu')
        self.add_link("Help menu\n", 'help_menu')

    def section_what_is_fssa(self):
        self.add_heading("What is FSSA ?")
        self.add_line_break()
        self.add_paragraph(WHAT_IS_FSSA_p1)
        self.add_heading("References", 'h2')
        self.add_line_break()
        self.add_paragraph(WHAT_IS_FSSA_p2, TEXT_SMALL)

    def section_move_between_screens(self):
        self.add_heading("How to move between screens")
        self.add_line_break()
        self.add_paragraph("There are two ways to navigate the screens:")
        self.add_txt("You can use the menu bar to choose commands from the ")
        self.add_link("Input Data, ", s_INPUT_DATA_MENU)
        self.add_link("SSA ", s_SSA_menu)
        self.add_txt("& ")
        self.add_link("Facets ", s_FACETS_MENU)
        self.add_paragraph("menus that will get you immediately where you "
                           "are going.")
        self.add_txt("Or, you can use the ")
        self.add_link("Next ", s_NEXT_COMMAND)
        self.add_txt("and ")
        self.add_link("Previous ", s_PREVIOUS_COMMAND)
        self.add_txt(
            "commands to move serially from one screen to the next. These commands are available through the ")
        self.add_link("View menu", s_VIEW_MENU)
        self.add_paragraph(
            ", through the toolbar, and through buttons on the bottom of the screen.")

    def section_input_data_menu(self):
        self.add_heading("Input Data menu commands")
        self.add_line_break()
        self.add_paragraph(
            "The Input Data menu offers the following commands:")
        e_1_2_a = "Open the recorded data file definitions screen, marking " \
                  "recorded data"
        self.add_txt(TABLE_PRE_PAD)
        self.add_link("Recorded Data", s_RECORDED_DATA_command)
        self.add_txt(8 * " " + e_1_2_a + "\n")
        self.add_txt((41 * " ") + "is to be used.\n")
        self.add_txt(TABLE_PRE_PAD)
        self.add_link("Coefficient", s_COEFFICIENT_MATRIX_COMMAND)
        self.add_txt(15 * " " + "Open the coefficient matrix file definitions "
                                "screen, marking a\n")
        self.add_txt(TABLE_PRE_PAD)
        self.add_link("Matrix", s_COEFFICIENT_MATRIX_COMMAND)
        self.add_txt((25 * " ") + "coefficient matrix is to be used.\n")
        self.add_txt(TABLE_PRE_PAD)
        self.add_link("Variables", s_VARIABLES_COMMAND)
        self.add_txt(19 * " " + "Open the Variable Definitions screen.\n")
        self.add_line_break()
        self.add_paragraph("Only one type of input can be used in each run; "
                           "the currently selected type (i.e. Recorded Data "
                           "or Coefficient Matrix) will be marked with a "
                           "check-mark in the Input Data menu.")

    def section_ssa_menu(self):
        self.add_heading("SSA menu commands")
        self.add_line_break()
        self.add_paragraph("The SSA menu offers the following commands:")
        self.add_row("Dimensions & Coeffs",
                     left_link=s_DIMENSIONS_AND_COEFFS_COMMAND,
                     right="Open the Dimensions and Coefficients screen.")
        self.add_row("Technical Options", left_link=s_TECHNICAL_OPTIONS_COMMAND,
                     right="Open the Technical Options dialog.")


    def section_use_keyboard(self):
        self.add_heading("How to use the keyboard")
        self.add_line_break()
        self.add_txt(USE_KEYBOARD_p1)
        self.add_link("Variable Elements in Facets screen",
                      s_VARIABLE_ELEMENTS_COMMAND)

    def section_use_facets(self):
        self.add_heading("How to use facets")
        self.add_line_break()
        self.add_txt(
            "To use facets, after you have defined and selected your variables, select")
        self.add_link(" Facets ", s_FACETS_MENU)
        self.add_txt(" | ")
        self.add_link("Element Labels", s_ELEMENT_LABELS_COMMAND)
        self.add_txt(" to go to the ")
        self.add_link("Facet Definition screen", s_FACETS_DEFINITION_SCREEN)
        self.add_paragraph(". In the box in the top right corner, choose the "
                           "number of facets you want. Fields will show up "
                           "for facet elements number and element labels, "
                           "for each facet. Fill those in if you want. In "
                           "addition, when you choose a number of facets to "
                           "use, the Next button will be enabled.")
        self.add_txt("Push ")
        self.add_link("Next", s_NEXT_COMMAND)
        self.add_txt(" to move to the ")
        self.add_link("Variable Elements in Facets screen",
                      s_VARIABLE_ELEMENTS_COMMAND)
        self.add_txt(". In this screen you should classify variables in "
                     "facets.\n")
        self.add_line_break()
        self.add_txt("You may go to the ")
        self.add_link("Facet Hypotheses", s_HYPOTHESES_SCREEN)
        self.add_txt(" and ")
        self.add_link("Facet Diagrams", s_FACET_DIAGRAMS_SCREEN)
        self.add_paragraph(" screens to fine-tune the output you want. They "
                           "are the next two screens.")

    def section_not_use_facets(self):
        self.add_heading("How to NOT use facets")
        self.add_line_break()
        self.add_txt("Select ")
        self.add_link("Facets", s_FACETS_MENU)
        self.add_txt(" | ")
        self.add_link("Element Labels", s_ELEMENT_LABELS_COMMAND)
        self.add_txt(" to go to the ")
        self.add_link("Facet Definition screen", s_FACETS_DEFINITION_SCREEN)
        self.add_paragraph(". In the box in the top right corner, choose 'No "
                           "facets'. The Next command, along with all other "
                           "commands on the Facets menu will be disabled, "
                           "and no facets will be used in the process.")

    def section_file_menu(self):
        self.add_heading("File menu commands")
        self.add_line_break()
        self.add_paragraph("The File menu offers the following commands:")
        self.add_txt(TABLE_PRE_PAD)
        self.add_link("New", s_NEW_command)
        self.add_txt(21 * " " + "Creates a new form.\n")
        self.add_txt(TABLE_PRE_PAD)
        self.add_link("Open", s_OPEN_command)
        self.add_txt(19 * " " + "Opens an existing form.\n")
        self.add_txt(TABLE_PRE_PAD)
        self.add_link("Save", s_SAVE_command)
        self.add_txt(
            21 * " " + "Saves an opened form using the same file name.\n")
        self.add_txt(TABLE_PRE_PAD)
        self.add_link("Save As", s_SAVE_AS_command)
        self.add_txt(
            15 * " " + "Saves an opened form to a specified file name.\n")
        self.add_txt(TABLE_PRE_PAD)
        self.add_link("Run", s_RUN_command)
        self.add_txt(23 * " " + "Runs FSSA according to current form\n")
        self.add_txt(TABLE_PRE_PAD)
        self.add_link("Exit", s_EXIT_command)
        self.add_paragraph(23 * " " + "Exits FSSA for Windows.")

    def section_open_command(self):
        self.add_heading("Open command (File menu)")
        self.add_line_break()
        self.add_paragraph("Use this command to open an existing form")
        self.add_paragraph("You can create new forms with the")
        self.add_link(" New command.", s_NEW_command)
        self.add_line_break()
        self.add_heading("Shortcuts")
        self.add_paragraph("Keys:CTRL+O")

    def section_run_command(self):
        self.add_heading("Run command (File menu)")
        self.add_line_break()
        self.add_paragraph(RUN_COMMAND_p1)

    def section_exit_command(self):
        self.add_heading("Exit command (File menu)")
        self.add_line_break()
        self.add_paragraph(EXIT_COMMAND_p1)
        self.add_heading("Shortcuts")
        self.add_paragraph("Keys:ESC")

    def section_recorded_data_screen(self):
        self.add_heading("Recorded data")
        self.add_line_break()
        self.add_txt(RECORDED_DATA_SCREEN_p1)
        self.add_link("Data screen", s_DATA_SCREEN)
        self.add_txt(RECORDED_DATA_SCREEN_p2)
        self.add_paragraph(RECORDED_DATA_SCREEN_p3)

    def section_facets_menu(self):
        self.add_heading("Facets menu commands")
        self.add_line_break()
        self.add_paragraph("The Facets menu offers the following commands:")
        self.add_row(left="Element Labels", left_link=s_ELEMENT_LABELS_COMMAND,
                     right="Open the Element Labels screen to define the labels for the elements.")
        self.add_row(left="Variable Elements", left_link=s_VARIABLE_ELEMENTS_COMMAND,
                     right="Open the Variable Elements in Facets screen to define to which element in each facet each variable belongs.")
        self.add_row(left="Hypotheses", left_link=s_HYPOTHESES_COMMAND,
                     right="Open the Hypotheses screen to specify which hypotheses to check for each facet.")
        self.add_row(left="Diagrams", left_link=s_DIAGRAMS_COMMAND,
                     offset=1,
                     right="Open the Facet Diagrams screen to specify which diagrams to draw.")

    def section_view_menu(self):
        self.add_heading("View menu commands")
        self.add_line_break()
        self.add_paragraph("The View menu offers the following commands:")
        self.add_row(left="Next", left_link=s_NEXT_COMMAND,
                     right="Move to next screen")
        self.add_row(left="Previous", left_link=s_PREVIOUS_COMMAND,
                     right="Move to previous screen")
        self.add_row(left="Toolbar",
                     right="Shows or hides the toolbar.")
        self.add_row(left="Status Bar",
                     right="Shows or hides the status bar.")
        self.add_row(left="Input File", left_link=s_INPUT_FILE,
                     right="Open input file in a DOS editor.")
        self.add_row(left="Output File", left_link=s_OUTPUT_FILE,
                     right="Open last output file in a DOS editor.")
        self.add_row(left="Diagrams", left_link=s_DIAGRAMS_COMMAND,
                     right="Show diagrams for last run.")

    def section_help_menu(self):
        self.add_heading("Help menu commands")
        self.add_line_break()
        tmp = self.col_width
        self.col_width = 50
        self.add_paragraph(
            "The Help menu offers the following commands, which provide you assistance with this application:")
        self.add_row(left="Contents", left_link=s_CONTENTS,
                     right="Opens the help main screen, for general help.")
        self.add_row(left="Help on current screen",
                     right="Provides help on the currently visible screen of the application.")
        self.add_row(left="Open Readme.txt", offset=-2,
                     right="Opens the file Readme.txt (supplied with FSSA for Windows) in notepad for viewing.")
        self.add_row(left="About", left_link=s_ABOUT_COMMAND,
                     right="Displays the version number of this application.")
        self.col_width = tmp

    def section_new_command(self):
        self.add_heading("New command (File menu)")
        self.add_line_break()
        self.add_paragraph(
            "Use this command to create a new form in FSSA for Windows. Select the type of input for the new form you want to create in the New form dialog box.")
        self.add_paragraph(
            "You can open an existing form with the Open command.")
        self.add_heading("Shortcuts", tag="h2")
        self.add_paragraph("Keys:CTRL+N")

    def section_new_form_dialog_box(self):
        self.add_heading("New form dialog box")
        self.add_line_break()
        self.add_paragraph(NEW_FORM_DIALOG_BOX_p1)

    def section_save_command(self):
        self.add_heading("Save command (File menu)")
        self.add_line_break()
        self.add_paragraph(
            "Use this command to save the active form to its current name "
            "and directory. When you save a form for the first time, "
            "FSSA for Windows displays the Save As dialog box so you can "
            "name your form. If you want to change the name and directory of "
            "an existing form before you save it, choose the")
        self.add_link("Save As command", s_SAVE_AS_command)
        self.add_paragraph(".")
        self.add_heading("Shortcuts", tag="h2")
        self.add_paragraph("Keys:CTRL+S")

    def section_save_as_command(self):
        self.add_heading("Save As command (File menu)")
        self.add_line_break()
        self.add_paragraph(
            "Use this command to save the active form to a new name or directory. "
            "FSSA for Windows displays the Save As dialog box so you can name your form.")
        self.add_paragraph("To save a form with its existing name and "
                           "directory, use the ")
        self.add_link("Save command", s_SAVE_command)
        self.add_paragraph(".")
        self.add_heading("Shortcuts", tag="h2")
        self.add_paragraph("Keys:CTRL+SHIFT+S")

    def section_recorded_data_command(self):
        self.add_heading("Recorded Data command (File menu)")
        self.add_line_break()
        self.add_paragraph(
            "Use this command to open the Recorded Data screen, where you can enter the data you want to analyze.")
        self.add_paragraph(
            "You can also open the Recorded Data screen by clicking the Recorded Data button on the toolbar.")
        self.add_link("Recorded Data file definition screen screen",
                      s_RECORDED_DATA_SCREEN)
        self.add_paragraph(".")

    def section_manual_variables_screen(self):
        self.add_heading("Manual Variables Screen")
        self.add_line_break()
        self.add_paragraph(MANUAL_VARIABLES_SCREEN_p1)

    def section_dimensions_and_coeffs_command(self):
        self.add_heading("Dimensions and Coeffs command (SSA menu)")
        self.add_line_break()
        self.add_paragraph(
            "Use this command to open the Dimensions and Coeffs screen, where you can enter the dimensions and coefficients for the form you want to analyze.")
        self.add_paragraph(
            "You can also open the Dimensions and Coeffs screen by clicking the Dimensions and Coeffs button on the toolbar.")
        self.add_link("Dimensions and Coefficients screen",
                      s_DIMENSIONS_AND_COEFFS_SCREEN)
        self.add_paragraph(".")

    def section_dimensions_and_coeffs_screen(self):
        self.add_heading("Dimensions and Coefficients Screen")
        self.add_line_break()
        self.add_paragraph(DIMENSIONS_AND_COEFFS_SCREEN_p1)

    def section_facets_definition_screen(self):
        self.add_heading("Facets Definition Screen")
        self.add_line_break()
        self.add_paragraph(FACETS_DEFINITION_SCREEN_p1)

    def variables_facets_screen(self):
        self.add_heading("Variable Elements in Facets screen")
        self.add_line_break()
        self.add_paragraph(VARIABLES_FACETS_SCREEN_p1)

    def section_hypotheses_screen(self):
        self.add_heading("Regional Hypotheses Screen")
        self.add_line_break()
        self.add_paragraph(REGIONAL_HYPOTHESES_SCREEN_p1)

    def section_facet_diagrams_screen(self):
        self.add_heading("Facet Diagrams Screen")
        self.add_line_break()
        self.add_paragraph(FACET_DIAGRAM_SCREEN_p1)

    def section_next_command(self):
        self.add_heading("Next command (View menu)")
        self.add_paragraph(NEXT_command_p1)

    def section_previous_command(self):
        self.add_heading("Previous command (View menu)")
        self.add_paragraph(PREVIOUS_command_p1)

    def section_input_file_command(self):
        self.add_heading("Input File command (View menu)")
        self.add_paragraph(INPUT_FILE_command_p1)

    def section_output_file_command(self):
        self.add_heading("Output File command (View menu)")
        self.add_paragraph(OUTPUT_FILE_command_p1)

    def section_element_labels_command(self):
        self.add_heading("Element Labels command (Facets menu)")
        self.add_line_break()
        self.add_txt("Use this command to open the ")
        self.add_link("Facets Definition screen", s_FACETS_DEFINITION_SCREEN)
        self.add_paragraph(ELEMENT_LABELS_COMMAND_p1)

    def section_coefficient_matrix_command(self):
        self.add_heading("Coefficient Matrix command (Input Data menu)")
        self.add_line_break()
        self.add_txt("Use this command to indicate you are going to use a "
                     "file containing a matrix of coefficients of similarity "
                     "(or dissimilarity) between your variables, and open "
                     "the ")
        self.add_link("Coefficient Matrix screen", s_COEFFICIENT_MATRIX_SCREEN)
        self.add_paragraph(".")

    def section_variables_command(self):
        self.add_heading("Variables command (Input Data menu)")
        self.add_line_break()
        self.add_txt("Use this command to open the ")
        self.add_link("Variables screen", s_VARIABLES_SCREEN)
        self.add_paragraph(", where you can define variable labels and select"
                   "variables for a run. If you are working with Recorded "
                           "Data, you are also required to define the file "
                           "structure (i.e. where in the file the variables "
                           "data reside) in this screen.")

    def section_data_screen(self):
        self.add_heading("Data Screen")
        self.add_line_break()
        self.add_paragraph(" TO BE DONE")

    def section_technical_options_command(self):
        self.add_heading("Technical Options command (SSA menu)")
        self.add_line_break()
        self.add_txt("Use this command to open the ")
        self.add_link("Technical Options dialog", s_TECHNICAL_OPTIONS_DIALOG)
        self.add_paragraph(" where you can set some output formatting options and the "
               "weight for locality.")

    def section_variable_elements_command(self):
        self.add_heading("Variable elements command (Facets menu)")
        self.add_line_break()
        self.add_txt("Use this command to open the ")
        self.add_link("Variable Elements in Facets screen",
                      s_VARIABLE_ELEMENTS_FACETS_SCREEN)
        self.add_paragraph(" to define for each variable, to which element in each facet it belongs.")

    def section_variable_elements_in_facets_screen(self):
        self.add_heading("Variable Elements in Facets screen")
        self.add_line_break()
        self.add_paragraph(VARIABLE_ELEMENTS_IN_FACETS_SCREEN_p1)

    def section_hypotheses_command(self):
        self.add_heading("Hypotheses command (Facets menu)")
        self.add_line_break()
        self.add_txt("Use this command to open the ")
        self.add_link("Regional Hypotheses screen", s_HYPOTHESES_SCREEN)
        self.add_paragraph("to specify which geometric hypotheses to check "
                           "for each facet.")

    def section_diagrams_command(self):
        self.add_heading("Diagrams command (Facets menu)")
        self.add_txt("Use this command to open the ")
        self.add_link("Facet Diagrams screen", s_FACET_DIAGRAMS_SCREEN)
        self.add_paragraph("to specify which dimensionalities are to be "
                           "diagrammed for each facet.")


    def section_about_command(self):
        self.add_heading("About command (Help menu)")
        self.add_line_break()
        self.add_paragraph("Use this command to display the copyright notice "
                         "and version number of your copy of FSSA for "
                         "Windows.")
