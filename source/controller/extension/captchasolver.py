import random
import time

from interface.extension.plugin_manager import PluginManager


class CaptchaSolver(PluginManager):
    SOLVER_CHALLENGE = False
    # Randomization Related
    MIN_RAND = 0.64
    MAX_RAND = 1.27
    LONG_MIN_RAND = 4.78
    LONG_MAX_RAND = 11.1
    # Settings
    NUMBER_OF_ITERATIONS = 10
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

    def __init__(self, path_assets, browser="chrome", driver_manager=None, driver_action=None, driver=None):
        self.path_assets = path_assets
        self.browser = browser
        self.driver_manager = driver_manager
        self.driver_action = driver_action
        self.driver = driver

        self._init_variables()

        super().__init__(path_assets, browser, driver_manager, driver)

    def _init_variables(self):
        self.download_extension = None
        self.path_data = f"{self.path_assets}/{self.path_data}"

    def sleep_seconds(self):
        time.sleep(random.uniform(self.MIN_RAND, self.MAX_RAND))

    def set_test_url(self):
        self.driver_action.set_setting_window(self.RECAPTCHA_PAGE_URL)
        self.sleep_seconds()

    def resolve(self):
        """Resolve the captcha Google"""
        if self._check_webdriver():
            self._resolve_captcha()

    def _check_webdriver(self):
        if self.driver_action is None or self.driver is None:
            return False
        if self.driver_action and self.driver:
            return True

    def _resolve_captcha(self):
        self._start_tries()

    def _start_tries(self):
        counter = 0
        for i in range(self.NUMBER_OF_ITERATIONS):
            if self.SOLVER_CHALLENGE:
                break
            else:
                if self._check_exist_captcha():
                    self._solve()
                    self.current_iteration = i + 1
                    counter += 1
                else:
                    break
            print("Successful breaks: {0}".format(counter))
        message = f"{counter} - {self.NUMBER_OF_ITERATIONS}"
        print(f"Total successful breaks: {message}")

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
                self.SOLVER_CHALLENGE = check_challenge
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
            print(f"[{self.current_iteration}] ReCaptcha has no challenge. Trying again!")
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
        xpath = "//div[contains(@class, 'button-holder') and contains(@class, 'help-button-holder')]"
        # Check Audio Button
        check_exist = self._check_button(xpath)
        if check_exist:
            # Click on the Audio Button
            self._click_button(xpath)
        return check_exist

    def _check_submit_button(self):
        # Check again button is present
        xpath = "//*[contains(@class, 'rc-button-default') and contains(@class, 'goog-inline-block')]"
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

# # Test
# def main():
#     import os
#     from controller.web_driver import WebDriver
#
#     # Env
#     from dotenv import load_dotenv
#     load_dotenv()
#
#     # Get path asset
#     path_asset = os.path.dirname(os.path.abspath(__file__))
#     path_asset = path_asset.replace("controller/extension", "assets/")
#     # Install with Chrome/Firefox
#     browser = 'chrome'  # 'Firefox'
#     # browser = 'Firefox'# Chrome
#
#     captcha_solver = CaptchaSolver(path_asset, browser=browser)
#     captcha_solver.start()
#     path_extension = captcha_solver.get_path_extension()
#     web_driver = WebDriver(path_asset, browser, True)
#     web_driver.config_driver([path_extension])
#     driver_manager = web_driver.get_driver_manager()
#     driver = web_driver.get_driver()
#     captcha_solver.set_driver(driver_manager, driver)
#     # Test Solvent
#     captcha_solver.set_test_url()
#     captcha_solver.resolve()
#     driver.close()
#
#
# if __name__ == '__main__':
#     main()
