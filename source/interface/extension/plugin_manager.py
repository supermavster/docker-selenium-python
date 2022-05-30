"""
Plugin Manager
"""
from helper.complement import Complement
from interface.interface import Interface
from service.extension.download_extension_chrome import DownloadExtensionChrome
from service.extension.download_extension_firefox import DownloadExtensionFirefox


class PluginManager(metaclass=Interface):
    """ Plugin manager class """
    path_assets = ""
    path_data = ""
    # Chrome
    url_extension = ""
    # Firefox
    data_extension_firefox = {}

    def __init__(self, path_assets, browser, driver=None):
        self.path_assets = path_assets
        self.browser = browser

        self.driver = driver

        self.download_extension = None
        self.set_config()

    # @abstractmethod
    def set_config(self):
        """ Set config """
        self.set_browser()
        self.set_driver(self.driver)

    # @abstractmethod
    def set_browser(self):
        """ Set browser """
        if self.browser_is_chrome():
            self.download_extension = DownloadExtensionChrome(self.path_assets)
        elif self.browser_is_firefox():
            self.download_extension = DownloadExtensionFirefox(self.path_assets)

    # @abstractmethod
    def browser_is_chrome(self):
        """ Check if browser is chrome """
        return Complement.browser_is_chrome(self.browser)

    # @abstractmethod
    def browser_is_firefox(self):
        """ Check if browser is firefox """
        return Complement.browser_is_firefox(self.browser)

    # @abstractmethod
    def set_driver(self, driver):
        """ Set driver """
        self.driver = driver
        self.download_extension.set_driver(self.driver)

    # @abstractmethod
    def get_information_extension(self):
        """ Get information extension """
        url = self.url_extension
        return self.download_extension.exist_extension_by_url(url)

    # @abstractmethod
    def get_path_extension(self):
        """ Get path extension """
        check_extension = self.get_information_extension()
        return check_extension["path_file"]

    # @abstractmethod
    def extension_exist(self):
        """ Check if extension exist """
        check_extension = self.get_information_extension()
        return check_extension["exist"]

    # @abstractmethod
    def install(self):
        """ Install extension """
        if not self.extension_exist():
            self.download_extension.generate_extension(self.url_extension)

    # @abstractmethod
    def start(self):
        """ Start extension """
        if self.browser_is_firefox():
            self.url_extension = self.download_extension.get_url_extension(
                self.data_extension_firefox
            )
        self.install()
