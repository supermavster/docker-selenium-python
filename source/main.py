"""
Main Run file for the project.
"""
import os

from controller.runner import Runner

if __name__ == "__main__":
    root_path = os.path.dirname(os.path.abspath(__file__))
    Runner(root_path)
