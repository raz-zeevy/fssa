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
        for key in ['gui', 'keyboard', 'navigator', 'history']:
            controller_dict.pop(key, None)
        controller_dict['data'] = []
        controller_dict['fss_data'] = []
        return controller_dict

    def _attributes_from_save(self, path):
        with open(path, 'r') as file:
            attributes = jsonpickle.decode(file.read())
        return attributes

    def save(self, path):
        json_string = jsonpickle.encode(self.state, indent=2)
        with open(path, 'w') as file:
            file.write(json_string)

    def load_to_controller_attributes(self, controller):
        state = self.state
        controller.has_header = state.get('has_header')
        controller.are_missing_values = state.get('are_missing_values')
        controller.update_save_path(state['save_path'])

    def load_to_controller(self, controller):
        state = self.state
        controller.reset_session(state['matrix_input'])
        self.load_to_controller_attributes(controller)
        gui = controller.gui
        controller.active_variables_details = state['active_variables_details']
        for key, value in state.items():
            if key in ['navigator']:
                continue
            setattr(controller, key, value)
        manual_page = controller.gui.pages[MANUAL_FORMAT_PAGE_NAME]
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
            # controller.next_page()
            #
            controller.gui.button_next.invoke()
            #   Manual Format Page
            manual_page.set_labels(state["var_labels"])
            # controller.next_page()
        else:
            # Input Page
            input_page = controller.gui.pages[INPUT_PAGE_NAME]
            if state["data_file_path"]:
                input_page.set_data_file_path(state["data_file_path"])
            controller.set_header(state["has_header"])
            controller._suggest_parsing(interactive=False)
            if state["lines_per_var"]:
                input_page.set_entry_lines(state["lines_per_var"])
            if self.state['are_missing_values']:
                input_page.checkbox_missing_value.invoke()
            if state["additional_options"]:
                if state["fixed_width"] != "No":
                    input_page.set_fixed_width(state["fixed_width"])
                elif state["delimiter"]:
                    input_page.set_delimiter(state["delimiter"])
            if state["manual_input"]:
                # controller.next_page()
                #   Manual Format Page
                for var in state["manual_format_details"]:
                    manual_page.add_variable(**var)
            else:
                for i, var in enumerate(controller.active_variables_details):
                    if not var['remove']:
                        manual_page.add_variable(label=var['label'],
                                                 var_i=var['index'])
                        if not var['show']:
                            manual_page.data_table.toggle_row(
                                -1)
                manual_page.set_variables_nums(manual_page.vars_i)
        dims_page = controller.gui.pages[DIMENSIONS_PAGE_NAME]
        if state['max_dim']:
            dim_range = state["max_dim"] > state["min_dim"]
            dims_page.dimension_combo.current(dim_range)
            dims_page.dimension_combo_selected(None)
            dims_page.set_dims(state["min_dim"], state["max_dim"])
        dims_page.set_correlation_type(state["correlation_type"])
        # #   Facet Page
        facet_page = controller.gui.pages[FACET_PAGE_NAME]
        facet_page.set_facets_num(state["facets_num"])
        controller.on_facet_num_change(None)
        facet_page.set_facets_details(state["facet_details"])
        # #   Facet Var Page
        if not state["facet_details"]: return
        facet_var_page = controller.gui.pages[FACET_VAR_PAGE_NAME]
        controller.load_facet_var_page()
        facet_var_page.set_facets_var_from_active(
            state['active_variables_details'])
        controller.load_hypothesis_page()
        controller.load_facet_dim_page()
        # #   Hypothesis Page
        hypothesis_page = controller.gui.pages[HYPOTHESIS_PAGE_NAME]
        hypothesis_page.set_hypotheses(state["hypotheses_details"])
        # controller.next_page()
        # #   Facet Dim Page
        facet_dim_page = controller.gui.pages[FACET_DIM_PAGE_NAME]
        facet_dim_page.set_facets_dim(state["facet_dim_details"])
        controller.active_variables_details = state['active_variables_details']
