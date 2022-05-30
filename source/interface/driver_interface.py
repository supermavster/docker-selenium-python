"""
Driver interface for the robot.
"""
import json
import os
import uuid
from abc import abstractmethod

from selenium import webdriver

from interface.interface import Interface


class DriverInterface(metaclass=Interface):
    """ Driver interface for the robot. """
    driver = None
    path_driver = None
    path_assets = None
    environment = 'local'

    def __init__(self, path_driver, path_assets, environment):
        self.path_driver = path_driver
        self.path_assets = path_assets
        self.environment = environment

    @abstractmethod
    def set_driver(self):
        """ Set driver for the browser. """
        options_browser = self._get_options()
        self.driver = self._get_manager_driver(options_browser)

    @abstractmethod
    def set_driver_extension(self, path_extensions):
        """ Set driver for the browser. """
        options_browser = self._get_options()
        options_browser = self._get_extension_pre_config(options_browser)
        # options_browser = self._sign_extension(options_browser)
        self.driver = self._get_manager_driver(options_browser)

    @abstractmethod
    def _get_extension_pre_config(self, options_browser):
        """ Set driver for the browser. """
        options_browser.accept_untrusted_certs = True
        options_browser.accept_insecure_certs = True
        return options_browser

    @abstractmethod
    def _sign_extension(self, options_browser):
        """ Sign extension. """
        addon_id = "webextension@metamask.io"
        json_info = json.dumps({addon_id: str(uuid.uuid4())})
        options_browser.set_preference("extensions.webextensions.uuids", json_info)
        return options_browser

    @abstractmethod
    def get_driver(self):
        """ Get driver for the browser. """
        return self.driver

    @abstractmethod
    def _get_manager_driver(self, options_browser):
        match self.environment:
            case 'local':
                return self._get_driver_local(options_browser)
            case 'docker':
                return self._get_driver_docker(options_browser)
            case 'remote':
                return self._get_driver_remote(options_browser)
            case default:
                return None

    @abstractmethod
    def _get_driver_local(self, options_browser):
        service = self._get_service()
        # webdriver.Firefox or webdriver.Chrome

    @abstractmethod
    def _get_driver_docker(self, options_browser):
        # webdriver.Firefox or webdriver.Chrome
        return None

    @abstractmethod
    def _get_driver_remote(self, options_browser):
        remote_url = os.getenv("REMOTE_URL") or "http://selenium-hub:4444/wd/hub"
        return webdriver.Remote(
            command_executor=remote_url,
            options=options_browser
        )

    @abstractmethod
    def _get_service(self):
        # ServiceFirefox or ServiceChrome
        return None

    @abstractmethod
    def _get_options(self):
        options_browser = self._set_service_option()
        options_browser = self._get_options_general(options_browser)
        options_browser = self._get_manager_options(options_browser)
        return options_browser

    @abstractmethod
    def _set_service_option(self):
        # return webdriver.FirefoxOptions() webdriver.ChromeOptions()
        return None

    @abstractmethod
    def _get_manager_options(self, options_browser):
        match self.environment:
            case 'local':
                return self._get_options_local(options_browser)
            case 'docker':
                return self._get_options_docker(options_browser)
            case 'remote':
                return self._get_options_remote(options_browser)
            case default:
                return options_browser

    @abstractmethod
    def _get_options_general(self, options_browser):
        options_browser.add_argument("--lang=en-US")
        options_browser.add_argument("--disable-infobars")
        return options_browser

    @abstractmethod
    def _get_options_local(self, options_browser):
        options_browser.add_argument("--start-maximized")
        options_browser.add_argument("--disk-cache-size=1")
        options_browser.add_argument("--media-cache-size=1")
        options_browser.add_argument("--disable-application-cache")
        return options_browser

    @abstractmethod
    def _get_options_docker(self, options_browser):
        options_browser.add_argument("--headless")
        return options_browser

    @abstractmethod
    def _get_options_remote(self, options_browser):
        return options_browser
