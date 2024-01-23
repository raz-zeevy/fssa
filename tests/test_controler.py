import time

import pytest
from unittest.mock import Mock, patch
from app import App
from contextlib import contextmanager
import os
from lib.controller import *

@contextmanager
def change_dir(new_dir):
    old_dir = os.getcwd()
    os.chdir(new_dir)
    try:
        yield
    finally:
        os.chdir(old_dir)

@pytest.fixture
def app():
    app = App()
    yield app
    app.controller.shutdown()

def test_add_variable(app):
    app.controller.gui.navigate_page(MANUAL_FORMAT_PAGE_NAME)
    manual_page = app.controller.gui.pages[MANUAL_FORMAT_PAGE_NAME]
    manual_page.add_variable("test", "test", "test", "test")
    assert len(manual_page.data_table.iidmap) == 1

@patch('tkinter.filedialog.asksaveasfilename')
def test_file_save(mock_save_dialog, app):
    pass