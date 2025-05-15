from const import *

from lib.controller.controller import *
from lib.controller.controller import Controller
from lib.fss.fss_input_parser import *

# SET_MODE_TEST()
SET_MODE_PRODUCTION()
SAVE_PATH = (
    r"C:\Users\raz3z\Projects\Shmuel\fssaDist\fssa\tests\example_3"
    r"\save.mms"
)

###
test_facets = [
                ["figural", "verbal", "numeral", "social"],
                ["fluency", "flexibility", "orginality", "elaboration", "closure"],
                ["titles", "appropriateness"],
                ["creativity", "torrance"],
            ]

class example_3_gui(Controller):
    def __init__(self):
        super().__init__()

    def test_example_3(self):
        # get the absoult path of the data file
        self.gui.pages[START_PAGE_NAME].button_recorded_data.invoke()
        test_dir_path = os.path.dirname(os.path.abspath(__file__))
        data_file_path = os.path.join(test_dir_path,
                                      EX_3_DATA_PATH)
        self.gui.pages[INPUT_PAGE_NAME].set_data_file_path(
            data_file_path)
        self.gui.pages[INPUT_PAGE_NAME].checkbox_missing_value.invoke()
        self.gui.pages[INPUT_PAGE_NAME].set_entry_lines(4)
        self.gui.button_next.invoke()
        manual_page = self.gui.pages[MANUAL_FORMAT_PAGE_NAME]
        simulate_manual_format(EX_3_FORMAT_TXT, manual_page.add_variable,
                               labels=EX_3_LABELS_TXT,
                               missing_values_txt=EX_3_MISSING_VALUES_TXT)
        self.gui.button_next.invoke()
        self.gui.button_next.invoke()
        dims_page = self.gui.pages[DIMENSIONS_PAGE_NAME]
        dims_page.dimension_combo.current(1)
        dims_page.dimension_combo_selected(None)
        dims_page.set_dims(2,3)
        self.gui.button_next.invoke()
        facet_page = self.gui.pages[FACET_PAGE_NAME]
        facet_page.set_facets_num(4)
        self.on_facet_num_change(None)
        # just basic test
        facet_page.set_facets_details(test_facets)
        assert facet_page.get_facets_details() == test_facets
        facet_data = simulate_facets_details(EX_3_FACETS_TXT,
                                 facet_page.set_facets_details)
        assert facet_data == facet_page.get_facets_details()
        self.gui.button_next.invoke()
        simulate_facets_var_data(EX_3_FACETS_VAR_TXT,
                                 self.gui.pages[
            FACET_VAR_PAGE_NAME].combo_by_var)
        assert self.gui.pages[
                   FACET_VAR_PAGE_NAME].get_all_var_facets_indices_values()\
               == \
               parse_facets_var_data(EX_3_FACETS_VAR_TXT)
        self.gui.button_next.invoke()
        hypo_data = parse_hypotheses_per_facet(EX_3_HYPOTHESES_TXT)
        simulate_hypothesis(hypo_data.models,
                          self.gui.pages[
                              HYPOTHESIS_PAGE_NAME].models)
        assert self.gui.pages[
                   HYPOTHESIS_PAGE_NAME].get_hypotheses() \
               == \
                hypo_data.models
        self.gui.button_next.invoke()
        simulate_facets_dim(hypo_data.facets_dim,
                           self.gui.pages[
                               FACET_DIM_PAGE_NAME].facets_dim_check_buttons)
        assert self.gui.pages[
                   FACET_DIM_PAGE_NAME].get_facets_dim() \
               == \
                hypo_data.facets_dim
        try:
            self.output_path = (
                r"C:\Users\raz3z\Projects\Shmuel\fssaDist\fssa\output"
                r"\test_3_gui.fss"
            )
            self.run_fss(self._run_fss)
            self.enable_view_results()
        except Exception as e:
            print(e)
            raise(e)
        run_file_path = p_FSS_DRV
        true_file_path = os.path.join(test_dir_path, "FSSAINP.DRV")
        assert os.path.isfile(self.output_path)
        self.save_session(SAVE_PATH)

    def load(self):
        self.gui.pages[START_PAGE_NAME].button_recorded_data.invoke()
        # self.reset_session(False)
        self.load_session(SAVE_PATH)
        self.next_page()
        self.next_page()
        try:
            self.output_path = (
                r"C:\Users\raz3z\Projects\Shmuel\fssaDist\fssa\output"
                r"\test_3_gui.fss"
            )
            self.run_fss(self._run_fss)
            self.enable_view_results()
        except Exception as e:
            print(e)
            raise(e)

def test():
    a = example_3_gui()
    try:
        a.run_process()
    except Exception:
        return False
    return True


if __name__ == '__main__':
    ex_3 = example_3_gui()
    # ex_3.test_example_3()
    ex_3.load()
    ex_3.run_process()