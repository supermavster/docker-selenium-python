from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from helper.complement import Complement
from services.configuration_chrome import ConfigurationChrome
from services.configuration_firefox import ConfigurationFirefox


class DriverManager:
    driver = None
    path_driver = None
    path_assets = None

    environment = 'local'

    browser = 'chrome'
    is_chrome = False
    is_firefox = False
    configuration_driver = None

    def __init__(self, path_driver, path_assets, browser, environment):
        self.path_driver = path_driver
        self.path_assets = path_assets
        self.browser = browser
        self.environment = environment
        self.is_chrome = Complement.browser_is_chrome(browser)
        self.is_firefox = Complement.browser_is_firefox(browser)
        self.configure_driver()

    def setup_driver(self):
        if not Complement.check_file_exist(self.path_driver) and self.environment == 'local':
            self.download_driver()

    def download_driver(self):
        driver_data = None
        if self.is_chrome:
            driver_data = self.download_chrome_driver()
        elif self.is_firefox:
            driver_data = self.download_firefox_driver()

        if driver_data is not None:
            Complement.move_file(driver_data, self.path_driver)

    def download_chrome_driver(self):
        return ChromeDriverManager().install()

    def download_firefox_driver(self):
        return GeckoDriverManager().install()

    def configure_driver(self):
        config_single = None
        if self.is_chrome:
            config_single = ConfigurationChrome(self.path_driver, self.environment)
        elif self.is_firefox:
            config_single = ConfigurationFirefox(self.path_driver, self.path_assets, self.environment)

        self.configuration_driver = config_single

    def configure_single(self):
        self.configuration_driver.set_driver()

    def get_driver(self):
        return self.configuration_driver.get_driver()

    def configure_master(self, path_extensions):
        self.configuration_driver.set_driver_extension(path_extensions)
