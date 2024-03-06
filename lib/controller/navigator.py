from lib.gui import GUI
from lib.utils import *

class Navigator():
    class Page():
        def __init__(self, name, show=True):
            self.name: str = name
            self.show: bool = show

    def __init__(self, gui : GUI):
        self.pages_list = [Navigator.Page(page_name) for page_name in
                           gui.pages]
        self.index: int = 0
        self.gui = gui

    def append_page(self, page_name):
        self.pages_list.append(page_name)

    def pop_page(self, index=None):
        return self.pages_list.pop(index)

    ######
    def set_page(self, page_name: str):
        self.index = self.get_index(page_name)
        # menu enabling and disabling
        self.update_menu()

    def update_menu(self):
        if self.index < self.get_index(DATA_PAGE_NAME):
            self.gui.FSSA_menu.entryconfig("Dimensions & Coeffs",
                                           state="disabled")
            self.gui.menu_bar.entryconfig("Facet", state="disabled")
        else:
            self.gui.FSSA_menu.entryconfig("Dimensions & Coeffs",
                                           state="normal")
            self.gui.menu_bar.entryconfig("Facet", state="normal")
        try:
            if self.index >= self.get_index(DATA_PAGE_NAME) and self.get_page(
                DATA_PAGE_NAME).show:
                self.gui.input_data_menu.entryconfig("Data", state="normal")
            else:
                self.gui.input_data_menu.entryconfig("Data", state="disabled")
        except: pass
        if self.get_page(MANUAL_FORMAT_PAGE_NAME).show:
            self.gui.input_data_menu.entryconfig('Variables', state="normal")
        else:
            self.gui.input_data_menu.entryconfig('Variables', state="disabled")
        for page in [(FACET_PAGE_NAME, "Element Labels"), (FACET_VAR_PAGE_NAME,
                                                   "Variable Elements"),
                     (HYPOTHESIS_PAGE_NAME, "Hypotheses"),
                     (FACET_DIM_PAGE_NAME, "Diagrams")]:
            if self.get_page(page[0]).show:
                self.gui.facet_menu.entryconfig(page[1], state="normal")
            else:
                self.gui.facet_menu.entryconfig(page[1], state="disabled")

    ######

    def get_next(self) -> str:
        if self.index == len(self.pages_list):
            return None
        for i in range(self.index + 1, len(self.pages_list)):
            if self.pages_list[i].show:
                return self.pages_list[i].name

    def get_current(self) -> str:
        for i in range(self.index, len(self.pages_list)):
            if self.pages_list[i].show:
                return self.pages_list[i].name

    def get_prev(self) -> str:
        if self.index == 0:
            return None
        for i in range(self.index - 1, -1, -1):
            if self.pages_list[i].show:
                return self.pages_list[i].name

    ######

    def hide_page(self, name: str):
        index = self.find(name)
        if index is None:
            raise Exception(
                "Usage Error:\nCan't hide page that doesn't exist")
        self.pages_list[index].show = False

    def show_page(self, name: str):
        index = self.find(name)
        if index is None:
            raise Exception(
                "Usage Error:\nCan't show page that doesn't exist")
        self.pages_list[index].show = True

    def add_block(self, name: str):
        index = self.get_index(name)
        for i in range(index + 1, len(self.pages_list)):
            self.pages_list[i].show = False

    def remove_block(self, name: str):
        index = self.get_index(name)
        for i in range(index + 1, len(self.pages_list)):
            self.pages_list[i].show = True

    ######
    def get_index(self, name):
        for i, page in enumerate(self.pages_list):
            if page.name == name:
                return i
        raise Exception(
            "Usage Error:\n Can't get index of page that doesn't exist")

    def find(self, name):
        for i, page in enumerate(self.pages_list):
            if page.name == name:
                return i

    def get_page(self, name):
        return self.pages_list[self.get_index(name)]