# pylint: skip-file
"""
Configuration for Chrome.
"""
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ServiceChrome

from interface.driver_interface import DriverInterface


class ConfigurationChrome(DriverInterface):
    """ Configuration Chrome class """

    def __init__(self, path_driver, path_assets, environment):
        super().__init__(path_driver, path_assets, environment)

    def set_driver_extension(self, path_extensions):
        """ Set driver extension """
        options_browser = self._get_options()
        options_browser = self._set_extension_pre_config(options_browser, path_extensions)
        self.driver = self._get_manager_driver(options_browser)

    def _get_extension_pre_config(self, options_browser):
        """ Get extension pre config """
        options_browser.accept_untrusted_certs = True
        options_browser.accept_insecure_certs = True
        # options_browser.add_argument('--disable-popup-blocking')

        return options_browser

    def _set_extension_pre_config(self, options_browser, path_extensions):
        """ Set extension pre config """
        options_browser = self._get_extension_pre_config(options_browser)
        for path_extension in path_extensions:
            options_browser = self._set_manager_extension_pre_config(options_browser, path_extension)
        return options_browser

    def _set_manager_extension_pre_config(self, options_browser, path_extension):
        """ Set manager extension pre config """
        match self.environment:
            case 'local':
                return self._set_extension_pre_local(options_browser, path_extension)
            case 'docker':
                return self._set_extension_pre_docker(options_browser, path_extension)
            case 'remote':
                return self._set_extension_pre_remote(options_browser, path_extension)
            case default:
                return options_browser

    def _set_extension_pre_local(self, options_browser, path_extension):
        """ Set extension pre local """
        #   options_browser.add_argument(f'--load-extension = {extension}')
        options_browser.add_extension(path_extension)
        return options_browser

    def _set_extension_pre_docker(self, options_browser, path_extension):
        """ Set extension pre docker """
        #   options_browser.add_argument(f'--load-extension = {extension}')
        options_browser.add_extension(path_extension)
        return options_browser

    def _set_extension_pre_remote(self, options_browser, path_extension):
        """ Set extension pre remote """
        #   options_browser.add_argument(f'--load-extension = {extension}')
        options_browser.add_extension(path_extension)
        return options_browser

    def _get_driver_local(self, options_browser):
        """ Get driver local """
        service = self._get_service()
        return webdriver.Chrome(service=service, options=options_browser)

    def _get_driver_docker(self, options_browser):
        """ Get driver docker """
        return webdriver.Chrome(options=options_browser)

    def _get_service(self):
        """ Get service """
        service_browser = ServiceChrome(self.path_driver)
        return service_browser

    def _set_service_option(self):
        """ Set service option """
        return webdriver.ChromeOptions()

    def _get_options_general(self, options_browser):
        """ Get options general """
        options_browser.add_argument("--lang=en-US")
        options_browser.add_argument("--disable-infobars")
        options_browser.add_argument("--start-maximized")
        options_browser.add_experimental_option(
            "prefs",
            {
                "intl.accept_languages": "en,en_US",
                "download.default_directory": os.getcwd(),
                "download.prompt_for_download": False,
            },
        )
        options_browser.add_experimental_option("excludeSwitches", ["enable-logging"])
        options_browser.add_experimental_option("excludeSwitches", ["enable-automation"])
        options_browser.add_experimental_option("useAutomationExtension", False)
        return options_browser

    def _get_options_local(self, options_browser):
        """ Get options local """
        # options_browser.add_argument("--no-sandbox")
        options_browser.add_argument("--log-level=3")
        options_browser.add_argument("--disable-gpu")
        options_browser.add_argument("--no-first-run")
        options_browser.add_argument("--disk-cache-size=1")
        options_browser.add_argument("--media-cache-size=1")
        options_browser.add_argument("--no-service-autorun")
        options_browser.add_argument("--password-store=basic")
        # options_browser.add_argument("--disable-dev-shm-usage")
        options_browser.add_argument("--disable-application-cache")
        options_browser.add_argument("--disable-blink-features=AutomationControlled")
        return options_browser

    def _get_options_docker(self, options_browser):
        """ Get options docker """
        # options_browser.add_argument('--headless')
        options_browser.add_argument('--no-sandbox')
        options_browser.add_argument('--disable-dev-shm-usage')
        return options_browser
