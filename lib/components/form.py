import ttkbootstrap as ttk

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
            kwargs['width'] = 10
        super().__init__(parent, **kwargs,
                         bootstyle="primary", )


class SelectionBox(ttk.Combobox):
    """A button that can be used to navigate to a different page."""

    def __init__(self, parent, **kwargs):
        default_index = None
        if 'default' in kwargs:
            default_index = kwargs['default'].index(kwargs['default'])
            del kwargs['default']
        super().__init__(parent, **kwargs,
                         state="readonly",)
        self.values = kwargs['values']
        if default_index is not None:
            self.current(default_index)