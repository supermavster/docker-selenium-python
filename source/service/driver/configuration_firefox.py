# pylint: skip-file
"""
Configuration Firefox driver
"""
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as ServiceFirefox

from helper.complement import Complement
from interface.driver_interface import DriverInterface


class ConfigurationFirefox(DriverInterface):
    """ Configuration Firefox driver """

    def __init__(self, path_driver, path_assets, environment):
        super().__init__(path_driver, path_assets, environment)

    def set_driver_extension(self, path_extensions):
        """ Set driver extension """
        options_browser = self._get_options()
        options_browser = self._get_extension_pre_config(options_browser)
        # options_browser = self._sign_extension(options_browser)
        self.driver = self._get_manager_driver(options_browser)
        self._set_extension_post_config(path_extensions)

    def _get_extension_pre_config(self, options_browser):
        """ Get extension pre config """
        options_browser.accept_untrusted_certs = True
        options_browser.accept_insecure_certs = True
        options_browser.set_preference('xpinstall.signatures.required', False)
        options_browser.set_preference('security.fileuri.strict_origin_policy', False)
        options_browser.set_preference("plugin.state.flash", 2)
        # options_browser.add_argument('--disable-popup-blocking')

        return options_browser

    def _set_extension_post_config(self, path_extensions):
        """ Set extension post config """
        for path_extension in path_extensions:
            self._set_manager_extension_post_config(path_extension)

    def _set_manager_extension_post_config(self, path_extension):
        """ Set manager extension post config """
        match self.environment:
            case 'local':
                self._set_extension_post_local(path_extension)
            case 'docker':
                self._set_extension_post_docker(path_extension)
            case 'remote':
                self._set_extension_post_remote(path_extension)

    def _set_extension_post_local(self, path_extension):
        """ Set extension post local """
        self.driver.install_addon(path_extension)

    def _set_extension_post_docker(self, path_extension):
        """ Set extension post docker """
        self.driver.install_addon(path_extension)

    def _set_extension_post_remote(self, path_extension):
        """ Set extension post remote """
        payload = {"path": path_extension, "temporary": True}
        # The function returns an identifier of the installed addon.
        var = self.driver.execute("INSTALL_ADDON", payload)["value"]
        # This identifier can later be used to uninstall installed addon.
        print(var)

    def _get_driver_local(self, options_browser):
        """ Get driver local """
        service = self._get_service()
        return webdriver.Firefox(service=service, options=options_browser)

    def _get_driver_docker(self, options_browser):
        """ Get driver docker """
        return webdriver.Firefox(options=options_browser)

    def _get_service(self):
        """ Get service """
        log_path = f"{self.path_assets}/log"
        Complement.make_folder(log_path)

        return ServiceFirefox(executable_path=self.path_driver, log_path=f"{log_path}/firefox.log")

    def _set_service_option(self):
        """ Set service option """
        return webdriver.FirefoxOptions()
