# app.py
from lib.controller.controller import Controller
from lib.version import __version__
import os
import tkinter as tk
import sys

os.environ['APP_VERSION'] = __version__

def main():
    print("Starting the FSSA: {}".format(__version__))
    print(f"Python version: {sys.version}")
    print(f"Tkinter version: {tk.TkVersion}")
    controller = Controller()
    controller.run_process()

if __name__ == '__main__':
    main()
