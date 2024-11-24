# Import the required modules
import unittest  # Python's built-in testing framework
import logging   # For handling log messages during tests
from lib.windows.recoding_window import RecodeWindow  # The class we're testing

class TestRecodeWindow(unittest.TestCase):  # Create a test class that inherits from unittest.TestCase
    def setUp(self):
        """
        setUp runs before EACH test method
        We use it to set up any objects we'll need in multiple tests
        """
        # Create a RecodeWindow instance with None as parent
        # This works because we're only testing methods that don't require GUI interaction
        self.window = RecodeWindow(None)

    def test_parse_ranges(self):
        """
        Test method for parsing valid ranges
        Method names MUST start with 'test_' to be recognized as tests
        """
        # Define test cases as pairs of (input, expected_output)
        test_cases = [
            ("1,2,3", {1,2,3}),        # Simple comma-separated list
            ("1-3", {1,2,3}),          # Simple range
            ("1,3-5,7", {1,3,4,5,7}),  # Mixed format
            ("1-3,5-7", {1,2,3,5,6,7}) # Multiple ranges
        ]
        
        # Test each case
        for input_str, expected in test_cases:
            # subTest allows us to see which specific test case failed
            with self.subTest(input_str=input_str):
                # Call the method we're testing
                result = self.window.parse_ranges(input_str)
                # Assert that the result matches what we expect
                self.assertEqual(result, expected)

    def test_invalid_ranges(self):
        """
        Test method for handling invalid ranges
        """
        # Define invalid inputs we want to test
        invalid_inputs = [
            "3-1",    # reverse range
            "a-b",    # non-numeric
            "1,2,a",  # mixed invalid
            "1--3",   # double negative
        ]
        
        # Test each invalid input
        for invalid_input in invalid_inputs:
            with self.subTest(invalid_input=invalid_input):
                # assertRaises checks that the specified exception is raised
                with self.assertRaises(ValueError):
                    self.window.parse_ranges(invalid_input)

# This allows running the tests directly from this file
if __name__ == '__main__':
    unittest.main()