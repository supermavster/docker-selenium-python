import os


class ExtensionManager:
    path_assets = None
    browser = None
    driver_manager = None
    driver = None
    wallet = None
    extensions = []

    def __init__(self, path_assets, browser, driver_manager=None, driver=None):
        self.path_assets = path_assets
        self.browser = browser
        self.driver_manager = driver_manager
        self.driver = driver
        self.set_extensions()

    def get_extensions(self):
        return self.extensions

    def set_extensions(self):
        self.extensions = []

        extensions = os.getenv('EXTENSIONS_' + self.browser.upper())
        extensions = extensions.replace('[', '').replace(']', '').replace('"', '') \
            .replace(', ', ',').replace(' ,', ',').split(',')

        if 'metamask' in extensions:
            self.set_wallet()
            if self.wallet is not None:
                self.extensions.append(self.wallet.get_path_extension())

    def set_wallet(self):
        from controller.extension.metamask import MetaMask

        self.wallet = MetaMask(self.path_assets, self.browser, self.driver_manager, self.driver)
        self.wallet.start()

    def get_waller(self):
        return self.wallet
