import os
from pyvirtualdisplay import Display

from dotenv import load_dotenv

from .web_driver import WebDriver


class Runner:
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
        self.configuration()
        self.configure_browser()
        self.test()

    def configuration(self):
        load_dotenv()
        self.path_asset = os.getenv('PATH_ASSETS') or 'assets'
        self.path_asset = self.root_path + '/' + self.path_asset
        self.environment = os.getenv('ENVIRONMENT') or 'local'
        self.browser = os.getenv('BROWSER') or 'chrome'

    def configure_browser(self):
        if self.environment == 'docker':
            self.start_display()
        self.start_webdriver()

    def start_webdriver(self):
        self.webdriver = WebDriver(self.path_asset, self.browser, self.environment)
        self.driver = self.webdriver.get_driver()

    def start_display(self):
        self.display = Display(size=(800, 600))
        self.display.start()

    def stop_display(self):
        self.display.stop()

    def test(self):
        self.webdriver.start()
        if self.environment == 'docker':
            self.stop_display()
