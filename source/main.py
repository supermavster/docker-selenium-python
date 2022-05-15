import os

from controller.runner import Runner

# from pyvirtualdisplay import Display

if __name__ == "__main__":
    # display = Display(visible=0, size=(800, 600))
    # display.start()
    root_path = os.path.dirname(os.path.abspath(__file__))
    Runner(root_path)
    # display.stop()
