import random
import time

from interface.plugin_manager import PluginManager


class CaptchaSolver(PluginManager):
    # Randomization Related
    MIN_RAND = 0.64
    MAX_RAND = 1.27
    LONG_MIN_RAND = 4.78
    LONG_MAX_RAND = 11.1
    # Settings
    NUMBER_OF_ITERATIONS = 10
    RECAPTCHA_PAGE_URL = "https://patrickhlauke.github.io/recaptcha"
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

    def __init__(self, path_asset, webdriver=None, browser="Chrome"):
        super().__init__(path_asset, webdriver, browser)

    def _check_exist_captcha(self):
        return self.driver.visible("//iframe[contains(@src,'recaptcha')]")

    def set_test_url(self, webdriver=None):
        if webdriver is not None:
            self.set_web_driver(webdriver)
        # Navigate to a ReCaptcha page
        self.driver.get(self.RECAPTCHA_PAGE_URL)
        time.sleep(random.uniform(self.MIN_RAND, self.MAX_RAND))

    def get_recaptcha_challenge(self):
        while 1:

            # Get all the iframes on the page
            iframes = self.driver.find_elements_by_tag_name("iframe")

            # Switch focus to ReCaptcha iframe
            if len(iframes) > 0:
                self.driver.switch_to.frame(iframes[0])
                time.sleep(random.uniform(self.MIN_RAND, self.MAX_RAND))

            # Verify ReCaptcha checkbox is present
            if not self.webdriver.is_exists_by_xpath(
                    '//div[@class="recaptcha-checkbox-checkmark" '
                    "and "
                    '@role="presentation"]'
            ):
                message = f"[{self.current_iteration}] "
                print(message + "No element in the frame!!")
                continue

            # Click on ReCaptcha checkbox
            xpath = '//div[@class="recaptcha-checkbox-border"]'
            if self.webdriver.is_exists_by_xpath(xpath):
                try:
                    self.driver.find_element_by_xpath(xpath).click()
                    time.sleep(random.uniform(self.LONG_MIN_RAND, self.LONG_MAX_RAND))
                except Exception as e:
                    print(e)
                    continue

            # Check if the ReCaptcha has no challenge
            xpath = '//span[@aria-checked="true"]'
            exist = self.webdriver.is_exists_by_xpath(xpath)
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
        if not self.webdriver.is_exists_by_xpath(
                "//div[contains(@class, 'button-holder') "
                "and "
                "contains(@class, 'help-button-holder')]"
        ):
            print(f"[{self.current_iteration}] No class=button-holder!!")
        else:
            message = f"[{self.current_iteration}]"
            print(message + "Clicking on Plugin challenge")
            if self.webdriver.is_exists_by_xpath(
                    "//div[contains(@class, 'button-holder') "
                    "and "
                    "contains(@class, 'help-button-holder')]"
            ):
                self.driver.find_element_by_xpath(
                    "//div[contains(@class, 'button-holder') "
                    "and "
                    "contains(@class, 'help-button-holder')]"
                ).click()

            time.sleep(random.uniform(self.LONG_MIN_RAND, self.LONG_MAX_RAND))

            if self.webdriver.is_exists_by_xpath(
                    "//*[contains(@class, 'rc-button-default') "
                    "and "
                    "contains(@class, 'goog-inline-block')]"
            ):
                self.driver.find_element_by_xpath(
                    "//*[contains(@class, 'rc-button-default') "
                    "and "
                    "contains(@class, 'goog-inline-block')]"
                ).click()
            else:
                return True

        # Check if the audio challenge button is present
        if not self.webdriver.is_exists_by_xpath(
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
        iframes = self.driver.find_elements_by_tag_name("iframe")
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
        if self.driver is None or self.webdriver is None:
            return False
        if self.webdriver and self.driver:
            return True

    def resolve_captcha(self):
        if self._check_exist_captcha():
            self._start_tries()

    def resolve(self, webdriver=None):
        """Resolve the captcha Google"""
        if webdriver is not None:
            self.set_web_driver(webdriver)
        if self._check_webdriver():
            self.resolve_captcha()


# Test
def main():
    import os

    # Env
    from dotenv import load_dotenv
    load_dotenv()

    # Get path asset
    path_asset = os.path.dirname(os.path.abspath(__file__))
    path_asset = path_asset.replace("controller/extension", "assets")
    # Install with Chrome/Firefox
    browser = 'chrome'  # 'Firefox'
    # browser = 'firefox'  # Chrome
    captcha_solver = CaptchaSolver(path_asset, browser=browser)
    captcha_solver.start()
    path_extension = captcha_solver.get_path_extension()
    from controller.web_driver import WebDriver
    web_driver = WebDriver(path_asset, browser)
    web_driver.config_driver([path_extension])
    driver = web_driver.get_driver()
    captcha_solver.set_web_driver(web_driver, driver)
    # Test Solvent
    captcha_solver.set_test_url(web_driver)
    captcha_solver.resolve()
    driver.close()


if __name__ == '__main__':
    main()
