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
    with change_dir(os.path.join(os.path.dirname(__file__), '..')):
        app = App()
        yield app
        app.shutdown()

def test_initial_state(app):
    assert app.data_file_path is None


@patch('tkinter.filedialog.asksaveasfilename')
def test_file_save(mock_save_dialog, app):
    pass