"""
WebDriver class for the controller.
"""
import os

from controller.extension_manager import ExtensionManager
from helper.complement import Complement
from service.driver_action import DriverAction
from service.driver_manager import DriverManager
from service.user_agent_browser import UserAgentBrowser


class WebDriver:
    """ WebDriver class for the controller. """
    path_assets = None
    browser = None
    environment = 'local'
    driver = None
    driver_manager = None
    driver_action = None
    extension_manager = None

    def __init__(self, path_assets, browser, environment):
        self.path_assets = path_assets
        self.browser = browser
        self.environment = environment
        self._init()

    def _init(self):
        self._start_driver()

    def _get_is_configured(self):
        path_file = f"{self.path_assets}/config_{self.browser}"
        return Complement.check_file_exist(path_file)

    def _start_driver(self):
        if not self._get_is_configured():
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
        user_agent_browser = UserAgentBrowser(self.path_assets, self.browser, self.driver)
        if not user_agent_browser.exist_user_agent():
            user_agent_browser.data_user_agent()

    def _make_config_file(self):
        Complement.write_file(f"{self.path_assets}/config_{self.browser}", "True")

    def get_driver_manager(self):
        """ Return the driver manager. """
        return self.driver_manager

    def get_driver(self):
        """ Return the driver. """
        return self.driver

    def _download_extension(self):
        self.extension_manager = ExtensionManager(self.path_assets, self.browser)

    def _set_extension_manager(self):
        self.extension_manager = None
        self.extension_manager = ExtensionManager(self.path_assets, self.browser,
                                                  self.driver_action, self.driver)

    def _get_path_extension(self):
        if self.extension_manager is not None:
            return self.extension_manager.get_extensions()
        return []

    def _set_driver_action(self):
        is_chrome = Complement.browser_is_chrome(self.browser)
        is_firefox = Complement.browser_is_firefox(self.browser)
        self.driver_action = DriverAction(self.driver, is_chrome, is_firefox)

    def start(self):
        """ Start the driver """
        self.driver_action.set_setting_window()

        # Example:
        self.example_extensions()

        self.driver_action.close_window()

    def example_extensions(self):
        """ Example of use of the extension manager. """
        extensions = os.getenv('EXTENSIONS_' + self.browser.upper()) or None
        if extensions is None:
            # Normal
            self.driver_action.wait_time()
            print(self.driver_action.get_title())
        else:
            self.example_extensions_basic(extensions)

    def example_extensions_basic(self, extensions):
        """ Example extensions """
        extensions = Complement.convertENVArray(extensions)

        for extension in extensions:
            match extension:
                case 'metamask':
                    # Metamask
                    self.example_metamask()
                case 'captcha':
                    # CAPTCHA
                    self.example_captcha()

    def example_metamask(self):
        """ Example of metamask """
        keys = os.getenv('METAMASK_AUTH') or ""
        keys = Complement.convertENVArray(keys)
        self.extension_manager.wallet.set_passwords(keys[0], keys[1])
        self.extension_manager.wallet.login()

    def example_captcha(self):
        """ Example of CAPTCHA """
        self.extension_manager.captcha.set_test_url()
        self.extension_manager.captcha.resolve()
