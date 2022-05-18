from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from controller.extension_manager import ExtensionManager
from helper.complement import Complement
from services.driver_manager import DriverManager
from services.user_agent_browser import UserAgentBrowser


class WebDriver:
    browser = None
    path_assets = None
    path_driver = None
    is_chrome = False
    is_firefox = False
    is_debug = False
    is_configured = False

    driver = None
    driver_manager = None
    user_agent_browser = None
    extension_manager = None

    driver_chrome = "chromedriver"
    driver_firefox = "geckodriver"

    def __init__(self, path_assets, browser, debug=False):
        self.is_debug = debug
        self.browser = browser
        self.path_assets = path_assets
        self.path_driver = f"{self.path_assets}/driver/"
        self.is_chrome = Complement.browser_is_chrome(browser)
        self.is_firefox = Complement.browser_is_firefox(browser)
        self.is_configured = Complement.check_file_exist(f"{self.path_assets}/config_{self.browser}")
        self.init()

    def init(self):
        self.set_path_driver()
        if not self.is_configured:
            self.configure_driver()

        if self.is_debug is False:
            extension_paths = self.download_extension()
            self.config_driver(extension_paths)

    def configure_driver(self):
        self.install_driver()
        self.init_single_driver()
        self.install_user_agent()
        Complement.write_file(f"{self.path_assets}/config_{self.browser}", "True")
        self.driver.quit()

    def set_path_driver(self):
        driver_name = None
        if self.is_chrome:
            driver_name = self.driver_chrome
        elif self.is_firefox:
            driver_name = self.driver_firefox

        Complement.make_folder(self.path_driver)
        self.path_driver = self.path_driver + driver_name

    def install_driver(self):
        if not Complement.check_file_exist(self.path_driver):
            self.download_driver()

    def init_single_driver(self):
        driver_manager = DriverManager(self.browser, self.path_driver, self.path_assets)
        driver_manager.configure_single()
        self.driver_manager = driver_manager
        self.driver = driver_manager.get_driver()

    def install_user_agent(self):
        user_agent_browser = self._get_user_agent()
        if not user_agent_browser.exist_user_agent():
            self.config_user_agent()

    def _get_user_agent(self):
        if self.user_agent_browser is None:
            self.user_agent_browser = UserAgentBrowser(self.path_assets, self.browser)
        return self.user_agent_browser

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

    def config_driver(self, extension_paths=None):
        if Complement.check_file_exist(self.path_driver):
            driver_manager = DriverManager(self.browser, self.path_driver, self.path_assets, extension_paths)
            driver_manager.configuration(extension_paths)
            self.driver_manager = driver_manager
            self.driver = driver_manager.get_driver()
        else:
            self.download_driver()
            self.config_driver(extension_paths)

    def get_driver_manager(self):
        return self.driver_manager

    def get_driver(self):
        return self.driver

    def config_user_agent(self):
        if self.driver is None:
            self.init_single_driver()
        self.user_agent_browser.set_driver(self.driver)
        self.user_agent_browser.data_user_agent()

    def download_extension(self, debug=False):
        extension_paths = []
        self.extension_manager = ExtensionManager(self.driver_manager, self.driver, self.path_assets, self.browser)
        extension_paths = self.extension_manager.get_extensions()
        return extension_paths

    def start(self):
        import os
        self.driver_manager.set_setting_window()
        # self.extension_manager = ExtensionManager(self.driver_manager, self.driver, self.path_assets, self.browser)
        keys = os.getenv('METAMASK_AUTH')
        keys = keys.replace('[', '').replace(']', '').replace('"', '').replace(', ', ',').replace(' ,', ',').split(',')
        self.extension_manager.wallet.set_passwords(keys[0], keys[1])
        self.extension_manager.wallet.set_driver(self.driver_manager, self.driver)
        self.extension_manager.wallet.login()
        self.driver_manager.close_window()


# # TEST
# def main():
#     import os
#
#     # Get path asset
#     path_asset = os.path.dirname(os.path.abspath(__file__))
#     path_asset = path_asset.replace("helper", "assets")
#     webdriver = WebDriver(path_asset, "chrome")
#     # webdriver = WebDriver(path_asset, 'firefox')
#     driver = webdriver.get_driver()
#     print(webdriver.path_driver)
#
#
# if __name__ == '__main__':
#     main()
