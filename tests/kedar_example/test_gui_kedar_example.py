"""
this file is a test for the kedar example which contains:
- bad line that str omitted from the data (with no warning)
- lines not in the same length so variables should be selected
"""

from lib.controller.controller import *
from lib.controller.controller import Controller

DATA_PATH = 'DJKEDAR2_FIXED.DAT'
F_DATA_PATH = 'DJKEDAR2.DAT'
SET_MODE_PRODUCTION()

###
test_facets = [
    ["figural", "verbal", "numeral", "social"],
    ["fluency", "flexibility", "orginality", "elaboration", "closure"],
    ["titles", "appropriateness"],
    ["creativity", "torrance"],
]


class simple_example_gui(Controller):
    def __init__(self):
        super().__init__()

    def test_fixed_data(self):
        self.gui.pages[START_PAGE_NAME].button_recorded_data.invoke()
        # get the absoult path of the data file
        test_dir_path = os.path.dirname(os.path.abspath(__file__))
        data_file_path = os.path.join(test_dir_path,
                                      DATA_PATH)
        self._suggest_parsing(interactive=False)
        self.gui.pages[INPUT_PAGE_NAME].set_data_file_path(
            data_file_path)
        self.gui.pages[INPUT_PAGE_NAME].set_entry_lines(1)
        self.next_page()
        for _ in range(25):
            self.gui.pages[MANUAL_FORMAT_PAGE_NAME].add_variable()
        self.next_page()
        self.next_page()
        self.gui.pages[DIMENSIONS_PAGE_NAME].set_dims(2, 3)
        self.next_page()
        self.gui.pages[FACET_PAGE_NAME].set_facets_num(2)
        self.on_facet_num_change(None)
        self.next_page()
        facets_var = [[1, 2], [2, 1], [1, 2], [2, 1], [1, 2]] * 5
        self.gui.pages[FACET_VAR_PAGE_NAME].set_facets_vars(facets_var)
        self.next_page()
        self.next_page()
        try:
            self.output_path = \
                r"C:\Users\Raz_Z\Projects\Shmuel\fssaDist\fssa\output" \
                r"\test_kedar.fss"
            self.run_fss(self._run_fss)
            self.enable_view_results()
        except Exception as e:
            print(e)
            raise (e)
        assert os.path.isfile(self.output_path)

    def test_fault_data(self):
        self.gui.pages[START_PAGE_NAME].button_recorded_data.invoke()
        # self.reset_session(False)
        # get the absoult path of the data file
        test_dir_path = os.path.dirname(os.path.abspath(__file__))
        data_file_path = os.path.join(test_dir_path,
                                      F_DATA_PATH)
        self._suggest_parsing(interactive=False)
        self.gui.pages[INPUT_PAGE_NAME].set_data_file_path(
            data_file_path)
        self.gui.pages[INPUT_PAGE_NAME].set_entry_lines(1)
        self.next_page()
        for _ in range(25):
            self.gui.pages[MANUAL_FORMAT_PAGE_NAME].add_variable()
        self.next_page()
        self.next_page()


def test():
    a = simple_example_gui()
    try:
        a.test_fixed_data()
    except Exception as e:
        return False
    return True


if __name__ == '__main__':
    a = simple_example_gui()
    # a.test_fixed_data()
    a.test_fault_data()
    a.run_process()
