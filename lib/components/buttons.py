from ttkbootstrap import Button

class DataButton(Button):
    """A button that can be used to navigate to a different page."""

    def __init__(self, parent, **kwargs):
        if 'width' not in kwargs:
            kwargs['width'] = 10
        super().__init__(parent, **kwargs,
                         bootstyle="dark", )


class NavigationButton(Button):
    """A button that can be used to navigate to a different page."""

    def __init__(self, parent, **kwargs):
        if 'width' not in kwargs:
            kwargs['width'] = 10
        super().__init__(parent, **kwargs,
                         bootstyle="primary", )
