import ttkbootstrap as ttk
import tkinter as tk
from PIL import ImageTk, Image
from lib.utils import real_size
from lib.utils import get_resource


CALIBRI_FONT = ('Calibri', 10)
SEGOE_UI_FONT = ('Segoe UI', 9)


class Label(ttk.Label):
    """A label that can be used to display text."""

    def __init__(self, parent, **kwargs):
        if 'font' not in kwargs:
            kwargs['font'] = SEGOE_UI_FONT
        super().__init__(parent, **kwargs)


class DataButton(ttk.Button):
    """A button that can be used to navigate to a different page."""

    def __init__(self, parent, **kwargs):
        if 'width' not in kwargs:
            kwargs['width'] = 10
        super().__init__(parent, **kwargs,
                         bootstyle="dark", )


class NavigationButton(ttk.Button):
    """A button that can be used to navigate to a different page."""

    def __init__(self, parent, **kwargs):
        if 'width' not in kwargs:
            kwargs['width'] = 15
        if 'bootstyle' not in kwargs:
            kwargs['bootstyle'] = 'primary'
        super().__init__(parent, **kwargs)


class SelectionBox(ttk.Combobox):
    """A button that can be used to navigate to a different page."""

    def __init__(self, parent, **kwargs):
        default_index = None
        if 'default' in kwargs:
            default_index = kwargs['values'].index(kwargs['default'])
            del kwargs['default']
        if 'width' not in kwargs:
            kwargs['width'] = 10
        super().__init__(parent, **kwargs,
                         state="readonly", )
        self.values = kwargs['values']
        if default_index is not None:
            self.current(default_index)


def create_labeled_selection_box(master, label_text, values, default,
                                 width=10, label_padx=10, box_pad_x=0, pady=10,
                                 wraplength=real_size(500)):
    # Delimiter Frame
    frame = ttk.Frame(master)
    frame.pack(fill='x', padx=label_padx, pady=pady)
    # What is the delimiter Entry
    label = Label(frame,
                  text=label_text,
                  wraplength=wraplength)
    label.pack(side=ttk.LEFT)
    selection_box = SelectionBox(
        frame,
        values=values,
        default=default,
        width=width)
    selection_box.pack(side=ttk.RIGHT, padx=box_pad_x)
    return label, selection_box



class HelpButton(tk.Button):
    """
    Must be displayed on screen using the place method
    """
    img_path = get_resource("help.ico")
    img = None

    def __init__(self, parent, msg, **kwargs):
        if HelpButton.img is None:
            img = Image.open(HelpButton.img_path, "r").\
                resize(real_size((19,19),_round=True))
            HelpButton.img = ImageTk.PhotoImage(img)

        kwargs['text'] = "?"
        kwargs['image'] = self.img
        kwargs['autostyle'] = False
        kwargs['border'] = 0
        kwargs['background'] = 'white'
        kwargs['relief'] = 'sunken'
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.help_msg = msg
        self.bind("<Enter>", self.on_hover)


    def on_hover(self, event):
        """show a rectangle with the help message"""
        width = 200
        y_pad = 5
        background = '#FFFFDD'
        self.tooltip_frame = tk.Frame(self.parent,
                                      autostyle=False,
                                      background=background,
                                      relief='ridge',
                                      borderwidth=1)
        # place the tooldtip frame just below the button itself
        x, y = int(self.place_info()['x']), int(self.place_info()['y'])
        self.tooltip_frame.place(x=x-width+self.winfo_width(),
                                 y=y+self.winfo_height()+y_pad,
                                 anchor='nw',
                                 width=width)
        self.help_msg_box = ttk.Label(self.tooltip_frame,
                                      background=background,
                                      text=self.help_msg,
                                      wraplength=width,
                                      justify='left')
        self.help_msg_box.pack(expand=False, fill="x")
        self.unbind("<Enter>")
        self.bind("<Leave>", self.on_leave)

    def on_leave(self, event):
        """hide the help message"""
        self.tooltip_frame.destroy()
        self.bind("<Enter>", self.on_hover)

if __name__ == '__main__':
    # create a root and test the helpbutton
    root = ttk.Window(size=(400,400))
    root.title("Test Help Button")
    # set backgounrd green
    root.configure(background='green')
    main_frame = ttk.Frame(root)
    main_frame.pack(fill='both', expand=True)
    help_button = HelpButton(main_frame, "This is a test message")
    help_button.pack(side=ttk.RIGHT, padx=10, pady=10)
    root.mainloop()