from controller.extension_manager import ExtensionManager
from helper.complement import Complement
from services.driver_action import DriverAction
from services.driver_manager import DriverManager
from services.user_agent_browser import UserAgentBrowser


class WebDriver:
    path_assets = None
    is_configured = False

    browser = None
    is_chrome = False
    is_firefox = False
    environment = 'local'

    driver = None
    driver_manager = None
    driver_action = None
    user_agent_browser = None
    extension_manager = None

    def __init__(self, path_assets, browser, environment):
        self.path_assets = path_assets
        self.browser = browser
        self.environment = environment
        self._init()

    def _init(self):
        self._set_main_variables()
        self._start_driver()

    def _set_main_variables(self):
        self.is_chrome = Complement.browser_is_chrome(self.browser)
        self.is_firefox = Complement.browser_is_firefox(self.browser)
        self.is_configured = Complement.check_file_exist(f"{self.path_assets}/config_{self.browser}")

    def _start_driver(self):
        if not self.is_configured:
            self._configure_driver()

        self._download_extension()
        self._init_driver()

    def _configure_driver(self):
        self._init_driver_manager()
        self._install_driver()
        self._init_single_driver()
        self._install_user_agent()
        self._make_config_file()
        self.driver.quit()

    def _init_driver_manager(self):
        driver_manager = DriverManager(self.path_assets, self.browser, self.environment)
        self.driver_manager = driver_manager

    def _install_driver(self):
        self.driver_manager.setup_driver()

    def _check_managers(self):
        self.driver = None
        if self.driver_manager is None:
            self._init_driver_manager()

    def _init_single_driver(self):
        self.driver_manager.configure_single()
        self.driver = self.driver_manager.get_driver()

    def _init_driver(self):
        self._check_managers()

        path_extensions = self._get_path_extension()
        self.driver_manager.configure_master(path_extensions)
        self.driver = self.driver_manager.get_driver()
        self._set_driver_action()
        if path_extensions is not None and len(path_extensions) > 0:
            self._set_extension_manager()

    def _install_user_agent(self):
        self.user_agent_browser = UserAgentBrowser(self.path_assets, self.browser, self.driver)
        if not self.user_agent_browser.exist_user_agent():
            self.user_agent_browser.data_user_agent()

    def _make_config_file(self):
        Complement.write_file(f"{self.path_assets}/config_{self.browser}", "True")

    def get_driver_manager(self):
        return self.driver_manager

    def get_driver(self):
        return self.driver

    def _download_extension(self):
        self.extension_manager = ExtensionManager(self.path_assets, self.browser)

    def _set_extension_manager(self):
        self.extension_manager = ExtensionManager(self.path_assets, self.browser, self.driver_manager,
                                                  self.driver_action, self.driver)

    def _get_path_extension(self):
        if self.extension_manager is not None:
            return self.extension_manager.get_extensions()
        return []

    def _set_driver_action(self):
        self.driver_action = DriverAction(self.driver, self.is_chrome, self.is_firefox)

    def start(self):
        self.driver_action.set_setting_window()
        # self.driver_action.wait_time()
        self.example_metamask()
        self.driver_action.close_window()

    def example_metamask(self):
        import os
        keys = os.getenv('METAMASK_AUTH')
        keys = keys.replace('[', '').replace(']', '').replace('"', '').replace(', ', ',').replace(' ,', ',').split(',')
        self.extension_manager.wallet.set_passwords(keys[0], keys[1])
        # self.extension_manager.wallet.set_driver(self.driver_action, self.driver)
        self.extension_manager.wallet.login()

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
