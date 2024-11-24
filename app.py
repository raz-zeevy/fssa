# app.py
from lib.controller.controller import Controller
from lib.version import __version__

def main():
    controller = Controller()
    controller.run_process()

if __name__ == '__main__':
    main()
