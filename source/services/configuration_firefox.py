import os

from selenium import webdriver

from helper.complement import Complement


class ConfigurationFirefox:
    driver = None
    path_driver = None
    path_assets = None
    environment = 'local'

    def __init__(self, path_driver, path_assets, environment):
        self.path_driver = path_driver
        self.path_assets = path_assets
        self.environment = environment

    def set_driver(self):
        options_browser = self._get_options()
        self.driver = self._get_manager_driver(options_browser)

    def set_driver_extension(self, path_extensions):
        options_browser = self._get_options()
        options_browser = self._get_extension_pre_config(options_browser)
        # options_browser = self._sign_extension(options_browser)
        self.driver = self._get_manager_driver(options_browser)
        self._set_extension_post_config(path_extensions)

    def _get_extension_pre_config(self, options_browser):
        options_browser.accept_untrusted_certs = True
        options_browser.accept_insecure_certs = True
        options_browser.set_preference('xpinstall.signatures.required', False)
        options_browser.set_preference('security.fileuri.strict_origin_policy', False)
        options_browser.set_preference("plugin.state.flash", 2)
        # options_browser.add_argument('--disable-popup-blocking')

        return options_browser

    # def _sign_extension(self, options_browser):
    #     import uuid
    #     import json
    #     addon_id = "webextension@metamask.io"
    #     json_info = json.dumps({addon_id: str(uuid.uuid4())})
    #     options_browser.set_preference("extensions.webextensions.uuids", json_info)
    #     return options_browser

    def _set_extension_post_config(self, path_extensions):
        for path_extension in path_extensions:
            self._set_manager_extension_post_config(path_extension)

    def _set_manager_extension_post_config(self, path_extension):
        match self.environment:
            case 'local':
                self._set_extension_post_local(path_extension)
            case 'docker':
                self._set_extension_post_docker(path_extension)
            case 'remote':
                self._set_extension_post_remote(path_extension)

    def _set_extension_post_local(self, path_extension):
        self.driver.install_addon(path_extension)

    def _set_extension_post_docker(self, path_extension):
        self.driver.install_addon(path_extension)

    def _set_extension_post_remote(self, path_extension):
        payload = {"path": path_extension, "temporary": True}
        # The function returns an identifier of the installed addon.
        var = self.driver.execute("INSTALL_ADDON", payload)["value"]
        # This identifier can later be used to uninstall installed addon.
        print(var)

    def get_driver(self):
        return self.driver

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

    def _get_driver_local(self, options_browser):
        service = self._get_service()
        return webdriver.Firefox(service=service, options=options_browser)

    def _get_driver_docker(self, options_browser):
        return webdriver.Firefox(options=options_browser)

    def _get_driver_remote(self, options_browser):
        remote_url = os.getenv("REMOTE_URL") or "http://selenium-hub:4444/wd/hub"
        return webdriver.Remote(
            command_executor=remote_url,
            options=options_browser
        )

    def _get_service(self):
        log_path = f"{self.path_assets}/log"
        Complement.make_folder(log_path)

        from selenium.webdriver.firefox.service import Service as ServiceFirefox
        return ServiceFirefox(executable_path=self.path_driver, log_path=f"{log_path}/firefox.log")

    def _get_options(self):
        options_browser = self._set_service_option()
        options_browser = self._get_options_general(options_browser)
        options_browser = self._get_manager_options(options_browser)
        return options_browser

    def _set_service_option(self):
        return webdriver.FirefoxOptions()

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

    def _get_options_general(self, options_browser):
        options_browser.add_argument("--lang=en-US")
        options_browser.add_argument("--disable-infobars")
        return options_browser

    def _get_options_local(self, options_browser):
        options_browser.add_argument("--start-maximized")
        options_browser.add_argument("--disk-cache-size=1")
        options_browser.add_argument("--media-cache-size=1")
        options_browser.add_argument("--disable-application-cache")
        return options_browser

    def _get_options_docker(self, options_browser):
        options_browser.add_argument("--headless")
        return options_browser

    def _get_options_remote(self, options_browser):
        return options_browser
