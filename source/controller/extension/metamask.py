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
        self.fails = 0
        self.private_key = None
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
    def set_passwords(self, password: str = None, recovery_phrase: str = None) -> None:
        question = "What is your MetaMask password?"
        self.password = password
        question = "What is your MetaMask recovery phrase?"
        self.recovery_phrase = recovery_phrase

    def start(self):
        # self.ask_passwords()
        if self.browser_is_firefox():
            self.url_extension = self.download_extension.get_url_extension(
                self.data_extension_firefox
            )
        self.install()

    # Selenium Process

    def login(self):
        """Login to the MetaMask extension."""
        try:
            # Switch to the MetaMask extension tab.
            self.driver_manager.window_handles(0)
            # Prevent a blank page.
            self.driver.refresh()
            # Click on the "Start" button.
            self.driver_manager.clickable('//*[@class="welcome-page"]/button')
            # Click on the "Import wallet" button.
            self.driver_manager.clickable('//*[contains(@class, "btn-primary")][position()=1]')
            # Click on the "I agree" button.
            self.driver_manager.clickable('//footer/button[2]')
            # Put the password
            self._set_data_password()
            # Wait until the login worked and click on the "All done" button.
            self.driver_manager.visible('//*[contains(@class, "emoji")][position()=1]')
            # Confirm the connection to MetaMask.
            self.driver_manager.clickable('//*[contains(@class, "btn-primary")][position()=1]')
            # Set Private Key
            self._set_private_key()
        except (Exception,):  # Failed - a web element is not accessible.
            self.fails += 1  # Increment the counter.
            if self.fails < 2:  # Retry login to the MetaMask.
                self.login()
            else:  # Failed twice - the wallet is not accessible.
                self.driver.quit()  # Stop the webdriver.

    def _set_data_password(self):
        # If a recovery phrase and password are set.
        if self.recovery_phrase != '' and self.password != '':
            # Count the words in the recovery phrase.
            split_recovery_phrase = self.recovery_phrase.split(" ")
            count = len(split_recovery_phrase)
            # Select by length the recovery phrase.
            self.driver_manager.select_by_value('//select[contains(@class, "dropdown__select")]', count)
            # Put the recovery phrase.
            for i in range(count):
                # Get the word.
                word = split_recovery_phrase[i]
                # Set the word.
                self.driver_manager.send_keys(f'//*[@id="import-srp__srp-word-{i}"]', word)
            # Input a password of your account.
            for path in ('//*[@id="password"]', '//*[@id="confirm-password"]'):
                self.driver_manager.send_keys(path, self.password)
            # Click on the "I have read and agree to the..." checkbox.
            self.driver_manager.clickable('(//*[@id="create-new-vault__terms-checkbox"])[1]')
            # Click on the "Import" button.
            self.driver_manager.clickable('//*[contains(@class, "btn-primary")][position()=1]')

    def _set_private_key(self):
        if self.private_key is not None:  # Change account.
            self.driver_manager.clickable('//button[@data-testid="popover-close"]')
            self.driver_manager.clickable(  # Click on the menu icon.
                '//*[@class="account-menu__icon"][position()=1]')
            self.driver_manager.clickable('//*[contains(@class, "account-menu__item--'
                                          'clickable")][position()=2]')
            self.driver_manager.send_keys(  # Input the private key.
                '//*[@id="private-key-box"]', self.private_key)
            self.driver_manager.clickable('//*[contains(@class, "btn-secondary")]'
                                          '[position()=1]')

    def sign(self, contract: bool = True, page: int = 2) -> None:
        """Sign the MetaMask contract to login to OpenSea."""
        windows = self.driver_manager.driver.window_handles  # Opened windows.
        for _ in range(page):  # "Next" and "Connect" buttons.
            self.driver_manager.window_handles(2)  # Switch to the MetaMask pop up tab.
            self.driver_manager.clickable('//*[contains(@class, "btn-primary")]')
        if contract:
            self.driver_manager.wait_new_tab(windows)
            self.contract()  # Sign the contract.

    def contract(self, new_contract: bool = False) -> None:
        """Sign a MetaMask contract to upload or confirm sale."""
        self.driver_manager.window_handles(2)  # Switch to the MetaMask pop up tab.
        if self.driver_manager.window == 1 and new_contract:  # GeckoDriver.
            self.driver_manager.clickable('(//div[contains(@class, "signature") and '
                                          'contains(@class, "scroll")])[position()=1]')
        self.driver_manager.driver.execute_script(  # Scroll down.
            'window.scrollTo(0, document.body.scrollHeight);')
        # Click on the "Sign" button - Make a contract link.
        self.driver_manager.clickable('(//div[contains(@class, "signature") and contains(@class, "footer")])'
                                      '[position()=1]/button[2]')
        if not self.driver_manager.wait_popup_close():
            # Sign the contract a second time.
            self.contract()
        # Switch back to the OpenSea tab.
        self.driver_manager.window_handles(1)

    def close(self) -> None:
        """Close the MetaMask popup."""
        if len(self.driver_manager.driver.window_handles) > 2:
            try:
                self.driver_manager.window_handles(2)  # Switch to the MetaMask popup.
                self.driver.close()  # Close the popup extension.
                self.driver_manager.window_handles(1)  # Switch back to OpenSea.
            except (Exception,):
                pass  # Ignore the exception.


## Test
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
#     # browser = 'firefox'# Chrome
#
#     metamask = MetaMask(path_asset, browser=browser)
#     metamask.start()
#     path_extension = metamask.get_path_extension()
#     web_driver = WebDriver(path_asset, browser, True)
#     web_driver.config_driver([path_extension])
#     web_driver.start()
#     driver_manager = web_driver.get_driver_manager()
#     driver = web_driver.get_driver()
#     metamask.set_driver(driver_manager, driver)
#     # Open metamask extension in chrome
#     keys = os.getenv('METAMASK_AUTH')
#     keys = keys.replace('[', '').replace(']', '').replace('"', '').replace(', ', ',').replace(' ,', ',').split(',')
#     metamask.set_passwords(keys[0], keys[1])
#     metamask.login()
#     driver.close()
#
#
# if __name__ == '__main__':
#     main()
