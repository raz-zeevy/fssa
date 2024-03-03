from lib.controller.controller import *
from lib.controller.controller import Controller
from const import *


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
        self.test_simple_example()

    def test_simple_example(self):
        self.gui.pages[START_PAGE_NAME].button_recorded_data.invoke()
        # get the absoult path of the data file
        test_dir_path = os.path.dirname(os.path.abspath(__file__))
        data_file_path = os.path.join(test_dir_path,
                                      DATA_PATH)
        self.gui.pages[INPUT_PAGE_NAME].set_data_file_path(
            data_file_path)
        self.gui.pages[INPUT_PAGE_NAME].set_entry_lines(1)
        self.next_page()
        manual_page = self.gui.pages[MANUAL_FORMAT_PAGE_NAME]
        for _ in range(5):
            manual_page.add_variable()
        self.next_page()
        self.next_page()
        dims_page = self.gui.pages[DIMENSIONS_PAGE_NAME]
        dims_page.dimension_combo.current(1)
        dims_page.dimension_combo_selected(None)
        dims_page.set_dims(2,5)
        self.next_page()
        try:
            self.output_path = \
                r"C:\Users\Raz_Z\Projects\Shmuel\fssaDist\fssa\output" \
                r"\test_simple.fss"
            self.run_fss()
            self.enable_view_results()
        except Exception as e:
            # print(e)
            assert False
        run_file_path = p_FSS_DRV
        # true_file_path = os.path.join(test_dir_path, "FSSAINP.DRV")
        # # assert diff_lines_num(run_file_path, true_file_path) == 1
        # assert os.path.isfile(self.output_path)

if __name__ == '__main__':
    a = simple_example_gui()
    a.run_process()