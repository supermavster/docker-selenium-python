from abc import abstractmethod

import helpers.complement as complement
from helpers.download_extension_chrome import DownloadExtensionChrome
from helpers.download_extension_firefox import DownloadExtensionFirefox
from interface.interface import Interface


class PluginManager(metaclass=Interface):
    path_assets = ""
    path_data = ""
    # Chrome
    url_extension = ""
    # Firefox
    data_extension_firefox = {}

    def __init__(self, path_assets, webdriver=None, browser="Chrome"):
        self.driver = None
        self.download_extension = None
        self.browser = browser
        self.webdriver = webdriver
        self.path_assets = path_assets
        self.set_config()

    @abstractmethod
    def set_config(self):
        self.set_browser()
        self.set_web_driver(self.webdriver)

    @abstractmethod
    def set_browser(self):
        if self.browser_is_chrome():
            self.download_extension = DownloadExtensionChrome(self.path_assets)
        elif self.browser_is_firefox():
            self.download_extension = DownloadExtensionFirefox(self.path_assets)

    @abstractmethod
    def browser_is_chrome(self):
        return complement.browser_is_chrome(self.browser)

    @abstractmethod
    def browser_is_firefox(self):
        return complement.browser_is_firefox(self.browser)

    @abstractmethod
    def set_web_driver(self, webdriver, driver=None):
        if webdriver is not None:
            self.webdriver = webdriver
            if driver is None:
                self.driver = self.webdriver.driver
            else:
                self.driver = driver
            self.download_extension.set_driver(self.driver)

    @abstractmethod
    def get_information_extension(self):
        url = self.url_extension
        return self.download_extension.exist_extension_by_url(url)

    @abstractmethod
    def get_path_extension(self):
        check_extension = self.get_information_extension()
        return check_extension["path_file"]

    @abstractmethod
    def extension_exist(self):
        check_extension = self.get_information_extension()
        return check_extension["exist"]

    @abstractmethod
    def install(self):
        if not self.extension_exist():
            self.download_extension.generate_extension(self.url_extension)

    @abstractmethod
    def start(self):
        if self.browser_is_firefox():
            self.url_extension = self.download_extension.get_url_extension(
                self.data_extension_firefox
            )
        self.install()