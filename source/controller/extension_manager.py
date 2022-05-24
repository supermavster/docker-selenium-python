import os


class ExtensionManager:
    path_assets = None
    browser = None
    driver_manager = None
    driver_action = None
    driver = None
    wallet = None
    captcha = None
    extensions = []

    def __init__(self, path_assets, browser, driver_manager=None, driver_action=None, driver=None):
        self.path_assets = path_assets
        self.browser = browser
        self.driver_manager = driver_manager
        self.driver_action = driver_action
        self.driver = driver
        self.set_extensions()

    def get_extensions(self):
        return self.extensions

    def set_extensions(self):
        self.extensions = []

        extensions = os.getenv('EXTENSIONS_' + self.browser.upper())
        if extensions is not None:
            extensions = extensions.replace('[', '').replace(']', '').replace('"', '') \
                .replace(', ', ',').replace(' ,', ',').split(',')

            for extension in extensions:
                match extension:
                    case 'metamask':
                        self.start_wallet()
                    case 'captcha':
                        self.start_captcha()

    def start_captcha(self):
        self.set_captcha()
        if self.captcha is not None:
            self.extensions.append(self.captcha.get_path_extension())

    def set_captcha(self):
        from controller.extension.captchasolver import CaptchaSolver

        self.captcha = CaptchaSolver(self.path_assets, self.browser, self.driver_manager, self.driver_action,
                                     self.driver)
        self.captcha.start()

    def get_captcha(self):
        return self.captcha

    def start_wallet(self):
        self.set_wallet()
        if self.wallet is not None:
            self.extensions.append(self.wallet.get_path_extension())

    def set_wallet(self):
        from controller.extension.metamask import MetaMask

        self.wallet = MetaMask(self.path_assets, self.browser, self.driver_manager, self.driver_action, self.driver)
        self.wallet.start()

    def get_waller(self):
        return self.wallet
