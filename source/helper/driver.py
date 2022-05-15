import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ServiceChrome
from selenium.webdriver.firefox.service import Service as ServiceFirefox

from source.helper.complement import Complement


class Driver:
    driver = None
    browser = None
    path_driver = None
    is_chrome = False
    is_firefox = False

    def __init__(self, browser, path_driver, path_assets, extension_path=None):
        self.browser = browser
        self.is_chrome = Complement.browser_is_chrome(browser)
        self.is_firefox = Complement.browser_is_firefox(browser)
        self.path_driver = path_driver
        self.path_assets = path_assets
        self.configuration(extension_path)

    def get_driver(self):
        return self.driver

    def configuration(self, extension_path=None):
        environment = os.environ.get('ENVIRONMENT') or 'docker'
        service = self._get_service()
        options = self._get_options(environment)
        self.setting_driver(environment, service, options, extension_path)
        # self.set_setting_window()

    def setting_driver(self, environment, service, options, extension_path=None):
        profile = None
        if extension_path:
            options, profile = self._install_extension(extension_path)

        if environment == 'local':
            self.driver = self._get_driver_object(service, options)
        elif environment == 'remote':
            self.driver = self._get_remote_driver_object(options)
        elif environment == 'docker':
            self.driver = self._get_driver_single(options)

        # Exception Firefox (Addon)
        if extension_path and Complement.browser_is_firefox(self.browser):
            self.driver.profile = profile
            for extension in extension_path:
                self.driver.install_addon(extension)

        self.driver.maximize_window()

    def _install_extension(self, extension_path):
        profile = None
        options_browser = self._get_options()
        for extension in extension_path:
            if self.is_chrome:
                # options_browser
                #   .add_argument(f'--load-extension = {extension}')
                options_browser.add_extension(extension)
            elif self.is_firefox:
                profile = webdriver.FirefoxProfile()
                profile.add_extension(extension)
                profile.accept_untrusted_certs = True
                profile.assume_untrusted_cert_issuer = True
                policy = "security.fileuri.strict_origin_policy"
                profile.set_preference(policy, False)
                profile.update_preferences()

        return options_browser, profile

    def _get_service(self):
        service_browser = None
        if self.is_chrome:
            service_browser = ServiceChrome(self.path_driver)
        elif self.is_firefox:
            log_path = f"{self.path_assets}/log"
            Complement.make_folder(log_path)
            service_browser = ServiceFirefox(executable_path=self.path_driver, log_path=f"{log_path}/firefox.log")
        return service_browser

    def _get_options(self, environment):
        options_browser = self.set_service_option()

        options_browser.add_argument("--no-sandbox")
        options_browser.add_argument("--disable-dev-shm-usage")

        if environment == 'local':
            arg = "--disable-blink-features=AutomationControlled"
            options_browser.add_argument(arg)
            options_browser.add_argument("--start-maximized")
            options_browser.add_argument("--disable-gpu")
            options_browser.add_argument("--no-first-run")
            options_browser.add_argument("--no-service-autorun")
            options_browser.add_argument("--password-store=basic")
            options_browser.add_argument("--disk-cache-size=1")
            options_browser.add_argument("--media-cache-size=1")
            options_browser.add_argument("--disable-application-cache")
            options_browser.add_argument("--disable-infobars")
            options_browser.add_argument("--log-level=3")
            options_browser.add_argument("--lang=en-US")
            options_browser = self._set_special_options(options_browser)
        elif environment == 'docker':
            options_browser.add_argument("--headless")

        return options_browser

    def set_service_option(self):
        options_browser = None
        if self.is_chrome:
            options_browser = webdriver.ChromeOptions()
        elif self.is_firefox:
            options_browser = webdriver.FirefoxOptions()
        return options_browser

    def _set_special_options(self, options_browser):
        if self.is_chrome:
            import os

            options_browser.add_experimental_option(
                "excludeSwitches", ["enable-logging"]
            )
            options_browser.add_experimental_option(
                "prefs",
                {
                    "intl.accept_languages": "en,en_US",
                    "download.default_directory": os.getcwd(),
                    "download.prompt_for_download": False,
                },
            )
            options_browser.add_experimental_option(
                "excludeSwitches", ["enable-automation"]
            )
            auto = "useAutomationExtension"
            options_browser.add_experimental_option(auto, False)
        elif self.is_firefox:
            import uuid
            import json

            options_browser.accept_insecure_certs = True
            addon_id = "webextension@metamask.io"
            addon_dyn_id = str(uuid.uuid4())
            json_info = json.dumps({addon_id: addon_dyn_id})
            preference = "extensions.webextensions.uuids"
            options_browser.set_preference(preference, json_info)

        return options_browser

    def _get_driver_object(self, service, options=None):
        if self.is_chrome:
            return webdriver.Chrome(service=service, options=options)
        elif self.is_firefox:
            return webdriver.Firefox(service=service, options=options)

    def _get_driver_single(self, options):
        if self.is_chrome:
            return webdriver.Chrome(options=options)
        elif self.is_firefox:
            return webdriver.Firefox(options=options)

    def _get_remote_driver_object(self, options=None):
        remote_url = os.getenv("REMOTE_URL") or "http://localhost:4444/wd/hub"
        return webdriver.Remote(
            command_executor=remote_url,
            options=options
        )

    def set_setting_window(self):
        self.driver.get("https://google.com")
        # How many tabs
        handles = self.driver.window_handles
        size = len(handles)
        # Close other tabs if exist (Install extension)
        if size > 1:
            self.driver.close()

# # TEST
# def main():
#     import os
#
#     # Get path asset
#     path_asset = os.path.dirname(os.path.abspath(__file__))
#     path_asset = path_asset.replace("helper", "assets")
#     path_driver = f"{path_asset}/driver/"
#     browser = "chrome"
#
#     if Complement.browser_is_chrome(browser):
#         path_driver = f"{path_driver}chromedriver"
#     elif Complement.browser_is_firefox(browser):
#         path_driver = f"{path_driver}geckodriver"
#
#     driver = Driver(browser, path_driver, path_asset)
#     print(driver.path_driver)
#
#
# if __name__ == '__main__':
#     main()
