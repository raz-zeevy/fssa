import os
import shutil
from pathlib import Path
from tkinter import ttk

import pytest
from lib.utils import p_FSS_DRV
from lib.controller.controller import Controller
from lib.utils import SET_MODE_TEST, SET_MODE_PRODUCTION, MATRIX_INPUT_PAGE_NAME


@pytest.fixture
def visual_mode():
    """Fixture to control whether tests run in visual mode or not"""
    return os.getenv("VISUAL_MODE", "false").lower() == "true"


class TestScenarios:
    """Test class for running full POSAC scenarios"""

    @classmethod
    def setup_class(cls):
        """Create a single controller instance for all tests"""
        cls.controller = Controller()
        SET_MODE_TEST()  # Add this to prevent GUI issues during tests
        cls.controller.start_fss(matrix=False)

    @classmethod
    def teardown_class(cls):
        """Clean up after all tests are done"""
        if hasattr(cls, "controller"):
            cls.controller.gui.root.destroy()
            cls.controller.gui.root.quit()

    @pytest.fixture(autouse=True)
    def setup(self, visual_mode):
        """Reset state between tests"""
        # Reset to clean state for each test
        if not visual_mode:
            # Just reset attributes without calling problematic methods
            self.controller.init_controller_attributes()
            # Reset GUI state
            self.controller.gui.reset()
        else:
            # In visual mode, just do minimal reset to avoid button_run issues
            self.controller.init_controller_attributes()
        yield

    def get_drv_lines(self):
        # get from p_FSS_DRV
        with open(p_FSS_DRV, "r") as file:
            return file.readlines()

    def _setup_visual_test(self):
        """Setup visual testing environment with Done button and instructions"""

        def on_done():
            buttons_frame.destroy()
            self.controller.gui.root.quit()

        def on_open_run_dir():
            from lib.fss.fss_module import open_fss_files_dir

            open_fss_files_dir()

        buttons_frame = ttk.Frame(self.controller.gui.root)
        buttons_frame.pack(side="bottom", pady=10)
        done_button = ttk.Button(buttons_frame, text="Done Testing", command=on_done)
        done_button.pack(side="left", padx=3)

        open_run_dir_button = ttk.Button(
            buttons_frame, text="Open Run Directory", command=on_open_run_dir
        )
        open_run_dir_button.pack(side="left", padx=3)
        self.controller.gui.root.mainloop()

    def _save_session(self, test_dir: Path):
        """Save the current session to a file in the test directory"""
        session_file = test_dir / "session.fss"
        self.controller.save_session(str(session_file))

    def run_djmatsq_scenario(self):
        """Run the djmatsq scenario test"""
        # Reset session for matrix mode
        self.controller.reset_session(matrix=True)

        # Load the djmatsq test data
        djmatsq_dir = Path(os.path.abspath("tests/djmatSQ"))
        djmatsq_file = djmatsq_dir / "djmatSQ.txt"

        assert djmatsq_file.exists(), "DJMatSQ test data not found"

        # Set the matrix data file path
        matrix_page = self.controller.gui.pages[MATRIX_INPUT_PAGE_NAME]
        matrix_page.set_data_file_path(str(djmatsq_file))

        # Set matrix details (21x21 matrix, standard format)
        matrix_page.set_var_num(21)
        matrix_page.set_entries_num_in_row(21)
        matrix_page.set_field_width(4)
        matrix_page.set_decimal_places(0)

        # Navigate to the next page to continue with the scenario
        self.controller.next_page()
        self.controller.next_page()
        self.controller.next_page()
        self.controller.output_path = str(djmatsq_file).replace(".txt", ".fss")
        self.controller.run_fss(self.controller._run_matrix_fss)
        self.controller.enable_view_results()
        assert os.path.isfile(self.controller.output_path)
        self._save_session(djmatsq_dir)

    def run_real_csv_test_scenario(self):
        """Run the real CSV test scenario with recoding and facets"""
        # Reset session for recorded data mode
        self.controller.reset_session(matrix=False)

        # Load the real CSV test data
        real_csv_dir = Path(os.path.abspath("tests/real_csv_test"))
        data_file = real_csv_dir / "data.csv"

        assert data_file.exists(), "Real CSV test data not found"

        # Set up CSV input data with headers
        input_page = self.controller.gui.pages["InputPage"]
        input_page.set_data_file_path(str(data_file))
        self.controller.set_header(True)
        self.controller.data_file_extension = ".csv"
        self.controller.load_csv_init()
        input_page.disable_additional_options()

        # Move to manual format page
        self.controller.next_page()

        # Select variables 3-21 (Q3 through Gender)
        manual_page = self.controller.gui.pages["ManualFormatPage"]
        manual_page.select_variables_window({i for i in range(3, 21)})

        # Move to data page
        self.controller.next_page()

        # Run recoding operations
        self._run_recoding_operations()

        # Move to dimensions page
        self.controller.next_page()

        # Move to facets page (using default dimensions)
        self.controller.next_page()

        # Set output path and run initial analysis
        output_file = real_csv_dir / "real_csv.fss"
        self.controller.output_path = str(output_file)
        self.controller.run_fss(self.controller._run_fss)
        self.controller.enable_view_results()

        # Verify output file was created
        assert os.path.isfile(self.controller.output_path), f"Output file not created: {self.controller.output_path}"

        # Test facet functionality
        facet_page = self.controller.gui.pages["FacetPage"]
        facet_page.set_facets_num(1)
        self.controller.on_facet_num_change(None)

        # Move to facet variables page
        self.controller.next_page()

        # Set facet variables
        facet_var_page = self.controller.gui.pages["FacetVarPage"]
        facet_var_page.set_facets_vars([[1], [2], [1], [2], [1], [2], [1], [2], [1], [2], [1], [2], [1], [2], [1], [2], [1], [2], [1], [2]])

        # Test session save/load functionality
        session_file = real_csv_dir / "mms" / "facet_1.mms"
        session_file.parent.mkdir(exist_ok=True)
        self.controller.save_session(str(session_file))
        self.controller.load_session(str(session_file))

        # Test facet removal
        facet_page.set_facets_num(0)
        self.controller.on_facet_num_change(None)

        # Verify facet details are cleared
        self.controller.init_fss_attributes()
        assert not self.controller.facet_var_details, "facet_var_details should be empty"
        assert not self.controller.facet_dim_details, "facet_dim_details should be empty"
        assert not self.controller.facet_details, "facet_details should be empty"
        drv_lines = self.get_drv_lines()
        assert drv_lines[0].strip() == "Data", "Job name should be 'Data'"

        # Save final session
        self._save_session(real_csv_dir)

    def _run_recoding_operations(self):
        """Helper method to run the recoding operations for real CSV test"""
        # First recoding operation on variable 9
        self.controller.gui.show_recode_window()
        self.controller.gui.recode_window.set_variables_indices("9")

        # Define recoding pairs for variable 9
        recoding_pairs = [
            (10, 1),
            (20, 2),
            (30, 3),
            (40, 4),
            (60, 6),
            ("100-10000", 10),
        ]

        # Apply recoding pairs
        for pair in recoding_pairs:
            self.controller.gui.recode_window.add_pair(*pair)
        self.controller.gui.recode_window.apply_recoding()

        # Second recoding operation on variables 1-8 (inverse recoding)
        self.controller.gui.show_recode_window()
        self.controller.gui.recode_window.set_variables_indices("1-8")
        self.controller.gui.recode_window.set_inverse(True)
        self.controller.gui.recode_window.apply_recoding()

        # Show recoding history
        self.controller.gui.show_recode_history_window()
        self.controller.gui.recode_history_window.destroy()

    def run_simple_example_scenario(self):
        """Run the simple example scenario test"""
        # Reset session for recorded data mode
        self.controller.reset_session(matrix=False)

        # Load the simple example test data
        simple_example_dir = Path(os.path.abspath("tests/simple_example"))
        data_file = simple_example_dir / "diamond6.txt"

        assert data_file.exists(), "Simple example test data not found"

        # Set up input data
        input_page = self.controller.gui.pages["InputPage"]
        input_page.set_data_file_path(str(data_file))
        input_page.set_entry_lines(1)

        # Move to manual format page
        self.controller.next_page()

        # Set up manual format with 5 variables
        manual_page = self.controller.gui.pages["ManualFormatPage"]
        for _ in range(5):
            manual_page.add_variable()
        manual_page.set_labels(["a", "b", "c", "d", "e"])
        manual_page.select_variables([0, 1, 2, 4])  # Select variables a, c, e

        # Move to data page
        self.controller.next_page()

        # Move to dimensions page
        self.controller.next_page()

        # Set up dimensions (2-4)
        dims_page = self.controller.gui.pages["DimensionsPage"]
        dims_page.dimension_combo.current(1)
        dims_page.dimension_combo_selected(None)
        dims_page.set_dims(2, 4)

        # Move to facets page
        self.controller.next_page()

        # Set up facets (1 facet)
        facet_page = self.controller.gui.pages["FacetPage"]
        facet_page.set_facets_num(1)
        self.controller.on_facet_num_change(None)

        # Move to facet variables page
        self.controller.next_page()

        # Set up facet variables data
        from lib.fss.fss_input_parser import simulate_facets_var_data
        simulate_facets_var_data(
            " 1\n 1\n 2\n 1", self.controller.gui.pages["FacetVarPage"].combo_by_var
        )

        # Set output path and run
        output_file = simple_example_dir / "test_simple.fss"
        self.controller.output_path = str(output_file)
        self.controller.run_fss(self.controller._run_fss)
        self.controller.enable_view_results()

        # Verify output file was created
        assert os.path.isfile(self.controller.output_path), f"Output file not created: {self.controller.output_path}"

        # Save session
        self._save_session(simple_example_dir)

    def run_unified_load_recorded_data_file(self):
        """Run the unified load recorded data file
        1. load some data file (csv)
        2. move to variables page
        3. select some variables
        4. move back to input page
        5. load the same data file
        6. check if the variables are the same (browsed only)
        7. check if the data is the same
        8. check if the output file is the same
        9. check if the session is the same
        10. check if the job name is the same
        11. load a new data file with different name
        12. check if variables are different (reloaded correctly)
        13. check if data is different (reloaded correctly)
        14. check if output file is different (reloaded correctly)
        15. check if session is different (reloaded correctly)
        16. check if job name is different (reloaded correctly)
        17. load the same data file again
        18. check if variables are the same
        """
        self.controller.reset_session(matrix=False)
        data_file = Path(os.path.abspath("tests/real_csv_test/data.csv"))
        assert data_file.exists(), "Real CSV test data not found"

        input_page = self.controller.gui.pages["InputPage"]
        input_page.set_data_file_path(str(data_file))
        self.controller.set_header(True)
        self.controller.data_file_extension = ".csv"
        self.controller.load_csv_init()
        input_page.disable_additional_options()


    ##############
    # test cases #
    ##############

    def test_unified_load_recorded_data_file(self, visual_mode):
        """Test the unified load recorded data file"""
        self.run_unified_load_recorded_data_file()

        if visual_mode:
            self._setup_visual_test()

    def test_simple_example_scenario(self, visual_mode):
        """Test the simple example scenario"""
        self.run_simple_example_scenario()

        if visual_mode:
            self._setup_visual_test()

    def test_real_csv_test_scenario(self, visual_mode):
        """Test the real CSV test scenario with recoding and facets"""
        self.run_real_csv_test_scenario()

        if visual_mode:
            self._setup_visual_test()

    def test_djmatsq_scenario(self, visual_mode):
        """Test the djmatsq scenario"""
        self.run_djmatsq_scenario()
        if visual_mode:
            self._setup_visual_test()



if __name__ == "__main__":
    pytest.main(["-v", __file__])