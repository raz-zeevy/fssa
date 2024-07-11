from lib.moduls.help_content import *

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


class ScreensGenerator():
    def __init__(self, master):
        self.master = master

    def section(self, section_name):
        # swtich to section:
        # Construct the method name as a string
        method_name = SECTION_FUNC_PREFIX + section_name
        # Use getattr to get the method by name
        method = getattr(self, method_name, None)
        if method:
            method()
        else:
            raise Exception(f"Method {method_name} not found.")

    def section_contents(self):
        # default
        self.master.add_heading("FSSA for Windows Help Index", H1)
        self.master.add_line_break()
        self.master.add_link("What is FSSA ?\n", s_WHAT_IS_FSSA)
        self.master.add_line_break()
        self.master.add_heading("How To ...", 'h2')
        self.master.add_link("Move between screens\n", 'move_between_screens')
        self.master.add_link("Use the keyboard\n", 'use_keyboard')
        self.master.add_link("Use facets\n", 'use_facets')
        self.master.add_link("Not use facets\n", 'not_use_facets')
        self.master.add_line_break()
        self.master.add_heading("Commands", 'h2')
        self.master.add_link("File menu\n", 'file_menu')
        self.master.add_link("Input Data menu\n", 'input_data_menu')
        self.master.add_link("SSA menu\n", 'ssa_menu')
        self.master.add_link("Facets menu\n", 'facets_menu')
        self.master.add_link("View menu\n", 'view_menu')
        self.master.add_link("Help menu\n", 'help_menu')

    def section_what_is_fssa(self):
        self.master.add_heading("What is FSSA ?")
        self.master.add_line_break()
        self.master.add_paragraph(WHAT_IS_FSSA_p1)
        self.master.add_heading("References", 'h2')
        self.master.add_line_break()
        self.master.add_paragraph(WHAT_IS_FSSA_p2, TEXT_SMALL)

    def section_move_between_screens(self):
        self.master.add_heading("How to move between screens")
        self.master.add_line_break()
        self.master.add_paragraph("There are two ways to navigate the "
                                  "screens:")
        self.master.add_txt("You can use the menu bar to choose commands from "
                            "the ")
        self.master.add_link("Input Data, ", s_INPUT_DATA_MENU)
        self.master.add_link("SSA ", s_SSA_menu)
        self.master.add_txt("& ")
        self.master.add_link("Facets ", s_FACETS_MENU)
        self.master.add_paragraph("menus that will get you immediately where "
                                  "you "
                                  "are going.")
        self.master.add_txt("Or, you can use the ")
        self.master.add_link("Next ", s_NEXT_COMMAND)
        self.master.add_txt("and ")
        self.master.add_link("Previous ", s_PREVIOUS_COMMAND)
        self.master.add_txt(
            "commands to move serially from one screen to the next. These commands are available through the ")
        self.master.add_link("View menu", s_VIEW_MENU)
        self.master.add_paragraph(
            ", through the toolbar, and through buttons on the bottom of the screen.")

    def section_input_data_menu(self):
        self.master.add_heading("Input Data menu commands")
        self.master.add_line_break()
        self.master.add_paragraph(
            "The Input Data menu offers the following commands:")
        e_1_2_a = "Open the recorded data file definitions screen, marking " \
                  "recorded data"
        self.master.add_txt(TABLE_PRE_PAD)
        self.master.add_link("Recorded Data", s_RECORDED_DATA_command)
        self.master.add_txt(8 * " " + e_1_2_a + "\n")
        self.master.add_txt((41 * " ") + "is to be used.\n")
        self.master.add_txt(TABLE_PRE_PAD)
        self.master.add_link("Coefficient", s_COEFFICIENT_MATRIX_COMMAND)
        self.master.add_txt(15 * " " + "Open the coefficient matrix file "
                                       "definitions "
                                       "screen, marking a\n")
        self.master.add_txt(TABLE_PRE_PAD)
        self.master.add_link("Matrix", s_COEFFICIENT_MATRIX_COMMAND)
        self.master.add_txt((25 * " ") + "coefficient matrix is to be used.\n")
        self.master.add_txt(TABLE_PRE_PAD)
        self.master.add_link("Variables", s_VARIABLES_COMMAND)
        self.master.add_txt(19 * " " + "Open the Variable Definitions "
                                       "screen.\n")
        self.master.add_line_break()
        self.master.add_paragraph("Only one type of input can be used in each "
                                  "run; "
                                  "the currently selected type (i.e. Recorded Data "
                                  "or Coefficient Matrix) will be marked with a "
                                  "check-mark in the Input Data menu.")

    def section_ssa_menu(self):
        self.master.add_heading("SSA menu commands")
        self.master.add_line_break()
        self.master.add_paragraph("The SSA menu offers the following "
                                  "commands:")
        self.master.add_row("Dimensions & Coeffs",
                            left_link=s_DIMENSIONS_AND_COEFFS_COMMAND,
                            right="Open the Dimensions and Coefficients screen.")
        self.master.add_row("Technical Options",
                            left_link=s_TECHNICAL_OPTIONS_COMMAND,
                            right="Open the Technical Options dialog.")

    def section_use_keyboard(self):
        self.master.add_heading("How to use the keyboard")
        self.master.add_line_break()
        self.master.add_txt(USE_KEYBOARD_p1)
        self.master.add_link("Variable Elements in Facets screen",
                             s_VARIABLE_ELEMENTS_COMMAND)

    def section_use_facets(self):
        self.master.add_heading("How to use facets")
        self.master.add_line_break()
        self.master.add_txt(
            "To use facets, after you have defined and selected your variables, select")
        self.master.add_link(" Facets ", s_FACETS_MENU)
        self.master.add_txt(" | ")
        self.master.add_link("Element Labels", s_ELEMENT_LABELS_COMMAND)
        self.master.add_txt(" to go to the ")
        self.master.add_link("Facet Definition screen",
                             s_FACETS_DEFINITION_SCREEN)
        self.master.add_paragraph(". In the box in the top right corner, "
                                  "choose "
                                  "the "
                                  "number of facets you want. Fields will show up "
                                  "for facet elements number and element labels, "
                                  "for each facet. Fill those in if you want. In "
                                  "addition, when you choose a number of facets to "
                                  "use, the Next button will be enabled.")
        self.master.add_txt("Push ")
        self.master.add_link("Next", s_NEXT_COMMAND)
        self.master.add_txt(" to move to the ")
        self.master.add_link("Variable Elements in Facets screen",
                             s_VARIABLE_ELEMENTS_COMMAND)
        self.master.add_txt(". In this screen you should classify variables "
                            "in "
                            "facets.\n")
        self.master.add_line_break()
        self.master.add_txt("You may go to the ")
        self.master.add_link("Facet Hypotheses", s_HYPOTHESES_SCREEN)
        self.master.add_txt(" and ")
        self.master.add_link("Facet Diagrams", s_FACET_DIAGRAMS_SCREEN)
        self.master.add_paragraph(" screens to fine-tune the output you want. "
                                  "They "
                                  "are the next two screens.")

    def section_not_use_facets(self):
        self.master.add_heading("How to NOT use facets")
        self.master.add_line_break()
        self.master.add_txt("Select ")
        self.master.add_link("Facets", s_FACETS_MENU)
        self.master.add_txt(" | ")
        self.master.add_link("Element Labels", s_ELEMENT_LABELS_COMMAND)
        self.master.add_txt(" to go to the ")
        self.master.add_link("Facet Definition screen",
                             s_FACETS_DEFINITION_SCREEN)
        self.master.add_paragraph(". In the box in the top right corner, "
                                  "choose "
                                  "'No "
                                  "facets'. The Next command, along with all other "
                                  "commands on the Facets menu will be disabled, "
                                  "and no facets will be used in the process.")

    def section_file_menu(self):
        self.master.add_heading("File menu commands")
        self.master.add_line_break()
        self.master.add_paragraph("The File menu offers the following "
                                  "commands:")
        self.master.add_txt(TABLE_PRE_PAD)
        self.master.add_link("New", s_NEW_command)
        self.master.add_txt(21 * " " + "Creates a new form.\n")
        self.master.add_txt(TABLE_PRE_PAD)
        self.master.add_link("Open", s_OPEN_command)
        self.master.add_txt(19 * " " + "Opens an existing form.\n")
        self.master.add_txt(TABLE_PRE_PAD)
        self.master.add_link("Save", s_SAVE_command)
        self.master.add_txt(
            21 * " " + "Saves an opened form using the same file name.\n")
        self.master.add_txt(TABLE_PRE_PAD)
        self.master.add_link("Save As", s_SAVE_AS_command)
        self.master.add_txt(
            15 * " " + "Saves an opened form to a specified file name.\n")
        self.master.add_txt(TABLE_PRE_PAD)
        self.master.add_link("Run", s_RUN_command)
        self.master.add_txt(23 * " " + "Runs FSSA according to current form\n")
        self.master.add_txt(TABLE_PRE_PAD)
        self.master.add_link("Exit", s_EXIT_command)
        self.master.add_paragraph(23 * " " + "Exits FSSA for Windows.")

    def section_open_command(self):
        self.master.add_heading("Open command (File menu)")
        self.master.add_line_break()
        self.master.add_paragraph("Use this command to open an existing form")
        self.master.add_paragraph("You can create new forms with the")
        self.master.add_link(" New command.", s_NEW_command)
        self.master.add_line_break()
        self.master.add_heading("Shortcuts")
        self.master.add_paragraph("Keys:CTRL+O")

    def section_run_command(self):
        self.master.add_heading("Run command (File menu)")
        self.master.add_line_break()
        self.master.add_paragraph(RUN_COMMAND_p1)

    def section_exit_command(self):
        self.master.add_heading("Exit command (File menu)")
        self.master.add_line_break()
        self.master.add_paragraph(EXIT_COMMAND_p1)
        self.master.add_heading("Shortcuts")
        self.master.add_paragraph("Keys:ESC")

    def section_recorded_data_screen(self):
        self.master.add_heading("Recorded data")
        self.master.add_line_break()
        self.master.add_txt(RECORDED_DATA_SCREEN_p1)
        self.master.add_link("Data screen", s_DATA_SCREEN)
        self.master.add_txt(RECORDED_DATA_SCREEN_p2)
        self.master.add_paragraph(RECORDED_DATA_SCREEN_p3)

    def section_facets_menu(self):
        self.master.add_heading("Facets menu commands")
        self.master.add_line_break()
        self.master.add_paragraph("The Facets menu offers the following "
                                  "commands:")
        self.master.add_row(left="Element Labels",
                            left_link=s_ELEMENT_LABELS_COMMAND,
                            right="Open the Element Labels screen to define the labels for the elements.")
        self.master.add_row(left="Variable Elements",
                            left_link=s_VARIABLE_ELEMENTS_COMMAND,
                            right="Open the Variable Elements in Facets screen to define to which element in each facet each variable belongs.")
        self.master.add_row(left="Hypotheses", left_link=s_HYPOTHESES_COMMAND,
                            right="Open the Hypotheses screen to specify which hypotheses to check for each facet.")
        self.master.add_row(left="Diagrams", left_link=s_DIAGRAMS_COMMAND,
                            offset=1,
                            right="Open the Facet Diagrams screen to specify which diagrams to draw.")

    def section_view_menu(self):
        self.master.add_heading("View menu commands")
        self.master.add_line_break()
        self.master.add_paragraph("The View menu offers the following "
                                  "commands:")
        self.master.add_row(left="Next", left_link=s_NEXT_COMMAND,
                            right="Move to next screen")
        self.master.add_row(left="Previous", left_link=s_PREVIOUS_COMMAND,
                            right="Move to previous screen")
        self.master.add_row(left="Toolbar",
                            right="Shows or hides the toolbar.")
        self.master.add_row(left="Status Bar",
                            right="Shows or hides the status bar.")
        self.master.add_row(left="Input File", left_link=s_INPUT_FILE,
                            right="Open input file in a DOS editor.")
        self.master.add_row(left="Output File", left_link=s_OUTPUT_FILE,
                            right="Open last output file in a DOS editor.")
        self.master.add_row(left="Diagrams", left_link=s_DIAGRAMS_COMMAND,
                            right="Show diagrams for last run.")

    def section_help_menu(self):
        self.master.add_heading("Help menu commands")
        self.master.add_line_break()
        tmp = self.master.col_width
        self.master.col_width = 50
        self.master.add_paragraph(
            "The Help menu offers the following commands, which provide you assistance with this application:")
        self.master.add_row(left="Contents", left_link=s_CONTENTS,
                            right="Opens the help main screen, for general help.")
        self.master.add_row(left="Help on current screen",
                            right="Provides help on the currently visible screen of the application.")
        self.master.add_row(left="Open Readme.txt", offset=-2,
                            right="Opens the file Readme.txt (supplied with FSSA for Windows) in notepad for viewing.")
        self.master.add_row(left="About", left_link=s_ABOUT_COMMAND,
                            right="Displays the version number of this application.")
        self.master.col_width = tmp

    def section_new_command(self):
        self.master.add_heading("New command (File menu)")
        self.master.add_line_break()
        self.master.add_paragraph(
            "Use this command to create a new form in FSSA for Windows. Select the type of input for the new form you want to create in the New form dialog box.")
        self.master.add_paragraph(
            "You can open an existing form with the Open command.")
        self.master.add_heading("Shortcuts", tag="h2")
        self.master.add_paragraph("Keys:CTRL+N")

    def section_new_form_dialog_box(self):
        self.master.add_heading("New form dialog box")
        self.master.add_line_break()
        self.master.add_paragraph(NEW_FORM_DIALOG_BOX_p1)

    def section_save_command(self):
        self.master.add_heading("Save command (File menu)")
        self.master.add_line_break()
        self.master.add_paragraph(
            "Use this command to save the active form to its current name "
            "and directory. When you save a form for the first time, "
            "FSSA for Windows displays the Save As dialog box so you can "
            "name your form. If you want to change the name and directory of "
            "an existing form before you save it, choose the")
        self.master.add_link("Save As command", s_SAVE_AS_command)
        self.master.add_paragraph(".")
        self.master.add_heading("Shortcuts", tag="h2")
        self.master.add_paragraph("Keys:CTRL+S")

    def section_save_as_command(self):
        self.master.add_heading("Save As command (File menu)")
        self.master.add_line_break()
        self.master.add_paragraph(
            "Use this command to save the active form to a new name or directory. "
            "FSSA for Windows displays the Save As dialog box so you can name your form.")
        self.master.add_paragraph("To save a form with its existing name and "
                                  "directory, use the ")
        self.master.add_link("Save command", s_SAVE_command)
        self.master.add_paragraph(".")
        self.master.add_heading("Shortcuts", tag="h2")
        self.master.add_paragraph("Keys:CTRL+SHIFT+S")

    def section_recorded_data_command(self):
        self.master.add_heading("Recorded Data command (File menu)")
        self.master.add_line_break()
        self.master.add_paragraph(
            "Use this command to open the Recorded Data screen, where you can enter the data you want to analyze.")
        self.master.add_paragraph(
            "You can also open the Recorded Data screen by clicking the Recorded Data button on the toolbar.")
        self.master.add_link("Recorded Data file definition screen screen",
                             s_RECORDED_DATA_SCREEN)
        self.master.add_paragraph(".")

    def section_manual_variables_screen(self):
        self.master.add_heading("Manual Variables Screen")
        self.master.add_line_break()
        self.master.add_paragraph(MANUAL_VARIABLES_SCREEN_p1)

    def section_dimensions_and_coeffs_command(self):
        self.master.add_heading("Dimensions and Coeffs command (SSA menu)")
        self.master.add_line_break()
        self.master.add_paragraph(
            "Use this command to open the Dimensions and Coeffs screen, where you can enter the dimensions and coefficients for the form you want to analyze.")
        self.master.add_paragraph(
            "You can also open the Dimensions and Coeffs screen by clicking the Dimensions and Coeffs button on the toolbar.")
        self.master.add_link("Dimensions and Coefficients screen",
                             s_DIMENSIONS_AND_COEFFS_SCREEN)
        self.master.add_paragraph(".")

    def section_dimensions_and_coeffs_screen(self):
        self.master.add_heading("Dimensions and Coefficients Screen")
        self.master.add_line_break()
        self.master.add_paragraph(DIMENSIONS_AND_COEFFS_SCREEN_p1)

    def section_facets_definition_screen(self):
        self.master.add_heading("Facets Definition Screen")
        self.master.add_line_break()
        self.master.add_paragraph(FACETS_DEFINITION_SCREEN_p1)

    def variables_facets_screen(self):
        self.master.add_heading("Variable Elements in Facets screen")
        self.master.add_line_break()
        self.master.add_paragraph(VARIABLES_FACETS_SCREEN_p1)

    def section_hypotheses_screen(self):
        self.master.add_heading("Regional Hypotheses Screen")
        self.master.add_line_break()
        self.master.add_paragraph(REGIONAL_HYPOTHESES_SCREEN_p1)

    def section_facet_diagrams_screen(self):
        self.master.add_heading("Facet Diagrams Screen")
        self.master.add_line_break()
        self.master.add_paragraph(FACET_DIAGRAM_SCREEN_p1)

    def section_next_command(self):
        self.master.add_heading("Next command (View menu)")
        self.master.add_paragraph(NEXT_command_p1)

    def section_previous_command(self):
        self.master.add_heading("Previous command (View menu)")
        self.master.add_paragraph(PREVIOUS_command_p1)

    def section_input_file_command(self):
        self.master.add_heading("Input File command (View menu)")
        self.master.add_paragraph(INPUT_FILE_command_p1)

    def section_output_file_command(self):
        self.master.add_heading("Output File command (View menu)")
        self.master.add_paragraph(OUTPUT_FILE_command_p1)

    def section_element_labels_command(self):
        self.master.add_heading("Element Labels command (Facets menu)")
        self.master.add_line_break()
        self.master.add_txt("Use this command to open the ")
        self.master.add_link("Facets Definition screen",
                             s_FACETS_DEFINITION_SCREEN)
        self.master.add_paragraph(ELEMENT_LABELS_COMMAND_p1)

    def section_coefficient_matrix_command(self):
        self.master.add_heading("Coefficient Matrix command (Input Data menu)")
        self.master.add_line_break()
        self.master.add_txt("Use this command to indicate you are going to use"
                            " a "
                            "file containing a matrix of coefficients of similarity "
                            "(or dissimilarity) between your variables, and open "
                            "the ")
        self.master.add_link("Coefficient Matrix screen",
                             s_COEFFICIENT_MATRIX_SCREEN)
        self.master.add_paragraph(".")

    def section_variables_command(self):
        self.master.add_heading("Variables command (Input Data menu)")
        self.master.add_line_break()
        self.master.add_txt("Use this command to open the ")
        self.master.add_link("Variables screen", s_VARIABLE_DEFINITION)
        self.master.add_paragraph(", where you can define variable labels and "
                                  "select"
                                  "variables for a run. If you are working with Recorded "
                                  "Data, you are also required to define the file "
                                  "structure (i.e. where in the file the variables "
                                  "data reside) in this screen.")

    def section_data_screen(self):
        self.master.add_heading("Data Screen")
        self.master.add_line_break()
        self.master.add_paragraph(
            "In this screen, you will define and visualize the data that has been loaded into FSSA for analysis. Here are the steps and options available:"
        )
        self.master.add_paragraph(
            "1. Data Table Display: The main area of this screen shows a table where each row represents a record, and each column represents a variable. You can scroll through this table to inspect the data that has been loaded."
        )
        self.master.add_paragraph(
            "2. Reload Input: This button allows you to reload the input data file. If there have been changes to the data file outside of FSSA, or if you need to refresh the data for any reason, clicking this button will update the data displayed in the table."
        )
        self.master.add_paragraph(
            "3. Save To...: This option allows you to save the current state of your data. You can save the data to a specified file for later use or for further processing in other software."
        )
        self.master.add_paragraph(
            "4. Select Vars.: This button opens a dialog where you can select which variables (columns) you want to include in the analysis. By selecting specific variables, you can focus the analysis on relevant data, excluding any extraneous information."
        )
        self.master.add_paragraph(
            "5. Recode Vars.: This feature lets you transform or recode variables. If you need to adjust the data, such as converting categorical variables to numeric codes or normalizing values, this option provides the tools to do so."
        )
        self.master.add_paragraph(
            "6. Navigation Buttons: Use the \"Previous\" and \"Next\" buttons to move through the different screens in the FSSA workflow. The \"Previous\" button will take you back to the Variable Definition Screen, while the \"Next\" button will advance you to the Dimensions and Coefficients Screen."
        )
        self.master.add_paragraph(
            "7. Run: After configuring and verifying all your data and settings, clicking \"Run\" will start the analysis process using the defined variables and parameters."
        )
        self.master.add_paragraph(
            "Additional Notes:"
        )
        self.master.add_paragraph(
            "Data Validation: Ensure your data is correctly formatted and complete before running the analysis. Check for any missing or inconsistent values that might affect the results."
        )
        self.master.add_paragraph(
            "Help: For more detailed information on each feature or step, press F1 at any time to access the help documentation specific to the current screen."
        )

    def section_technical_options_command(self):
        self.master.add_heading("Technical Options command (SSA menu)")
        self.master.add_line_break()
        self.master.add_txt("Use this command to open the ")
        self.master.add_link("Technical Options dialog",
                             s_TECHNICAL_OPTIONS_DIALOG)
        self.master.add_paragraph(
            " where you can set some output formatting options and the "
            "weight for locality.")

    def section_variable_elements_command(self):
        self.master.add_heading("Variable elements command (Facets menu)")
        self.master.add_line_break()
        self.master.add_txt("Use this command to open the ")
        self.master.add_link("Variable Elements in Facets screen",
                             s_VARIABLE_ELEMENTS_FACETS_SCREEN)
        self.master.add_paragraph(
            " to define for each variable, to which element in each facet it belongs.")

    def section_variable_elements_in_facets_screen(self):
        self.master.add_heading("Variable Elements in Facets screen")
        self.master.add_line_break()
        self.master.add_paragraph(VARIABLE_ELEMENTS_IN_FACETS_SCREEN_p1)

    def section_hypotheses_command(self):
        self.master.add_heading("Hypotheses command (Facets menu)")
        self.master.add_line_break()
        self.master.add_txt("Use this command to open the ")
        self.master.add_link("Regional Hypotheses screen", s_HYPOTHESES_SCREEN)
        self.master.add_paragraph("to specify which geometric hypotheses to "
                                  "check "
                                  "for each facet.")

    def section_diagrams_command(self):
        self.master.add_heading("Diagrams command (Facets menu)")
        self.master.add_txt("Use this command to open the ")
        self.master.add_link("Facet Diagrams screen", s_FACET_DIAGRAMS_SCREEN)
        self.master.add_paragraph("to specify which dimensionalities are to "
                                  "be "
                                  "diagrammed for each facet.")

    def section_about_command(self):
        self.master.add_heading("About command (Help menu)")
        self.master.add_line_break()
        self.master.add_paragraph("Use this command to display the copyright "
                                  "notice "
                                  "and version number of your copy of FSSA for "
                                  "Windows.")

    def section_variable_definition_screen(self):
        self.master.add_heading("Variable Definition Screen")
        self.master.add_line_break()
        self.master.add_paragraph(VARIABLE_DEFINITION_SCREEN_p1)
        self.master.add_row(left="#", right="Variable serial number.")
        self.master.add_row(left="Line No.",
                            right="In which record is the variable located.")
        self.master.add_row(left="Start Col.",
                            right="Starting column in the record. If field width "
                                  "is 2 this the number of the first column.")
        self.master.add_paragraph(
            "If you use recorded data and specify that zero is not the only missing value, the table will also have the following columns:")
        self.master.add_row(left="Valid Hi/Lo.",
                            right="The valid minimum and maximum values of the variable")
        self.master.add_heading("Editing variables", tag="h2")
        self.master.add_paragraph(VARIABLE_DEFINITION_SCREEN_p2)

    def section_dimensions_and_coefficients_screen(self):
        self.master.add_heading("Dimensions and Coefficients Screen")
        self.master.add_line_break()
        self.master.add_paragraph(DIMENSIONS_AND_COEFFICIENTS_SCREEN_p1)
