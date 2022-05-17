import random
import time

from selenium.webdriver.common.by import By

from interface.plugin_manager import PluginManager


class CaptchaSolver(PluginManager):
    # Randomization Related
    MIN_RAND = 0.64
    MAX_RAND = 1.27
    LONG_MIN_RAND = 4.78
    LONG_MAX_RAND = 11.1
    # Settings
    NUMBER_OF_ITERATIONS = 10
    # RECAPTCHA_PAGE_URL = "https://patrickhlauke.github.io/recaptcha"
    RECAPTCHA_PAGE_URL = "https://www.google.com/recaptcha/api2/demo"
    # Chrome
    url_extension = (
        "https://chrome.google.com/webstore/detail/"
        "buster-captcha-solver-for/"
        "mpbjkejclgfgadiemmefgebjfooflfhl"
    )
    # Firefox
    data_extension_firefox = {
        "user_id": [12929064],
        "url": "https://addons.mozilla.org/en-US/firefox/"
               "addon/buster-captcha-solver",
        "collection_url": "https://addons.mozilla.org/en-US/"
                          "firefox/addon/youtube-video-quality",
    }

    def __init__(self, path_assets, driver_manager=None, driver=None, browser="Chrome"):
        self.download_extension = None
        self.path_assets = path_assets
        self.driver_manager = driver_manager
        self.driver = driver
        self.browser = browser
        self.path_data = f"{self.path_assets}/{self.path_data}"
        super().__init__(path_assets, driver_manager, driver, browser)

    def set_test_url(self):
        # Navigate to a ReCaptcha page
        self.driver.get(self.RECAPTCHA_PAGE_URL)
        time.sleep(random.uniform(self.MIN_RAND, self.MAX_RAND))

    def _check_exist_captcha(self):
        return self.driver_manager.visible("//iframe[contains(@src,'recaptcha')]") or False

    def get_recaptcha_challenge(self):
        # Get all the iframes on the page
        iframes = self.driver.find_elements(By.TAG_NAME, "iframe")

        # Switch focus to ReCaptcha iframe
        if len(iframes) > 0:
            self.driver.switch_to.frame(iframes[0])
            time.sleep(random.uniform(self.MIN_RAND, self.MAX_RAND))

        # Verify ReCaptcha checkbox is present
        if not self.driver_manager.is_exists_by_xpath(
                '//div[@class="recaptcha-checkbox-checkmark" '
                "and "
                '@role="presentation"]'
        ):
            message = f"[{self.current_iteration}] "
            print(message + "No element in the frame!!")

        # Click on ReCaptcha checkbox
        xpath = '//div[@class="recaptcha-checkbox-border"]'
        if self.driver_manager.is_exists_by_xpath(xpath):
            try:
                self.driver_manager.clickable(xpath)
                time.sleep(random.uniform(self.LONG_MIN_RAND, self.LONG_MAX_RAND))
            except Exception as e:
                print(e)

        # Check if the ReCaptcha has no challenge
        xpath = '//span[@aria-checked="true"]'
        exist = self.driver_manager.is_exists_by_xpath(xpath)
        if exist:
            print(
                "[{0}] ReCaptcha has no challenge. Trying again!".format(
                    self.current_iteration
                )
            )
        else:
            return

    def get_audio_challenge(self, iframes):
        # Switch to the last iframe (the new one)
        self.driver.switch_to.frame(iframes[-1])
        # Check if the audio challenge button is present
        if not self.driver_manager.is_exists_by_xpath(
                "//div[contains(@class, 'button-holder') "
                "and "
                "contains(@class, 'help-button-holder')]"
        ):
            print(f"[{self.current_iteration}] No class=button-holder!!")
        else:
            message = f"[{self.current_iteration}]"
            print(message + "Clicking on Plugin challenge")
            if self.driver_manager.is_exists_by_xpath(
                    "//div[contains(@class, 'button-holder') "
                    "and "
                    "contains(@class, 'help-button-holder')]"
            ):
                self.driver_manager.clickable(
                    "//div[contains(@class, 'button-holder') "
                    "and "
                    "contains(@class, 'help-button-holder')]"
                )

            time.sleep(random.uniform(self.LONG_MIN_RAND, self.LONG_MAX_RAND))

            if self.driver_manager.is_exists_by_xpath(
                    "//*[contains(@class, 'rc-button-default') "
                    "and "
                    "contains(@class, 'goog-inline-block')]"
            ):
                self.driver_manager.clickable(
                    "//*[contains(@class, 'rc-button-default') "
                    "and "
                    "contains(@class, 'goog-inline-block')]"
                )
            else:
                return True

        # Check if the audio challenge button is present
        if not self.driver_manager.is_exists_by_xpath(
                '//button[@id="recaptcha-audio-button"]'
        ):
            message = f"[{self.current_iteration}]"
            print(message + "No element of audio challenge!!")
            return False

        print(f"[{self.current_iteration}] Clicking on audio challenge")
        # Click on the audio challenge button
        time.sleep(random.uniform(self.LONG_MIN_RAND, self.LONG_MAX_RAND))

        return True

    def _solve(self, current_iteration):
        self.current_iteration = current_iteration + 1
        # Get a ReCaptcha Challenge
        self.get_recaptcha_challenge()
        # Switch to page's main frame
        self.driver.switch_to.default_content()
        # Get all the iframes on the page again
        iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
        # Get audio challenge
        self.get_audio_challenge(iframes)
        # Switch to the ReCaptcha iframe to verify it is solved
        self.driver.switch_to.default_content()

    def _start_tries(self):
        counter = 0
        for i in range(self.NUMBER_OF_ITERATIONS):
            if self._check_exist_captcha():
                self._solve(i)
                counter += 1
                time.sleep(random.uniform(self.LONG_MIN_RAND, self.LONG_MAX_RAND))
            else:
                break
            print("Successful breaks: {0}".format(counter))
        message = f"{counter} - {self.NUMBER_OF_ITERATIONS}"
        print(f"Total successful breaks: {message}")

    def _check_webdriver(self):
        if self.driver_manager is None or self.driver is None:
            return False
        if self.driver_manager and self.driver:
            return True

    def resolve_captcha(self):
        if self._check_exist_captcha():
            self._start_tries()

    def resolve(self):
        """Resolve the captcha Google"""
        if self._check_webdriver():
            self.resolve_captcha()


# Test
def main():
    import os
    from controller.web_driver import WebDriver

    # Env
    from dotenv import load_dotenv
    load_dotenv()

    # Get path asset
    path_asset = os.path.dirname(os.path.abspath(__file__))
    path_asset = path_asset.replace("controller/extension", "assets")
    # Install with Chrome/Firefox
    browser = 'chrome'  # 'Firefox'
    # browser = 'Firefox'# Chrome

    captcha_solver = CaptchaSolver(path_asset, browser=browser)
    captcha_solver.start()
    path_extension = captcha_solver.get_path_extension()
    web_driver = WebDriver(path_asset, browser, True)
    web_driver.config_driver([path_extension])
    driver_manager = web_driver.get_driver_manager()
    driver = web_driver.get_driver()
    captcha_solver.set_driver(driver_manager, driver)
    # Test Solvent
    captcha_solver.set_test_url()
    captcha_solver.resolve()
    driver.close()


if __name__ == '__main__':
    main()
