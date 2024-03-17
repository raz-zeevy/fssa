import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from lib.utils import get_resource


class EditableTreeview(ttk.Treeview):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self._cur_focus = None
        self._cur_focus_col = None
        self._entry_popup = None
        # Load the unchecked checkbox image
        checkbox_off_image = Image.open(get_resource("checkbox_off.png"))
        checkbox_off_image = checkbox_off_image.resize((20, 20), Image.LANCZOS)
        self.checkbox_off_image = ImageTk.PhotoImage(checkbox_off_image)
        checkbox_on_image = Image.open(get_resource("checkbox_on.png"))
        checkbox_on_image = checkbox_on_image.resize((20, 20), Image.LANCZOS)
        self.checkbox_on_image = ImageTk.PhotoImage(checkbox_on_image)
        #
        self.checkboxes_states = {}
        self.bind("<Double-1>", self._on_double_click)
        self.bind("<Button-1>", self._on_click)
        self.bind("<ButtonRelease-1>", self._on_check_click)
        self.bind("<Motion>", self._on_motion)

    def _on_click(self, event):
        row_id = self.identify_row(event.y)
        column_id = self.identify_column(event.x)

        # Clear focus if clicking on a different row or column
        if row_id != self._cur_focus or column_id != self._cur_focus_col:
            if self._entry_popup:
                self._on_return(self._cur_focus,
                                            self._cur_focus_col,
                                self._entry_popup)
                self._entry_popup = None
            self._cur_focus = None
            self._cur_focus_col = None

    def _on_double_click(self, event):
        row_id = self.identify_row(event.y)
        column_id = self.identify_column(event.x)

        # Set focus and select the row
        self.selection_set(row_id)
        self._cur_focus = row_id
        self._cur_focus_col = column_id

        # Enter edit mode
        self._enter_edit_mode(row_id, column_id)

    def _enter_edit_mode(self, item_id, column_id):
        if self._cur_focus_col == "#0":  # Skip the first column with
            # checkboxes
            return
        self._entry_popup = tk.Entry(self)
        self._entry_popup.insert(0, self.item(item_id, 'values')[
            int(self._cur_focus_col[1:])-1])
        self._entry_popup.select_range(0, tk.END)
        self._entry_popup.bind("<Return>", lambda e: self._on_return(item_id,
                                                                     column_id,
                                                                     self._entry_popup))
        self._entry_popup.bind("<KP_Enter>", lambda e: self._on_return(item_id,
                                                                       column_id,
                                                                       self._entry_popup))
        self._entry_popup.bind("<Escape>", lambda e: self._entry_popup.destroy())
        self._entry_popup.bind("<FocusOut>", lambda e: self._entry_popup.destroy(
        ))  # Destroy the popup when focus is lost
        x, y, width, height = self.bbox(item_id, column_id)
        self._entry_popup.place(x=x, y=y, anchor="nw", width=width)

    def _on_return(self, item_id, column_id, entry_widget):
        self.set(item_id, column_id, entry_widget.get())
        entry_widget.destroy()

    def _on_check_click(self, event):
        row_id = self.identify_row(event.y)
        column_id = self.identify_column(event.x)
        # If the click is on the checkbox column and on a valid row
        if column_id == '#0' and row_id:
            # Toggle the checkbox state
            self.checkboxes_states[row_id] = not self.checkboxes_states.get(row_id, False)
            image = self.checkbox_on_image if self.checkboxes_states[row_id] else self.checkbox_off_image
            # Update the checkbox image
            self.item(row_id, image=image)

    def _on_motion(self, event):
        region = self.identify_region(event.x, event.y)
        if region == "tree":
            column_id = self.identify_column(event.x)
            if column_id == '#0':
                self.master.config(cursor="hand2")
            else:
                self.master.config(cursor="")
        else:
            self.master.config(cursor="")


# Setup root window
root = tk.Tk()
root.geometry("600x400")
main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True, padx=30)
# Scrollbars
vsb = ttk.Scrollbar(root, orient="vertical")
hsb = ttk.Scrollbar(root, orient="horizontal")

cols = ("Sel_Var", "Rec_N", "Field_Width",
                                    "Start_Col", "Label")

# Treeview table
tree = EditableTreeview(main_frame,
                        columns=cols,
                        displaycolumns="#all",
                        yscrollcommand=vsb.set,
                        xscrollcommand=hsb.set,
                        selectmode="browse")

# Configure scrollbars
vsb['command'] = tree.yview
hsb['command'] = tree.xview

# Configure treeview columns
tree.heading("#0", text="Var_No", anchor='w')
tree.heading("Sel_Var", text="Sel_Var")
tree.heading("Rec_N", text="Rec_N")
tree.heading("Field_Width", text="Field_Width")
tree.heading("Start_Col", text="Start_Col")
tree.heading("Label", text="Label")

# Add checkboxes as the first column
tree.column("#0", width=50, anchor='w')
for col in tree['columns']:
    tree.column(col, width=70, anchor='w')

for i in range(1, 20):
    iid = tree.insert('', 'end', text=f"", values=(f"v{i}", i, 1, 0,
                                                          f"Label {i}"))  # Set the initial checkbox image
    tree.item(iid, image=tree.checkbox_off_image, tags=('checkbox',))  # Set the initial
    # checkbox image
    tree.checkboxes_states[iid] = False  # Set the initial checkbox state

# Pack everything
vsb.place(x=30+500+2, y=95, height=200+20)
hsb.place(x=0, y=385, width=650)
tree.pack(side="left", fill="both", expand=False)

root.mainloop()
""