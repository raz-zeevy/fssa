import os
import unittest

import numpy as np

from lib.controller import Controller
from lib.fss import load_data_file
from lib.utils import DELIMITER_1_D


class TestFSSAProcess(unittest.TestCase):
    def setUp(self):
        # Initialize the Controller
        self.controller = Controller()

        # Load the data file
        self.data_file_path = '../lib/scripts/simaple_example/diamond6.txt'
        self.data = load_data_file(self.data_file_path, delimiter=DELIMITER_1_D)

    def test_load_file(self):
        # Test if the file is loaded correctly
        data = [[1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 2], [1, 1, 1, 1, 2, 1], [1, 1, 1, 2, 1, 1], [1, 1, 2, 1, 1, 1], [1, 2, 1, 1, 1, 1], [2, 1, 1, 1, 1, 1], [1, 1, 1, 1, 2, 2], [1, 1, 1, 2, 2, 1], [1, 1, 2, 2, 1, 1], [1, 2, 2, 1, 1, 1], [2, 2, 1, 1, 1, 1], [1, 1, 1, 2, 2, 2], [1, 1, 2, 2, 2, 1], [1, 2, 2, 2, 1, 1], [2, 2, 2, 1, 1, 1], [1, 1, 2, 2, 2, 2], [1, 2, 2, 2, 2, 1], [2, 2, 2, 2, 1, 1], [1, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 1], [2, 2, 2, 2, 2, 2]]
        self.assertIsNotNone(np.array_equal(self.data, np.array(data)))

    def assert_files_exist(self):
        # Test if the files are created
        self.assertTrue(os.path.exists(self.controller.fss_file_path))
        self.assertTrue(os.path.exists(self.controller.fss_file_path))
        self.assertTrue(os.path.exists(self.controller.fss_file_path))

    def test_run_simple_example(self):
        # Access and set the dimensions in the GUI
        for scale in self.controller.gui.pages['DimensionsPage']. \
                dimension_boxes: scale.set('2')
        assert self.controller.gui.pages[
                   'DimensionsPage'].get_dimensions() == [2]

        # self.controller.gui.pages['FacetPage'].button_run.invoke()
        self.controller.run_fss()
        print("ok")


if __name__ == '__main__':
    unittest.main()