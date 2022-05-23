import os

from pyvirtualdisplay import Display
from controller.runner import Runner

if __name__ == "__main__":
    display = Display(size=(800, 600))
    display.start()
    root_path = os.path.dirname(os.path.abspath(__file__))
    Runner(root_path)
    display.stop()
