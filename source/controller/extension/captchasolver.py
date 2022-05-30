"""
CAPTCHA solver for the extension.
"""
import random
import time

from interface.extension.plugin_manager import PluginManager


def sleep_seconds():
    """Sleep seconds"""
    min_rand = 0.64
    max_rand = 1.27
    time.sleep(random.uniform(min_rand, max_rand))


class CaptchaSolver(PluginManager):
    """ CAPTCHA solver for the extension. """

    # Variables
    solver_challenge = False
    # Settings
    RECAPTCHA_PAGE_URL = "https://patrickhlauke.github.io/recaptcha"
    # RECAPTCHA_PAGE_URL = "https://www.google.com/recaptcha/api2/demo"
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

    def __init__(self, path_assets, browser="chrome",
                 driver_action=None, driver=None):
        self.path_assets = path_assets
        self.browser = browser
        self.driver_action = driver_action
        self.driver = driver

        self._init_variables()

        super().__init__(path_assets, browser, driver)

    def _init_variables(self):
        self.download_extension = None
        self.path_data = f"{self.path_assets}/{self.path_data}"

    def set_test_url(self):
        """Set the test url"""
        self.driver_action.set_setting_window(self.RECAPTCHA_PAGE_URL)
        sleep_seconds()

    def resolve(self):
        """Resolve the captcha Google"""
        if self._check_webdriver():
            self._resolve_captcha()

    def _check_webdriver(self):
        if self.driver_action is None or self.driver is None:
            return False
        if self.driver_action and self.driver:
            return True
        return False

    def _resolve_captcha(self):
        self._start_tries()

    def _start_tries(self):
        counter = 0
        number_of_iterations = 10
        for i in range(number_of_iterations):
            if self.solver_challenge:
                break

            if self._check_exist_captcha():
                self._solve()
                counter += 1
            else:
                break
            print(f"Successful breaks: {counter} - {i}")

        print(f"Total successful breaks: {counter}")

    def _check_exist_captcha(self):
        return self.driver_action.visible("//iframe[contains(@src,'recaptcha')]") or False

    def _solve(self):
        # Get a ReCaptcha Challenge
        if self._get_recaptcha_challenge():
            # Switch to page's main frame
            self.driver_action.switch_to_default_content()
            # Get audio challenge
            check_challenge = self._get_audio_challenge()
            if check_challenge:
                self.solver_challenge = check_challenge
            # Switch to the ReCaptcha iframe to verify it is solved
            self.driver_action.switch_to_default_content()

    def _get_recaptcha_challenge(self):
        iframes = self._get_all_iframes()
        if self._switch_recaptcha_iframe(iframes):
            self._click_recaptcha_checkbox()
            return self._check_recaptcha_has_challenge()
        return False

    def _get_all_iframes(self):
        iframes = self.driver_action.find_all_by_tag('iframe')
        if len(iframes) > 0:
            return iframes
        return []

    def _switch_recaptcha_iframe(self, iframes):
        # Switch focus to ReCaptcha iframe
        self.driver_action.switch_to_iframe(iframes[0])
        check_exist = self.driver_action.is_exists_by_xpath(
            '//div[@class="recaptcha-checkbox-checkmark" and @role="presentation"]')
        if not check_exist:
            print("No element in the frame!!")
        return check_exist

    def _click_recaptcha_checkbox(self):
        xpath = '//div[@class="recaptcha-checkbox-border"]'
        if self.driver_action.is_exists_by_xpath(xpath):
            self.driver_action.clickable(xpath)

    def _check_recaptcha_has_challenge(self):
        # Check if the ReCaptcha has no challenge
        exist = self.driver_action.is_exists_by_xpath('//span[@aria-checked="true"]')
        if exist:
            print("ReCaptcha has no challenge. Trying again!")
        return not exist

    def _get_audio_challenge(self):
        # Get all the iframes on the page again
        iframes = self._get_all_iframes()
        # Switch to the last iframe (the new one)
        self.driver_action.switch_to_iframe(iframes[-1])
        # Check and press Audio challenge button
        if self._check_audio_button():
            if not self._check_submit_button():
                return True

        return self._check_recaptcha_audio_button()

    def _check_recaptcha_audio_button(self):
        if not self._check_button('//button[@id="recaptcha-audio-button"]'):
            print("No element of audio challenge!!")
            return False
        return True

    def _check_audio_button(self):
        # Check if the audio challenge button is present
        rule_first = "contains(@class, 'button-holder')"
        rule_second = "contains(@class, 'help-button-holder')"
        xpath = f"//div[{rule_first} and {rule_second}]"
        # Check Audio Button
        check_exist = self._check_button(xpath)
        if check_exist:
            # Click on the Audio Button
            self._click_button(xpath)
        return check_exist

    def _check_submit_button(self):
        # Check again button is present
        rule_first = "contains(@class, 'rc-button-default')"
        rule_second = "contains(@class, 'goog-inline-block')"
        xpath = f"//*[{rule_first} and {rule_second}]"
        # Check Audio Button
        check_exist = self._check_button(xpath)
        if check_exist:
            # Click on the Audio Button
            self._click_button(xpath)
        return check_exist

    def _check_button(self, xpath):
        check_exist = self.driver_action.is_exists_by_xpath(xpath)
        if not check_exist:
            print("No exist button")
        return check_exist

    def _click_button(self, xpath):
        self.driver_action.clickable(xpath)
