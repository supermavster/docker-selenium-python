"""
Driver Manager
"""
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from helper.complement import Complement
from service.driver.configuration_chrome import ConfigurationChrome
from service.driver.configuration_firefox import ConfigurationFirefox


def download_chrome_driver():
    """ Download Chrome Driver """
    return ChromeDriverManager().install()


def download_firefox_driver():
    """ Download Firefox Driver """
    return GeckoDriverManager().install()


class DriverManager:
    """ Driver Manager """
    driver = None
    path_driver = None
    path_assets = None

    environment = 'local'

    browser = 'chrome'
    is_chrome = False
    is_firefox = False
    configuration_driver = None

    driver_chrome = "chromedriver"
    driver_firefox = "geckodriver"

    def __init__(self, path_assets, browser, environment):
        self.path_assets = path_assets
        self.browser = browser
        self.environment = environment
        self.init()

    def init(self):
        """ Initialize """
        self.is_chrome = Complement.browser_is_chrome(self.browser)
        self.is_firefox = Complement.browser_is_firefox(self.browser)
        self.path_driver = f"{self.path_assets}/driver/"
        self._set_path_driver()
        self.configure_driver()

    def _set_path_driver(self):
        """ Set Path Driver """
        driver_name = None
        if self.is_chrome:
            driver_name = self.driver_chrome
        elif self.is_firefox:
            driver_name = self.driver_firefox

        Complement.make_folder(self.path_driver)
        self.path_driver = self.path_driver + driver_name

    def setup_driver(self):
        """ Setup Driver """
        if not Complement.check_file_exist(self.path_driver) and self.environment == 'local':
            self.download_driver()

    def download_driver(self):
        """ Download Driver """
        driver_data = None
        if self.is_chrome:
            driver_data = download_chrome_driver()
        elif self.is_firefox:
            driver_data = download_firefox_driver()

        if driver_data is not None:
            Complement.move_file(driver_data, self.path_driver)

    def configure_driver(self):
        """ Configure Driver """
        config_single = None
        if self.is_chrome:
            config_single = ConfigurationChrome(
                self.path_driver, self.path_assets, self.environment
            )
        elif self.is_firefox:
            config_single = ConfigurationFirefox(
                self.path_driver, self.path_assets, self.environment
            )

        self.configuration_driver = config_single

    def configure_single(self):
        """ Configure Single """
        self.configuration_driver.set_driver()

    def get_driver(self):
        """ Get Driver """
        return self.configuration_driver.get_driver()

    def configure_master(self, path_extensions):
        """ Configure Master """
        self.configuration_driver.set_driver_extension(path_extensions)
