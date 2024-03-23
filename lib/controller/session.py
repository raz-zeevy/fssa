import jsonpickle
import pandas as pd

from lib.utils import *

class Session:
    def __init__(self, controller=None, path=None):
        if controller:
            controller = controller
            self.state = self._attributes_from_controller(controller)
        elif path:
            self.state = self._attributes_from_save(path)
        else:
            raise ValueError('Either controller or path must be provided')

    def _attributes_from_controller(self, controller):
        controller.init_fss_attributes()
        controller_dict = controller.__dict__.copy()
        for key in ['gui', 'keyboard', ]:
            controller_dict.pop(key, None)
        controller_dict['navigator'] = controller_dict['navigator'].__dict__.copy()
        for key in ['gui']:
            controller_dict['navigator'].pop(key, None)
        return controller_dict

    def _attributes_from_save(self, path):
        with open(path, 'r') as file:
            attributes = jsonpickle.decode(file.read())
        return attributes

    def save(self, path):
        json_string = jsonpickle.encode(self.state, indent=2)
        with open(path, 'w') as file:
            file.write(json_string)

    def load_to_controller(self, controller):
        state = self.state
        controller.reset_session(state['matrix_input'])
        for key, value in state.items():
            if key in ['navigator']:
                continue
            setattr(controller, key, value)
        if state['matrix_input']:
            #   Matrix Input Page
            matrix_page = controller.gui.pages[MATRIX_INPUT_PAGE_NAME]
            matrix_page.set_data_file_path(state["data_file_path"])
            # set matrix details
            details = state["matrix_details"]
            matrix_page.set_var_num(details["var_num"])
            matrix_page.set_entries_num_in_row(details["entries_num_in_row"])
            matrix_page.set_field_width(details["field_width"])
            matrix_page.set_decimal_places(details["decimal_places"])
            matrix_page.set_missing_ranges(details["missing_ranges"])
            controller.next_page()
            #
            controller.gui.button_next.invoke()
            #   Manual Format Page
            manual_page = controller.gui.pages[MANUAL_FORMAT_PAGE_NAME]
            manual_page.set_labels(state["var_labels"])
            controller.next_page()
        else:
            # Input Page
            input_page = controller.gui.pages[INPUT_PAGE_NAME]
            if state["data_file_path"]:
                input_page.set_data_file_path(state["data_file_path"])
            if state["lines_per_var"]:
                input_page.set_entry_lines(state["lines_per_var"])
            if state["additional_options"]:
                if state["fixed_width"] != "No":
                    input_page.set_fixed_width(state["fixed_width"])
                elif state["delimiter"]:
                    input_page.set_delimiter(state["delimiter"])
            if state["manual_input"]:
                controller.next_page()
                #   Manual Format Page
                manual_page = controller.gui.pages[MANUAL_FORMAT_PAGE_NAME]
                for var in state["manual_format_details"]:
                    manual_page.add_variable(**var)
            #   Data Page
            if not state["fss_data"]: return
            controller.next_page()
            data_page = controller.gui.pages[DATA_PAGE_NAME]
            data = pd.DataFrame(state["fss_data"], columns=state["var_labels"])
            data_page.show_data(data)
        #   Dimension Page
        if not state["max_dim"]: return
        controller.next_page()
        dims_page = controller.gui.pages[DIMENSIONS_PAGE_NAME]
        dim_range = state["max_dim"] > state["min_dim"]
        dims_page.dimension_combo.current(dim_range)
        dims_page.dimension_combo_selected(None)
        dims_page.set_dims(state["min_dim"], state["max_dim"])
        dims_page.set_correlation_type(state["correlation_type"])
        #   Facet Page
        controller.next_page()
        facet_page = controller.gui.pages[FACET_PAGE_NAME]
        facet_page.set_facets_num(state["facets_num"])
        controller.on_facet_num_change(None)
        facet_page.set_facets_details(state["facet_details"])
        controller.load_facet_var_page()
        controller.load_hypothesis_page()
        controller.load_facet_dim_page()
        #   Facet Var Page
        if not state["facet_details"]: return
        controller.next_page()
        facet_var_page = controller.gui.pages[FACET_VAR_PAGE_NAME]
        facet_var_page.set_facets_vars(state["facet_var_details"])
        controller.next_page()
        #   Hypothesis Page
        hypothesis_page = controller.gui.pages[HYPOTHESIS_PAGE_NAME]
        hypothesis_page.set_hypotheses(state["hypotheses_details"])
        controller.next_page()
        #   Facet Dim Page
        facet_dim_page = controller.gui.pages[FACET_DIM_PAGE_NAME]
        facet_dim_page.set_facets_dim(state["facet_dim_details"])
        # revert to current page
        while controller.navigator.get_current() != state['navigator']['pages_list'][state['navigator']['index']].name:
            controller.previous_page()
        print("done")



