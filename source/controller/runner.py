import os
import time

from dotenv import load_dotenv

from .web_driver import WebDriver


class Runner:
    driver = None
    webdriver = None

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
        print(self.environment)
        self.browser = os.getenv('BROWSER') or 'chrome'

    def configure_browser(self):
        self.webdriver = WebDriver(self.path_asset, self.browser, self.environment)
        self.driver = self.webdriver.get_driver()

    def test(self):
        self.webdriver.start()
