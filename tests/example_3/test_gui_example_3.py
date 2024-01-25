from lib.controller import *
from lib.controller import Controller
from lib.fss.fss_parsers import *
from tests.tests_utils import *
from const import *
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
        self.test_example_3()

    def test_example_3(self):
        # get the absoult path of the data file
        test_dir_path = os.path.dirname(os.path.abspath(__file__))
        data_file_path = os.path.join(test_dir_path,
                                      EX_3_DATA_PATH)
        self.gui.pages[START_PAGE_NAME].set_data_file_path(
            data_file_path)
        self.gui.pages[START_PAGE_NAME].set_entry_lines(4)
        self.gui.pages[START_PAGE_NAME].button_manual_input.state([
            "!disabled"])
        self.gui.pages[START_PAGE_NAME].button_manual_input.invoke()
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
                   FACET_VAR_PAGE_NAME].get_all_var_facets_indices()\
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
            self.output_path = \
                r"C:\Users\Raz_Z\Projects\Shmuel\fssa\output" \
                r"\test_3_gui.fss"
            self.run_fss()
        except Exception as e:
            print(e)
            assert False
        run_file_path = p_FSS_DRV
        true_file_path = os.path.join(test_dir_path, "FSSAINP.DRV")
        assert diff_lines_num(run_file_path, true_file_path) == 1
        assert os.path.isfile(self.output_path)

if __name__ == '__main__':
    a = example_3_gui()
    a.run_process()