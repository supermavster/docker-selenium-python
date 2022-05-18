import os
from datetime import datetime as dt

from selenium import webdriver
from selenium.common.exceptions import TimeoutException as TE
from selenium.webdriver.chrome.service import Service as ServiceChrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service as ServiceFirefox
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait as WDW
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.firefox_profile import AddonFormatError

from helper.complement import Complement

class FirefoxProfileWithWebExtensionSupport(webdriver.FirefoxProfile):
    def _addon_details(self, addon_path):
        try:
            return super()._addon_details(addon_path)
        except AddonFormatError:
            try:
                with open(os.path.join(addon_path, 'manifest.json'), 'r') as f:
                    manifest = json.load(f)
                    print(manifest)
                    return {
                        'id': manifest['applications']['gecko']['id'],
                        'version': manifest['version'],
                        'name': manifest['name'],
                        'unpack': True,
                    }
            except (IOError, KeyError) as e:
                raise AddonFormatError(str(e), sys.exc_info()[2])

class DriverManager:
    environment = None
    driver = None
    browser = None
    path_driver = None
    is_chrome = False
    is_firefox = False

    def __init__(self, browser, path_driver, path_assets, extension_path=None):
        self.browser = browser
        self.path_assets = path_assets
        self.path_driver = path_driver
        self.is_chrome = Complement.browser_is_chrome(browser)
        self.is_firefox = Complement.browser_is_firefox(browser)
        self.environment = os.environ.get('ENVIRONMENT') or 'local'

    def get_driver(self):
        return self.driver

    def configuration(self, extension_path=None):
        service = self._get_service()
        options = self._get_options()
        self.setting_driver(service, options, extension_path)

    def configure_single(self):
        service = self._get_service()
        options = self._get_options()
        self._set_driver(options, service)

    def setting_driver(self, service, options, extension_path=None):
        profile = None
        if extension_path:
            options, profile = self._install_extension(extension_path)

        self._set_driver(options, service, profile)

        # Exception Firefox (Addon)
        if extension_path and self.is_firefox:
            # self.driver.profile = profile
            # if self.environment != 'remote':
            for extension in extension_path:
                print(extension)
                self.driver.install_addon(extension)

        self.driver.maximize_window()

    def _set_driver(self, options, service, profile=None):
        if self.environment == 'local':
            self.driver = self._get_driver_object(service, options)
        elif self.environment == 'remote':
            self.driver = self._get_remote_driver_object(options, profile)
        elif self.environment == 'docker':
            self.driver = self._get_driver_single(options)

    def get_adblock_profile(config):
        ffprofile = FirefoxProfileWithWebExtensionSupport()
        ffprofile.add_extension(adblockfile)
        return ffprofile

    def _install_extension(self, extension_path):
        profile = None
        options_browser = self._get_options()
        for extension in extension_path:
            if self.is_chrome:
                # options_browser
                #   .add_argument(f'--load-extension = {extension}')
                options_browser.add_extension(extension)
            elif self.is_firefox:
                if self.environment == 'remote':
                    profile = FirefoxProfileWithWebExtensionSupport()
                else:
                    profile = webdriver.FirefoxProfile()
                profile.add_extension(extension)
                profile.set_preference("plugin.state.flash", 2)
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

    def _get_options(self):
        options_browser = self.set_service_option()

        options_browser.add_argument("--no-sandbox")
        options_browser.add_argument("--disable-dev-shm-usage")

        if self.environment == 'local':
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
        elif self.environment == 'docker' or self.environment == 'remote':
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
            options_browser.add_argument('--disable-popup-blocking')

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

    def _get_remote_driver_object(self, options, profile):
        remote_url = os.getenv("REMOTE_URL") or "http://selenium-hub:4444/wd/hub"
        return webdriver.Remote(
            command_executor=remote_url,
            options=options,
            browser_profile=profile
        )

    def set_setting_window(self):
        # self.driver.get("https://google.com")
        self.driver.get("about:addons")
        # How many tabs
        handles = self.driver.window_handles
        size = len(handles)
        # Close other tabs if exist (Install extension)
        if size > 1:
            self.driver.close()

    def close_window(self) -> None:
        """Try to close the webdriver."""
        try:
            self.driver.quit()
        except Exception as e:
            print("error", e)

    def is_exists_by_xpath(self, xpath):
        try:
            # WDW(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, xpath)))
            self.driver.find_element(By.XPATH, xpath)
        except Exception as e:
            print("error", e)
            return False
        return True

    def switch_to_main_window(self):
        """Switch to the main tab."""
        self.window_handles(0)

    def switch_to_popup_window(self):
        """Switch to the MetaMask pop up tab."""
        self.window_handles(1)

    def switch_to_window(self, index: int):
        """Switch to the MetaMask pop up tab."""
        self.window_handles(index)

    def check_diff_current_vs_url(self, url):
        try:
            return WDW(self.driver, 5).until(lambda _: self.driver.current_url != url)
        except TE:
            print("Timeout while waiting for the upload page.")
            return False
        except Exception as e:
            print("error", e)
            return False

    def quit(self) -> None:
        """Stop the webdriver."""
        try:
            self.driver.quit()
        except Exception as e:
            print("error", e)

    def clickable(self, element: str) -> None:
        """Click on an element if it's clickable using Selenium."""
        try:
            WDW(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, element))
            ).click()
        except Exception as e:
            print("error", e)
            # JavaScript can bypass this.
            self.driver.execute_script("arguments[0].click();", self.visible(element))

    def visible(self, element: str):
        """Check if an element is visible using Selenium."""
        try:
            return WDW(self.driver, 15).until(
                EC.visibility_of_element_located((By.XPATH, element))
            )
        except Exception as e:
            print("error", e)
            return False

    def send_keys(self, element: str, keys: str) -> None:
        """Send keys to an element if it's visible using Selenium."""
        try:
            self.visible(element).send_keys(keys)
        except Exception as e:
            print("error", e)
            WDW(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, element))
            ).send_keys(keys)

    def send_date(self, element: str, keys: str) -> None:
        """Send a date (DD-MM-YYYY HH:MM) to a date input by clicking on it."""
        # GeckoDriver (Mozilla Firefox).
        if self.is_firefox:
            self.send_keys(element, '-'.join(reversed(keys.split('-'))) if '-' in keys else keys)
        # ChromeDriver (Google Chrome).
        if self.is_chrome:
            keys = keys.split('-') if '-' in keys else [keys]
            keys = [keys[1], keys[0], keys[2]] if len(keys) > 1 else keys
            for part in range(len(keys) - 1 if keys[len(keys) - 1] == str(
                    dt.now().year) else len(keys)):  # Number of clicks.
                self.clickable(element)  # Click first on the element.
                self.send_keys(element, keys[part])  # Then send it the date.

    def clear_text(self, element) -> None:
        """Clear text from an input."""
        self.clickable(element)  # Click on the element then clear its text.
        # Note: change with 'darwin' if it's not working on MacOS.
        control = Keys.COMMAND if os.name == "posix" else Keys.CONTROL
        # ChromeDriver (Google Chrome).
        if self.is_chrome:
            webdriver.ActionChains(self.driver).key_down(control).send_keys('a').key_up(control).perform()
        # GeckoDriver (Mozilla Firefox).
        if self.is_firefox:
            self.send_keys(element, (control, 'a'))

    def is_empty(self, element: str, data: str, value: str = '') -> bool:
        """Check if data is empty and input its value."""
        if data != value:  # Check if the data is not an empty string
            self.send_keys(element, data)  # or a default value, and send it.
            return False
        return True

    def wait_new_tab(self, windows):
        """Wait for the new tab."""
        WDW(self.driver, 10).until(
            lambda _: windows != self.driver.window_handles)

    def wait_popup_close(self):
        try:
            """Wait until the popup is closed."""
            WDW(self.driver, 10).until(EC.number_of_windows_to_be(2))
            return True
        except TE:
            return False
        except Exception as e:
            print("error", e)
            return False

    def window_handles(self, window_number: int) -> None:
        """Check for window handles and wait until a specific tab is opened."""
        WDW(self.driver, 15).until(
            lambda _: len(self.driver.window_handles) > window_number
        )
        # Switch to the asked tab.
        self.driver.switch_to.window(self.driver.window_handles[window_number])

    def select_by_value(self, xpath: str, value: str) -> None:
        """Select an option by its value."""
        try:
            # Selenium <select> element.
            select = Select(self.visible(xpath))
            # Select the option by its value.
            select.select_by_value(value)
        except Exception as ex:
            print(ex)


# # TEST
# def main():
#     import os
#     # Env
#     from dotenv import load_dotenv
#     load_dotenv()
#     # Get path asset
#     path_asset = os.path.dirname(os.path.abspath(__file__))
#     path_asset = path_asset.replace("services", "assets")
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
