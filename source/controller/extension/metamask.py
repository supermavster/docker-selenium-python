from selenium.common.exceptions import TimeoutException as TE
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as WDW

import helpers.complement as Complement
from interface.plugin_manager import PluginManager


class MetaMask(PluginManager):
    path_assets = ""
    path_data = "wallets/metamask"
    # Chrome
    url_extension = (
        "https://chrome.google.com/webstore/detail/"
        "metamask/nkbihfbeogaeaoehlefnkodbefgpgknn"
    )
    # Firefox
    data_extension_firefox = {
        "url": "https://addons.mozilla.org/en-US/firefox/addon/ether-metamask",
        "collection_url": "https://addons.mozilla.org/en-US/firefox/"
        "addon/metamask-legacy-web3/",
        "user_id": [12436990, 13014139],
    }

    def __init__(self, path_assets, webdriver=None, browser="Chrome"):
        self.password = None
        self.recovery_phrase = None
        self.download_extension = None
        self.path_assets = path_assets
        self.webdriver = webdriver
        self.browser = browser
        self.path_data = f"{self.path_assets}/{self.path_data}"
        super().__init__(path_assets, webdriver, browser)

    # Init Process
    def ask_passwords(self):
        question = "What is your MetaMask password?"
        self.password = complement.save_file_question(
            self.path_data, "password", question
        )
        question = "What is your MetaMask recovery phrase?"
        self.recovery_phrase = complement.save_file_question(
            self.path_data, "recovery_phrase", question
        )

    def start(self):
        self.ask_passwords()
        if self.browser_is_firefox():
            self.url_extension = self.download_extension.get_url_extension(
                self.data_extension_firefox
            )
        self.install()

    # Selenium Process

    def login(self) -> None:
        """Login to the MetaMask extension."""
        try:  # Try to login to the MetaMask extension.
            print("Login to MetaMask.")
            # Get actual url.
            # Switch to the MetaMask extension tab.
            self.webdriver.window_handles(0)
            # Reload the page to prevent a blank page.
            self.webdriver.driver.refresh()
            # Click on the "Start" button.
            self.webdriver.clickable('//*[@class="welcome-page"]/button')
            # # Click on the "Import wallet" button.
            self.webdriver.clickable(
                '//*[contains(@class, "btn-primary")][position()=1]'
            )
            # Click on the "I agree" button.
            self.webdriver.clickable("//footer/button[2]")
            # Input the recovery phrase.
            xpath = "//input[position()=1]"
            self.webdriver.send_keys(xpath, self.recovery_phrase)
            # Input a new password or the same password of your account.
            self.webdriver.send_keys('//*[@id="password"]', self.password)
            xpath = '//*[@id="confirm-password"]'
            self.webdriver.send_keys(xpath, self.password)
            # Click on the "I have read and agree to the..." checkbox.
            self.webdriver.clickable('(//*[@role="checkbox"])[2]')
            # Click on the "Import" button.
            self.webdriver.clickable(
                '//*[contains(@class, "btn-primary")][position()=1]'
            )
            # Wait until the login worked and click on the "All done" button".
            xpath = '//*[contains(@class, "emoji")][position()=1]'
            self.webdriver.visible(xpath)
            self.webdriver.clickable(
                '//*[contains(@class, "btn-primary")][position()=1]'
            )
            print("Logged to MetaMask.")
        except Exception as ex:  # Failed - a web element is not accessible.
            print("Login to MetaMask failed, retrying...", ex)
            # self.metamask_login()

    def contract(self) -> None:
        """Sign a MetaMask contract to login to OpenSea."""
        # Click on the "Sign" button - Make a contract link.
        self.webdriver.clickable('//button[text()="Sign"]')
        try:  # Wait until the MetaMask pop up is closed.
            WDW(self.webdriver.driver, 5).until(EC.number_of_windows_to_be(1))
        except TE:
            self.contract()  # Sign the contract a second time.
        # Check window was already closed
        if len(self.webdriver.driver.window_handles) > 0:
            self.webdriver.window_handles(0)  # Switch back to the OpenSea tab.


# # Test
# def main():
#     # Install with Chrome/Firefox
#     browser = 'Chrome' # 'Firefox'
#     # browser = 'Firefox'# Chrome
#     metamask = MetaMask(browser=browser)
#     metamask.start()
#     path_extension = metamask.get_path_extension()
#     from helpers.web_driver import WebDriver
#     firefox_driver = WebDriver(browser)
#     driver = firefox_driver.get_driver([path_extension])
#     # Login
#     metamask.set_web_driver(firefox_driver, driver)
#     # Open metamask extension in chrome
#     metamask.login()
#     driver.close()
#
#
# if __name__ == '__main__':
#     main()