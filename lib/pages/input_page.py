from tkinter import filedialog, Menu
import ttkbootstrap as ttk
from lib.components.form import *
from lib.utils import *
from tktooltip import ToolTip

FIXED_WIDTH_OPTIONS = ["No", DELIMITER_1_D, DELIMITER_2_D]
AUTO_PARSING_DELIMITER_OPTIONS = ["None", "Tab", "Comma", "Space"]
ENTRIES_PADX = 20


class InputPage(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent.root)
        self.create_entries()
        self.automatic_parsable = False
        self.additional_options = True
        # self.create_navigation()

    #######
    # Gui #
    #######

    def create_entries(self):
        # Data File Frame
        frame_data_file = ttk.Frame(self)
        frame_data_file.pack(fill='x', padx=ENTRIES_PADX, pady=(40, 0))
        # Data File Entry
        label_data_file = Label(frame_data_file, text="Data File:")
        label_data_file.pack(side=ttk.LEFT, padx=(0, 10))
        data_file_path = ttk.StringVar()
        self.entry_data_file = ttk.Entry(frame_data_file, width=50,
                                         validate="focusout",
                                         textvariable=data_file_path, )
        self.entry_data_file.pack(side=ttk.LEFT, fill='x', expand=True)
        self.button_load = ttk.Button(frame_data_file,
                                        text="Browse &\nLoad")
        self.button_load.pack(side=ttk.LEFT, padx=10)
        ToolTip(self.button_load,
                msg="Click to select a data file and load it\n"
                    "into the system. This program accepts .csv,\n"
                    "excel or any file that contains only the\n"
                    "digits 0-9 with or without separators (see\n"
                    "below in 'Additional Data Options')",
                delay=TOOL_TIP_DELAY)
        self.button_browse = ttk.Button(frame_data_file,
                                        width=rreal_size(7),
                                        text="Browse\nOnly",
                                        bootstyle="secondary",)
        self.button_browse.pack(side=ttk.LEFT, padx=10)
        ToolTip(self.button_browse,
                msg="Click to select a data file without changing\nthe"
                    " current state of the job. Used for loading\nsame job "
                    "with a different data file path.",
                delay=TOOL_TIP_DELAY)
        # Missing Value Frame
        frame_missing_value = ttk.Frame(self)
        frame_missing_value.pack(fill='x', padx=ENTRIES_PADX, pady=(20, 0))
        # Label for the text
        label_text = Label(frame_missing_value,
                               text="If in any of the variables, zero (0) is a "
                                    "valid value, or "
                                    "values "
                                    "other than zero (0) represent missing "
                                    "values, switch this option on.",
                               anchor='w',  # Aligns text to the west (left)
                               justify=ttk.LEFT,
                               wraplength=real_size(WINDOW_WIDTH - 200))
        label_text.pack(side=ttk.LEFT, fill='x', expand=True)
        # Checkbox, without text, aligned to the right
        self.missing_value_var = ttk.BooleanVar(value=False)
        self.checkbox_missing_value = ttk.Checkbutton(frame_missing_value,
                                                      bootstyle="round-toggle",
                                                      variable=self.missing_value_var,
                                                      onvalue=True,
                                                      offvalue=False)
        self.checkbox_missing_value.pack(side=ttk.RIGHT, padx=(0, 27))
        # Data type label
        self.label_data_type = Label(self, text="If your data file is not "
                                                    "in "
                                                    "any of the following "
                                                    "formats: csv, excel, "
                                                    "or tsv, please fill the "
                                                    "additional data options to "
                                                    "parse the variables.",
                                         wraplength=real_size(WINDOW_WIDTH -
                                                    200) )
        self.label_data_type.pack(fill='x', padx=ENTRIES_PADX, pady=(20, 0))
        #
        self.additiona_options_frame = ttk.LabelFrame(self, text="Additional "
                                                                 "Data "
                                                                 "Options",
                                                      bootstyle="primary")
        self.additiona_options_frame.pack(fill='x', padx=ENTRIES_PADX,
                                          pady=(20,
                                                0))
        # Lines per Case Frame
        frame_lines = ttk.Frame(self.additiona_options_frame)
        frame_lines.pack(fill='x', padx=ENTRIES_PADX, pady=(15, 10))
        # Records per Case Entry
        self.entry_lines_label = Label(frame_lines,
                                           text="How many lines per case ? ("
                                                "1-10)")
        self.entry_lines_label.pack(side=ttk.LEFT)
        self.entry_lines = ttk.Entry(frame_lines, width=7)
        self.entry_lines.pack(side=ttk.RIGHT, padx=0)
        self.delimiter_label, self.entry_delimiter = \
            create_labeled_selection_box(
                self.additiona_options_frame,
                label_text="Is the data file delimited "
                     "by one of the delimiters in the "
                     "selection box? If yes, choose "
                     "the delimiter. If not, choose "
                     "None.", width=5, label_padx=ENTRIES_PADX, pady=10,
                values=AUTO_PARSING_DELIMITER_OPTIONS,
                default="None",
                wraplength=real_size(WINDOW_WIDTH - 200))
        self.fixed_width_label, self.selection_box_fixed_width = \
            create_labeled_selection_box(
                self.additiona_options_frame,
                label_text="Do all  variables "
                           f"have the same width? If yes, "
                           f"state the width ({DELIMITER_1_D},"
                           f" {DELIMITER_2_D})", width=5,
                label_padx=ENTRIES_PADX,
                pack=False,
                pady=10,
                values=FIXED_WIDTH_OPTIONS,
                default="No",
                wraplength=real_size(WINDOW_WIDTH - 200))

    #######################
    # getters and setters #
    #######################

    def is_manual_input(self):
        if self.additional_options and self.get_auto_parsing_format() is None:
            return True
        return False

    def set_delimiter(self, delimiter):
        self.entry_delimiter.set(delimiter)

    def set_fixed_width(self, width):
        self.selection_box_fixed_width.set(width)

    def set_entry_lines(self, lines: int):
        self.entry_lines.delete(0, ttk.END)
        self.entry_lines.insert(0, f"{lines}")

    def set_data_file_path(self, path):
        self.entry_data_file.delete(0, ttk.END)
        self.entry_data_file.insert(0, path)

    def set_missing_value(self, state : bool):
        if state != self.missing_value_var:
            self.checkbox_missing_value.invoke()

    def get_auto_parsing_format(self):
        """
        :return: the delimiter or the fixed width or None if the user didn't
        chose any auto-parsing format
        """
        delimiter = self.entry_delimiter.get()
        fixed_width = self.selection_box_fixed_width.get()
        if delimiter != AUTO_PARSING_DELIMITER_OPTIONS[0] and \
                fixed_width != FIXED_WIDTH_OPTIONS[0]:
            raise ValueError("You can't choose both delimiter and fixed width")
        if delimiter == "Space":
            return " "
        elif delimiter == "Tab":
            return "\t"
        elif delimiter == "Comma":
            return ","
        elif self.selection_box_fixed_width.get() == FIXED_WIDTH_OPTIONS[0]:
            return None
        return self.selection_box_fixed_width.get()

    def get_fixed_width(self):
        return self.selection_box_fixed_width.get()

    def default_entry_lines(self):
        self.set_entry_lines(1)

    def get_data_file_path(self):
        return self.entry_data_file.get()

    def get_lines_per_var(self):
        if self.entry_lines.get():
            return int(self.entry_lines.get())
        return 0

    def reset_entries(self):
        self.entry_data_file.delete(0, 'end')
        self.entry_lines.delete(0, 'end')
        self.entry_delimiter.delete(0, 'end')
        self.selection_box_fixed_width.current(0)
        self.selection_box_fixed_width.state(['!disabled'])
        self.entry_delimiter.state(['!disabled'])
        self.entry_lines.state(['!disabled'])
        if self.missing_value_var.get():
            self.checkbox_missing_value.invoke()

    ##################
    # Event Handlers #
    ##################

    def disable_additional_options(self):
        self.entry_delimiter.state(['disabled'])
        self.entry_lines.delete(0, ttk.END)
        self.entry_lines.state(['readonly'])
        self.selection_box_fixed_width.set("No")
        self.selection_box_fixed_width.state(['disabled'])
        for label in [self.entry_lines_label, self.delimiter_label,
                      self.fixed_width_label]:
            label.config(foreground="grey")
        self.additiona_options_frame.config(bootstyle="secondary")
        self.additional_options = False

    def enable_additional_options(self):
        self.entry_delimiter.state(['!disabled'])
        self.entry_lines.state(['!readonly'])
        self.selection_box_fixed_width.state(['!disabled'])
        for label in [self.entry_lines_label, self.delimiter_label,
                      self.fixed_width_label]:
            label.config(foreground="black")
        self.additiona_options_frame.config(bootstyle="primary")
        self.additional_options = True

    def enable_entry_lines(self):
        self.additiona_options_frame.config(bootstyle="primary")
        self.entry_lines.state(['!readonly'])
        self.entry_lines_label.config(foreground="black")
        self.entry_lines.delete(0, ttk.END)
        self.entry_lines.insert(0, "1")
        self.additional_options = True

    def browse_file(self):
        filetypes = [
            ("Data files", "*.dat;*.txt;*.prn;*.csv;*.xlsx;*.xls;*.tsv"),
            ("All files", "*.*")
        ]
        filename = filedialog.askopenfilename(
            title="Select Data File",
            filetypes=filetypes,
            initialdir="."  # Starts in current directory
        )
        if filename:
            self.entry_data_file.delete(0, ttk.END)
            self.entry_data_file.insert(0, filename)
        return filename
