from abc import abstractmethod

from helper.complement import Complement
from interface.interface import Interface
from services.extension.download_extension_chrome import DownloadExtensionChrome
from services.extension.download_extension_firefox import DownloadExtensionFirefox


class PluginManager(metaclass=Interface):
    path_assets = ""
    path_data = ""
    # Chrome
    url_extension = ""
    # Firefox
    data_extension_firefox = {}

    def __init__(self, path_assets, browser, driver_manager=None, driver=None):
        self.path_assets = path_assets
        self.browser = browser

        self.driver_manager = driver_manager
        self.driver = driver

        self.download_extension = None
        self.set_config()

    @abstractmethod
    def set_config(self):
        self.set_browser()
        self.set_driver(self.driver_manager, self.driver)

    @abstractmethod
    def set_browser(self):
        if self.browser_is_chrome():
            self.download_extension = DownloadExtensionChrome(self.path_assets)
        elif self.browser_is_firefox():
            self.download_extension = DownloadExtensionFirefox(self.path_assets)

    @abstractmethod
    def browser_is_chrome(self):
        return Complement.browser_is_chrome(self.browser)

    @abstractmethod
    def browser_is_firefox(self):
        return Complement.browser_is_firefox(self.browser)

    @abstractmethod
    def set_driver(self, driver_manager, driver=None):
        if driver_manager is not None:
            self.driver_manager = driver_manager
            if driver is None:
                self.driver = self.driver_manager.get_driver()
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
