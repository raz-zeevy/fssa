from lib.controller.controller import *
from lib.controller.controller import Controller
from const import *

TEST_LABELS = [
    'v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'v7', 'v8', 'v9', 'v10', 'v11', 'v12',
    'v13', 'v14','v15', 'v16', 'v17', 'v18'
]

SET_MODE_TEST()
SIMPLE_DATA_PATH = r"simple\ACHIEVEMENT CORRELATIONS MATRIX.txt"
ACHMOT_DATA_PATH = r"achmot\ACHIVMAT.txt"


class MatrixTest(Controller):
    def __init__(self):
        super().__init__()
        self.gui.pages[START_PAGE_NAME].button_matrix_data.invoke()

    def test_simple_example(self):
        matrix_page = self.gui.pages[MATRIX_INPUT_PAGE_NAME]
        matrix_page.set_var_num(18)
        matrix_page.set_entries_num_in_row(18)
        matrix_page.set_field_width(4)
        matrix_page.set_decimal_places(0)
        matrix_page.set_missing_ranges([[99., 99.]] * 5)

        test_dir_path = os.path.dirname(os.path.abspath(__file__))
        data_file_path = os.path.join(test_dir_path,
                                      SIMPLE_DATA_PATH)
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
            self._run_matrix_fss()
            self.enable_view_results()
        except Exception as e:
            raise (e)
            assert False
        # run_file_path = p_FSS_DRV
        # true_file_path = os.path.join(test_dir_path, "FSSAINP.DRV")
        # # assert diff_lines_num(run_file_path, true_file_path) == 1
        # assert os.path.isfile(self.output_path)
   
    def test_achmot(self):
        test_facets = [
            ["a1","a2"], ["b1","b2", "b3"]
        ]
        facets_var = [[1, 2],
                      [1, 2],
                      [1, 3],
                      [2, 1],
                      [2, 2],
                      [2,3]]*3
        test_dir_path = os.path.dirname(os.path.abspath(__file__))
        self.reset_session(matrix=True)
        data_file_path = os.path.join(test_dir_path,
                                      ACHMOT_DATA_PATH)
        self.gui.pages[MATRIX_INPUT_PAGE_NAME].set_data_file_path(data_file_path)
        self.gui.pages[MATRIX_INPUT_PAGE_NAME].set_var_num(18)
        self.gui.pages[MATRIX_INPUT_PAGE_NAME].set_entries_num_in_row(18)
        self.gui.pages[MATRIX_INPUT_PAGE_NAME].set_field_width(4)
        self.gui.pages[MATRIX_INPUT_PAGE_NAME].set_decimal_places(0)
        self.gui.pages[MATRIX_INPUT_PAGE_NAME].set_missing_ranges([[99.5, 99.5]] * 5)
        self.next_page()
        self.next_page()
        self.gui.pages[DIMENSIONS_PAGE_NAME].set_dims(2,2)
        self.next_page()
        # The duplication is on purpose to avoid some bug with the on_facets_num_change
        self.gui.pages[FACET_PAGE_NAME].set_facets_details(test_facets)
        self.on_facet_num_change(None)
        self.gui.pages[FACET_PAGE_NAME].set_facets_details(test_facets)
        self.next_page()
        self.gui.pages[FACET_VAR_PAGE_NAME].set_facets_vars(facets_var)
        try:
            self.output_path = r'C:\Users\Raz_Z\Projects\Shmuel\fssaDist\fssa\tests\matrix_test\achmot\output\achmot.fss'
            self._run_matrix_fss()
            self.enable_view_results()
        except Exception as e:
            raise (e)
            assert False

if __name__ == '__main__':
    a = MatrixTest()
    # a.test_simple_example
    a.test_achmot()
    a.run_process()
