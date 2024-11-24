import unittest
from unittest.mock import MagicMock, patch
import tkinter as tk
from tkinter import messagebox
from lib.windows.run_window import RunWindow
from lib.components.window import Window
from lib.utils import IS_PRODUCTION

class TestRunWindow(unittest.TestCase):
    def setUp(self):
        """
        setUp runs before EACH test method.
        Use it to set up any objects or state needed by all tests.
        """
        # Create a root window for testing - needed for any Tkinter testing
        self.parent = tk.Tk()
        self.default_output_file = "test_analysis.fss"
        
        # Clear singleton instances to ensure clean state
        Window.clear_instances()
        
        # Using context manager to mock get_resource
        # patch replaces the target function/object with a mock during the test
        with patch('lib.components.window.get_resource') as mock_get_resource:
            mock_get_resource.return_value = None  # Mock returns None instead of loading real icon
            # Create the window we'll test
            self.window = RunWindow(self.parent, default_output_file=self.default_output_file)

    def tearDown(self):
        """
        tearDown runs after EACH test method.
        Use it to clean up any resources created during tests.
        """
        # Clean up Tkinter windows with error handling
        if hasattr(self, 'window') and self.window:
            try:
                self.window.destroy()
            except tk.TclError:  # Handle case where window was already destroyed
                pass
        try:
            self.parent.destroy()
        except tk.TclError:
            pass
        # Clear singleton instances after test
        Window.clear_instances()

    def test_default_values(self):
        """
        Test case: Verify that default values are set correctly.
        Pattern: Arrange (setup) -> Act (perform action) -> Assert (verify results)
        """
        # Assert that all default values match expected values
        self.assertEqual(self.window.default_output_file, "test_analysis.fss")
        self.assertEqual(self.window.default_job_name, "test_analysis")
        self.assertEqual(self.window.job_name_entry.get(), "test_analysis")
        self.assertEqual(self.window.output_file_entry.get(), "test_analysis.fss")

    def test_empty_defaults(self):
        """
        Test case: Verify behavior with empty default values.
        Shows how to create a separate instance with different parameters.
        """
        with patch('lib.components.window.get_resource') as mock_get_resource:
            mock_get_resource.return_value = None
            window = RunWindow(self.parent)  # Create window with no defaults
            # Verify empty defaults
            self.assertEqual(window.default_output_file, "")
            self.assertEqual(window.default_job_name, "")
            self.assertEqual(window.job_name_entry.get(), "")
            self.assertEqual(window.output_file_entry.get(), "")
            window.destroy()

    @patch('tkinter.filedialog.asksaveasfilename')  # Decorator to mock file dialog
    def test_browse_output(self, mock_filedialog):
        """
        Test case: Verify browse button functionality.
        Shows how to mock dialog results and test UI interactions.
        """
        # Setup mock to return specific path
        mock_filedialog.return_value = "new_path/output.fss"
        # Act: Trigger browse action
        self.window.browse_output()
        # Assert: Verify entry was updated
        self.assertEqual(self.window.output_file_entry.get(), "new_path/output.fss")

    @patch('tkinter.filedialog.asksaveasfilename')
    def test_browse_output_cancel(self, mock_filedialog):
        """
        Test case: Verify browse cancellation behavior.
        Shows how to test cancel scenarios and state preservation.
        """
        # Arrange: Set initial value
        original_value = "original.fss"
        self.window.output_file_entry.delete(0, tk.END)
        self.window.output_file_entry.insert(0, original_value)
        
        # Setup mock to simulate cancel (empty return)
        mock_filedialog.return_value = ""
        # Act: Trigger browse action
        self.window.browse_output()
        # Assert: Original value should be preserved
        self.assertEqual(self.window.output_file_entry.get(), original_value)

    @patch('tkinter.messagebox.showerror')
    def test_run_with_empty_fields(self, mock_showerror):
        """
        Test case: Verify validation of empty fields.
        Shows how to test error scenarios and verify error messages.
        """
        # Arrange: Clear both fields
        self.window.job_name_entry.delete(0, tk.END)
        self.window.output_file_entry.delete(0, tk.END)
        
        # Act & Assert: Test empty job name
        self.window.run()
        mock_showerror.assert_called_with("Error", "Please enter a job name")
        
        # Act & Assert: Test empty output file
        self.window.job_name_entry.insert(0, "test_job")
        self.window.run()
        mock_showerror.assert_called_with("Error", "Please select an output file")

    def test_run_with_valid_input(self):
        """
        Test case: Verify successful run behavior.
        Shows how to test happy path and verify results.
        """
        # Arrange: Set valid inputs
        test_job = "test_job"
        test_output = "test_output.fss"
        
        self.window.job_name_entry.delete(0, tk.END)
        self.window.job_name_entry.insert(0, test_job)
        self.window.output_file_entry.delete(0, tk.END)
        self.window.output_file_entry.insert(0, test_output)
        
        # Act: Trigger run
        self.window.run()
        # Assert: Verify result tuple
        self.assertEqual(self.window.result, (test_job, test_output))

    def test_cancel(self):
        """
        Test case: Verify cancel behavior.
        Shows how to test cancellation and result clearing.
        """
        self.window.cancel()
        self.assertIsNone(self.window.result)

    @patch('lib.utils.IS_PRODUCTION', return_value=True)
    def test_singleton_pattern(self, mock_is_production):
        """
        Test case: Verify singleton pattern behavior.
        Shows how to test design patterns and object identity.
        """
        with patch('lib.components.window.get_resource') as mock_get_resource:
            mock_get_resource.return_value = None
            # Create two instances
            first_window = RunWindow(self.parent)
            second_window = RunWindow(self.parent)
            # Verify they are the same object
            self.assertIs(first_window, second_window)
            try:
                first_window.destroy()
            except tk.TclError:
                pass

if __name__ == '__main__':
    unittest.main()  # This allows running tests directly from this file 