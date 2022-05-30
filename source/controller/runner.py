"""
Runner for the controller.
"""
import os

from dotenv import load_dotenv
from pyvirtualdisplay import Display

from controller.web_driver import WebDriver


class Runner:
    """ Runner class """
    driver = None
    webdriver = None
    display = None

    root_path = None
    path_asset = None

    browser = 'chrome'
    environment = 'local'

    def __init__(self, root_path):
        self.root_path = root_path
        self.run()

    def run(self):
        """ Run """
        self.configuration()
        self.configure_browser()
        self.test()

    def configuration(self):
        """ Configuration """
        load_dotenv()
        self.path_asset = os.getenv('PATH_ASSETS') or 'assets'
        self.path_asset = self.root_path + '/' + self.path_asset
        self.environment = os.getenv('ENVIRONMENT') or 'local'
        self.browser = os.getenv('BROWSER') or 'chrome'

    def configure_browser(self):
        """ Configure browser """
        if self.environment == 'docker':
            self.start_display()
        self.start_webdriver()

    def start_webdriver(self):
        """ Start webdriver """
        self.webdriver = WebDriver(self.path_asset, self.browser, self.environment)
        self.driver = self.webdriver.get_driver()

    def start_display(self):
        """ Start display """
        self.display = Display(size=(800, 600))
        self.display.start()

    def stop_display(self):
        """ Stop display """
        self.display.stop()

    def test(self):
        """ Test """
        self.webdriver.start()
        if self.environment == 'docker':
            self.stop_display()
