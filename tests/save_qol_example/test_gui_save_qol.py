from const import *

from lib.controller.controller import *
from lib.controller.controller import Controller
from lib.fss.fss_input_parser import *

DATA_PATH = 'qolstu20.dat'
SET_MODE_TEST()
VARS_LABELS = [f"v{i}" for i in range(1,17)]
SAVE_PATH = (
    r"C:\Users\raz3z\Projects\Shmuel\fssaDist\fssa\tests"
    "\save_qol_example\sessions.mms"
)
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
        for _ in range(16):
            self.gui.pages[MANUAL_FORMAT_PAGE_NAME].add_variable()
        self.gui.pages[MANUAL_FORMAT_PAGE_NAME].set_labels(VARS_LABELS)
        self.next_page()
        self.next_page()
        self.next_page()
        self.gui.pages[
            FACET_PAGE_NAME].set_facets_num(2)
        self.on_facet_num_change(None)
        simulate_facets_details(FACET_VALUES, self.gui.pages[
            FACET_PAGE_NAME].set_facets_details)
        self.next_page()
        simulate_facets_var_data(FACET_VAR_DATA,
                        self.gui.pages[FACET_VAR_PAGE_NAME].combo_by_var)
        try:
            self.output_path = (
                r"C:\Users\raz3z\Projects\Shmuel\fssaDist\fssa\output"
                r"\_sqol_pakam_students.fss"
            )
            self.run_fss(self._run_fss)
            self.enable_view_results()
        except Exception as e:
            print(e)
            raise(e)
        assert os.path.isfile(self.output_path)
        [self.previous_page() for _ in range(3)]
        self.save_session_click(SAVE_PATH)

    def test_load(self):
        self.load_session(SAVE_PATH)
        assert (
            self.gui.pages[INPUT_PAGE_NAME].get_data_file_path()
            == r"C:\Users\raz3z\Projects\Shmuel\fssaDist\fssa\tests\save_qol_example\qolstu20.dat"
        )
        assert self.gui.pages[INPUT_PAGE_NAME].get_lines_per_var() == 1
        assert self.gui.pages[MANUAL_FORMAT_PAGE_NAME].get_labels() == VARS_LABELS
        assert self.gui.pages[FACET_PAGE_NAME].get_facets_num() == 2

if __name__ == '__main__':
    a = simple_example_gui()
    a.test_simple_example()
    a.test_load()
    a.run_process()
