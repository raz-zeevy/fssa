# app.py
from lib.controller import Controller


class App():
    def __init__(self):
        self.controller = Controller()

    def run(self):
        self.controller.run_process()

if __name__ == '__main__':
    app = App()
    app.run()