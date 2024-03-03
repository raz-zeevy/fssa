from lib.controller.controller import *
from lib.controller.controller import Controller
from const import *
from lib.utils import *
SET_MODE_TEST()

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
        self.test_simple_example()

    def test_simple_example(self):
        self.gui.pages[START_PAGE_NAME].button_recorded_data.invoke()
        # get the absoult path of the data file
        test_dir_path = os.path.dirname(os.path.abspath(__file__))
        data_file_path = os.path.join(test_dir_path,
                                      DATA_PATH)
        self.gui.pages[INPUT_PAGE_NAME].set_data_file_path(
            data_file_path)
        self.gui.pages[INPUT_PAGE_NAME].set_delimiter('Comma')
        self.gui.pages[INPUT_PAGE_NAME].set_entry_lines(1)
        self.next_page()
        self.gui.pages[DATA_PAGE_NAME].button_recode.invoke()
        self.gui.recode_window.set_grouping(9)
        self.gui.recode_window.set_indices("1-5")
        self.gui.recode_window.button_recode.invoke()
        self.gui.pages[DATA_PAGE_NAME].button_recode.invoke()
        self.gui.recode_window.set_grouping_type(GROUPING_TYPES[1])
        self.gui.recode_window.set_grouping(2)
        self.gui.recode_window.set_indices("1-5")
        self.gui.recode_window.set_grouping_type(GROUPING_TYPES[1])
        self.gui.recode_window.button_recode.invoke()
        self.gui.pages[DATA_PAGE_NAME].button_recode.invoke()
        self.gui.recode_window.set_grouping(0)
        self.gui.recode_window.set_indices("5")
        self.gui.recode_window.set_inverting(True)
        self.gui.recode_window.button_recode.invoke()
        self.next_page()
        self.next_page()
        try:
            self.output_path = \
                r"C:\Users\Raz_Z\Projects\Shmuel\fssaDist\fssa\output" \
                r"\test_recording_simple.fss"
            self.run_fss()
            self.enable_view_results()
        except Exception as e:
            # print(e)
            assert False
        assert os.path.isfile(self.output_path)

if __name__ == '__main__':
    a = simple_example_gui()
    a.run_process()