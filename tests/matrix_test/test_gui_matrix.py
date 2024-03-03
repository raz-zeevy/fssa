from lib.controller.controller import *
from lib.controller.controller import Controller
from const import *

TEST_LABELS = [
    'v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'v7', 'v8', 'v9', 'v10', 'v11', 'v12',
    'v13', 'v14','v15', 'v16', 'v17', 'v18'
]

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
        # get the absoult path of the data file
        self.gui.pages[START_PAGE_NAME].button_matrix_data.invoke()
        #
        matrix_page = self.gui.pages[MATRIX_INPUT_PAGE_NAME]
        matrix_page.set_var_num(18)
        matrix_page.set_entries_num_in_row(18)
        matrix_page.set_field_width(4)
        matrix_page.set_decimal_places(0)
        matrix_page.set_missing_ranges([[99., 99.]] * 5)

        test_dir_path = os.path.dirname(os.path.abspath(__file__))
        data_file_path = os.path.join(test_dir_path,
                                      DATA_PATH)
        matrix_page.set_data_file_path(
            data_file_path)
        self.gui.button_next.invoke()
        self.gui.pages[MANUAL_FORMAT_PAGE_NAME].set_labels(TEST_LABELS)
        self.next_page()
        dims_page = self.gui.pages[DIMENSIONS_PAGE_NAME]
        dims_page.dimension_combo.current(1)
        dims_page.dimension_combo_selected(None)
        dims_page.set_dims(2,5)
        self.next_page()
        try:
            self.output_path = \
                r"C:\Users\Raz_Z\Projects\Shmuel\fssaDist\fssa\output" \
                r"\achieement_18_vars.fss"
            self.run_matrix_fss()
            self.enable_view_results()
        except Exception as e:
            raise (e)
            assert False
        # run_file_path = p_FSS_DRV
        # true_file_path = os.path.join(test_dir_path, "FSSAINP.DRV")
        # # assert diff_lines_num(run_file_path, true_file_path) == 1
        # assert os.path.isfile(self.output_path)


if __name__ == '__main__':
    a = simple_example_gui()
    a.run_process()
