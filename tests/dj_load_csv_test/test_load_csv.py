"""
The purpose of this test is to test the GUI with a real csv file that
contains:
- Missing values
- Different types of variables, some of them are numerical and some aren't
- numerical variables that need recoding
"""

from lib.controller.controller import *
from lib.controller.controller import Controller
from lib.fss.fss_input_parser import *
from lib.utils import *
from const import *


DATA_PATH = 'data.csv'
SET_MODE_TEST()
# SET_MODE_PRODUCTION()
save_path= r"C:\Users\Raz_Z\Projects\Shmuel\fssaDist\fssa\tests" \
           r"\dj_load_csv_test\dj_test_all.mms"
facets_var_indices = {2: [1, 2], 3: [1, 1], 4: [1, 2], 5: [1, 1], 6: [1, 2], 7: [1, 1], 8: [1, 2], 9: [1, 1], 10: [1, 2], 11: [2, 1], 12: [1, 2], 13: [1, 1], 14: [2, 2], 15: [1, 1], 16: [1, 2], 17: [2, 1], 18: [1, 2], 19: [1, 1], 20: [2, 2]}

class simple_example_gui(Controller):
    def __init__(self):
        super().__init__()
        self.test_simple_example()

    def test_simple_example(self):
        self.gui.pages[START_PAGE_NAME].button_recorded_data.invoke()
        self.load_session(save_path)
        self.next_page()
        self.next_page()
        manual_page = self.gui.pages[MANUAL_FORMAT_PAGE_NAME]
        print(manual_page.get_labels())
        self.next_page()
        try:
            self.output_path = \
                r"C:\Users\Raz_Z\Projects\Shmuel\fssaDist\fssa\tests\dj_csv_test\output\jd_test.fss"
            self.run_fss()
            self.enable_view_results()
        except Exception as e:
            print(e)
            raise (e)
        cur_fvi = self.gui.pages[FACET_VAR_PAGE_NAME].get_all_var_facets_indices()
        assert cur_fvi == facets_var_indices
#
if __name__ == '__main__':
    a = simple_example_gui()
    a.run_process()