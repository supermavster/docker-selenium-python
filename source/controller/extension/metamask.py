import time

from selenium.common.exceptions import TimeoutException as TE
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as WDW

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

    def __init__(self, path_assets, driver_manager=None, driver=None, browser="chrome"):
        self.password = None
        self.recovery_phrase = None
        self.download_extension = None
        self.path_assets = path_assets
        self.driver_manager = driver_manager
        self.driver = driver
        self.browser = browser
        self.path_data = f"{self.path_assets}/{self.path_data}"
        super().__init__(path_assets, driver_manager, driver, browser)

    # Init Process
    def ask_passwords(self):
        question = "What is your MetaMask password?"
        self.password = ""
        #     Complement.save_file_question(
        #     self.path_data, "password", question
        # )
        question = "What is your MetaMask recovery phrase?"
        self.recovery_phrase = ""
        #     Complement.save_file_question(
        #     self.path_data, "recovery_phrase", question
        # )

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
            self.driver_manager.window_handles(0)
            print("Login to MetaMask.")
            # Reload the page to prevent a blank page.
            self.driver.refresh()
            print("Login to MetaMask.")
            # Click on the "Start" button.
            self.driver_manager.clickable('//*[@class="welcome-page"]/button')
            print("Login to MetaMask.")
            # # Click on the "Import wallet" button.
            self.driver_manager.clickable(
                '//*[contains(@class, "btn-primary")][position()=1]'
            )
            print("Login to MetaMask.")
            # Click on the "I agree" button.
            self.driver_manager.clickable("//footer/button[2]")
            # Input the recovery phrase.
            xpath = "//input[position()=1]"
            self.driver_manager.send_keys(xpath, self.recovery_phrase)
            # Input a new password or the same password of your account.
            self.driver_manager.send_keys('//*[@id="password"]', self.password)
            xpath = '//*[@id="confirm-password"]'
            self.driver_manager.send_keys(xpath, self.password)
            # Click on the "I have read and agree to the..." checkbox.
            self.driver_manager.clickable('(//*[@role="checkbox"])[2]')
            # Click on the "Import" button.
            self.driver_manager.clickable(
                '//*[contains(@class, "btn-primary")][position()=1]'
            )
            # Wait until the login worked and click on the "All done" button".
            xpath = '//*[contains(@class, "emoji")][position()=1]'
            self.driver_manager.visible(xpath)
            self.driver_manager.clickable(
                '//*[contains(@class, "btn-primary")][position()=1]'
            )
            print("Logged to MetaMask.")
        except Exception as ex:  # Failed - a web element is not accessible.
            print("Login to MetaMask failed, retrying...", ex)
            # self.metamask_login()

    def contract(self) -> None:
        """Sign a MetaMask contract to login to OpenSea."""
        # Click on the "Sign" button - Make a contract link.
        self.driver_manager.clickable('//button[text()="Sign"]')
        try:  # Wait until the MetaMask pop up is closed.
            WDW(self.driver, 5).until(EC.number_of_windows_to_be(1))
        except TE:
            self.contract()  # Sign the contract a second time.
        # Check window was already closed
        self.driver_manager.window_handles(0)  # Switch back to the OpenSea tab.


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

    metamask = MetaMask(path_asset, browser=browser)
    metamask.start()
    path_extension = metamask.get_path_extension()
    web_driver = WebDriver(path_asset, browser, True)
    web_driver.config_driver([path_extension])
    driver_manager = web_driver.get_driver_manager()
    driver = web_driver.get_driver()
    metamask.set_driver(driver_manager, driver)
    # Open metamask extension in chrome
    metamask.login()
    driver.close()


if __name__ == '__main__':
    main()
