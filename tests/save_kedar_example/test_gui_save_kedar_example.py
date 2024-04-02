"""
this file is a test for the kedar example which contains:
- bad line that str omitted from the data (with no warning)
- lines not in the same length so variables should be selected
"""

from lib.controller.controller import *
from lib.controller.controller import Controller

DATA_PATH = 'DJKEDAR2.DAT'
# SET_MODE_PRODUCTION()
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


    def test_simple_example(self):
        self.gui.pages[START_PAGE_NAME].button_recorded_data.invoke()
        # get the absoult path of the data file
        test_dir_path = os.path.dirname(os.path.abspath(__file__))
        data_file_path = os.path.join(test_dir_path,
                                      DATA_PATH)
        self.gui.pages[INPUT_PAGE_NAME].set_data_file_path(
            data_file_path)
        self.gui.pages[INPUT_PAGE_NAME].set_entry_lines(1)
        self.gui.pages[INPUT_PAGE_NAME].set_fixed_width("1-digit")
        self.next_page()
        self.next_page()
        self.gui.pages[DATA_PAGE_NAME].select_variables({i for i in range(1,
                                                                          26)})
        self.next_page()
        self.gui.pages[DIMENSIONS_PAGE_NAME].set_dims(2,3)
        self.next_page()
        self.gui.pages[FACET_PAGE_NAME].set_facets_num(2)
        self.on_facet_num_change(None)
        self.next_page()
        facets_var = [[1,2],[2,1],[1,2],[2,1],[1,2]]*5
        self.gui.pages[FACET_VAR_PAGE_NAME].set_facets_vars(facets_var)
        self.next_page()
        self.next_page()
        try:
            self.output_path = \
                r"C:\Users\Raz_Z\Projects\Shmuel\fssaDist\fssa\output" \
                r"\test_kedar.fss"
            self.run_fss()
            self.enable_view_results()
        except Exception as e:
            print(e)
            raise(e)
        assert os.path.isfile(self.output_path)
        self.save_session('sessions.mem')

    def test_load(self):
        self.load_session('sessions.mem')

if __name__ == '__main__':
    a = simple_example_gui()
    a.test_simple_example()
    # a.test_load()
    a.run_process()