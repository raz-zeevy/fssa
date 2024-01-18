import pytest
from unittest.mock import Mock, patch
from app import App
from contextlib import contextmanager
import os

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

def test_initial_state(app):
    assert app.controller.data_file_path is None


@patch('tkinter.filedialog.asksaveasfilename')
def test_file_save(mock_save_dialog, app):
    pass