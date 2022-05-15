from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from helper.complement import Complement
from helper.driver import Driver
from helper.user_agent_browser import UserAgentBrowser


class WebDriver:
    browser = None
    driver = None
    path_assets = None
    path_driver = None

    driver_chrome = "chromedriver"
    driver_firefox = "geckodriver"

    def __init__(self, path_assets, browser):
        self.path_assets = path_assets
        self.path_driver = f"{self.path_assets}/driver/"
        self.browser = browser
        self.init()

    def init(self):
        self.set_path_driver()
        self.install_driver()
        self.config_driver()
        self.config_user_agent()

    def set_path_driver(self):
        driver_name = None
        if Complement.browser_is_chrome(self.browser):
            driver_name = self.driver_chrome
        elif Complement.browser_is_firefox(self.browser):
            driver_name = self.driver_firefox

        Complement.make_folder(self.path_driver)
        self.path_driver = self.path_driver + driver_name

    def install_driver(self):
        if not Complement.check_file_exist(self.path_driver):
            self.download_driver()

    def download_driver(self):
        driver_data = None
        if Complement.browser_is_chrome(self.browser):
            driver_data = self.download_chrome_driver()
        elif Complement.browser_is_firefox(self.browser):
            driver_data = self.download_firefox_driver()

        if driver_data is not None:
            Complement.move_file(driver_data, self.path_driver)

    def download_chrome_driver(self):
        return ChromeDriverManager().install()

    def download_firefox_driver(self):
        return GeckoDriverManager().install()

    def config_driver(self, extension_path=None):
        if Complement.check_file_exist(self.path_driver):
            driver = Driver(self.browser, self.path_driver, self.path_assets, extension_path)
            self.driver = driver.get_driver()
        else:
            self.download_driver()
            return self.config_driver(extension_path)

    def get_driver(self):
        return self.driver

    def config_user_agent(self):
        user_agent_browser = UserAgentBrowser(self.path_assets)
        user_agent_browser.set_driver(self.driver)
        user_agent_browser.data_user_agent()

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
