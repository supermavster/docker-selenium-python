"""
Extension Manager for the controller.
"""
import os

from controller.extension.captchasolver import CaptchaSolver
from controller.extension.metamask import MetaMask
from helper.complement import Complement


class ExtensionManager:
    """ Extension Manager for the controller. """
    path_assets = None
    browser = None
    driver_action = None
    driver = None
    wallet = None
    captcha = None
    extensions = []

    def __init__(self, path_assets, browser, driver_action=None, driver=None):
        self.path_assets = path_assets
        self.browser = browser
        self.driver_action = driver_action
        self.driver = driver
        self.set_extensions()

    def get_extensions(self):
        """ Get the extensions """
        return self.extensions

    def set_extensions(self):
        """ Set the extensions """
        self.extensions = []

        extensions = os.getenv('EXTENSIONS_' + self.browser.upper())
        if extensions is not None:
            extensions = Complement.convertENVArray(extensions)

            for extension in extensions:
                match extension:
                    case 'metamask':
                        self.start_wallet()
                    case 'captcha':
                        self.start_captcha()

    def start_captcha(self):
        """ Start the captcha """
        self.set_captcha()
        if self.captcha is not None:
            self.extensions.append(self.captcha.get_path_extension())

    def set_captcha(self):
        """ Set the captcha instance """
        self.captcha = CaptchaSolver(self.path_assets, self.browser,
                                     self.driver_action, self.driver)
        self.captcha.start()

    def get_captcha(self):
        """ Get the captcha instance """
        return self.captcha

    def start_wallet(self):
        """ Start the wallet """
        self.set_wallet()
        if self.wallet is not None:
            self.extensions.append(self.wallet.get_path_extension())

    def set_wallet(self):
        """ Set the wallet instance """
        self.wallet = MetaMask(self.path_assets, self.browser,
                               self.driver_action, self.driver)
        self.wallet.start()

    def get_waller(self):
        """ Get the wallet instance """
        return self.wallet
