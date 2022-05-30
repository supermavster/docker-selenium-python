# pylint: skip-file
"""
Driver Action Service
"""
import os
import time
from datetime import datetime as dt

from selenium.common.exceptions import TimeoutException as TE
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait as WDW


class DriverAction:
    """ This class is used to perform actions on the webdriver. """
    driver = None
    is_chrome = False
    is_firefox = False

    def __init__(self, driver, is_chrome, is_firefox):
        self.driver = driver
        self.is_chrome = is_chrome
        self.is_firefox = is_firefox

    def wait(self, seconds: int = 5) -> None:
        """ Wait for a certain amount of seconds. """
        try:
            WDW(self.driver, seconds).until(lambda _: True)
        except Exception as execption:
            print("error", execption)

    def set_setting_window(self, start_url="https://google.com"):
        """ Start the webdriver. """
        self.driver.get(start_url)
        # How many tabs
        handles = self.driver.window_handles
        size = len(handles)
        # Close other tabs if exist (Install extension)
        if size > 1:
            self.driver.close()

    def get_title(self):
        """ Get the title of the web page. """
        return self.driver.title if self.driver.title else ""

    def close_window(self) -> None:
        """ Try to close the webdriver. """
        try:
            self.driver.quit()
        except Exception as execption:
            print("error", execption)

    def is_exists_by_xpath(self, xpath, show_error=False):
        """ Check if an element exists by xpath. """
        try:
            # WDW(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, xpath)))
            self.driver.find_element(By.XPATH, xpath)
        except Exception as execption:
            if show_error:
                print("error", execption)
            return False
        return True

    def switch_to_main_window(self):
        """Switch to the main tab."""
        self.window_handles(0)

    def switch_to_popup_window(self):
        """ Switch to the MetaMask pop up tab. """
        self.window_handles(1)

    def switch_to_window(self, index: int):
        """ Switch to the MetaMask pop up tab. """
        self.window_handles(index)

    def switch_to_iframe(self, iframe):
        """ Switch to the MetaMask pop up tab. """
        self.driver.switch_to.frame(iframe)

    def switch_to_default_content(self):
        """ Switch to the MetaMask pop up tab. """
        self.driver.switch_to.default_content()

    def check_diff_current_vs_url(self, url):
        """ Check if the current url is the same as the url. """
        try:
            return WDW(self.driver, 5).until(lambda _: self.driver.current_url != url)
        except TE:
            print("Timeout while waiting for the upload page.")
            return False
        except Exception as execption:
            print("error", execption)
            return False

    def quit(self) -> None:
        """Stop the webdriver."""
        try:
            self.driver.quit()
        except Exception as execption:
            print("error", execption)

    def clickable(self, element: str, show_error=False) -> None:
        """Click on an element if it's clickable using Selenium."""
        try:
            WDW(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, element))
            ).click()
        except Exception as execption:
            if show_error:
                print("error", execption)
            self.clickable_js(element, show_error)

    def clickable_js(self, element: str, show_error=False) -> None:
        """ Click on an element if it's clickable using JavaScript."""
        try:
            # JavaScript can bypass this.
            self.driver.execute_script("arguments[0].click();", self.visible(element))
        except Exception as execption:
            if show_error:
                print("error", execption)

    def visible(self, element: str):
        """ Check if an element is visible using Selenium. """
        try:
            return WDW(self.driver, 15).until(
                EC.visibility_of_element_located((By.XPATH, element))
            )
        except Exception as execption:
            print("error", execption)
            return False

    def find_by_tag(self, element: str):
        """ Find an element by tag name. """
        try:
            return self.driver.find_element(By.TAG_NAME, element)
        except Exception as execption:
            print("error", execption)
            return []

    def find_all_by_tag(self, element: str):
        """ Find all elements by tag name. """
        try:
            return WDW(self.driver, 15).until(
                lambda _: self.driver.find_elements(By.TAG_NAME, element)
            )
        except Exception as execption:
            print("error", execption)
            return []

    def send_keys(self, element: str, keys: str) -> None:
        """ Send keys to an element if it's visible using Selenium. """
        try:
            self.visible(element).send_keys(keys)
        except Exception as execption:
            print("error", execption)
            WDW(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, element))
            ).send_keys(keys)

    def send_date(self, element: str, keys: str) -> None:
        """ Send a date (DD-MM-YYYY HH:MM) to a date input by clicking on it. """
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

    def clear_text(self, element, webdriver) -> None:
        """ Clear text from an input. """
        self.clickable(element)  # Click on the element then clear its text.
        # Note: change with 'darwin' if it's not working on MacOS.
        control = Keys.COMMAND if os.name == "posix" else Keys.CONTROL
        # ChromeDriver (Google Chrome).
        if self.is_chrome:
            webdriver.ActionChains(self.driver) \
                .key_down(control) \
                .send_keys('a') \
                .key_up(control) \
                .perform()
        # GeckoDriver (Mozilla Firefox).
        if self.is_firefox:
            self.send_keys(element, (control, 'a'))

    def is_empty(self, element: str, data: str, value: str = '') -> bool:
        """ Check if data is empty and input its value. """
        if data != value:  # Check if the data is not an empty string
            self.send_keys(element, data)  # or a default value, and send it.
            return False
        return True

    def wait_new_tab(self, windows):
        """ Wait for the new tab. """
        WDW(self.driver, 10).until(
            lambda _: windows != self.driver.window_handles)

    def wait_popup_close(self):
        """ Wait for the popup to close. """
        try:
            # Wait until the popup is closed.
            WDW(self.driver, 10).until(EC.number_of_windows_to_be(2))
            return True
        except TE:
            return False
        except Exception as execption:
            print("error", execption)
            return False

    def window_handles(self, window_number: int) -> None:
        """ Check for window handles and wait until a specific tab is opened. """
        WDW(self.driver, 15).until(
            lambda _: len(self.driver.window_handles) > window_number
        )
        # Switch to the asked tab.
        self.driver.switch_to.window(self.driver.window_handles[window_number])

    def select_by_value(self, xpath: str, value: str) -> None:
        """ Select an option by its value. """
        try:
            # Selenium <select> element.
            select = Select(self.visible(xpath))
            # Select the option by its value.
            select.select_by_value(value)
        except Exception as ex:
            print(ex)

    def wait_time(seconds: int = 5) -> None:
        """ Wait for a certain amount of seconds. """
        time.sleep(seconds)
