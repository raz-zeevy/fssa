# app.py
import os
import sys
from lib.controller.controller import Controller

def main():
    controller = Controller()
    controller.run_process()

if __name__ == '__main__':
    main()
