import os


class ExtensionManager:
    path_asset = None
    browser = None
    driver_manager = None
    driver = None
    wallet = None
    extensions = []

    def __init__(self, driver_manager, driver, path_asset, browser):
        self.path_asset = path_asset
        self.browser = browser
        self.driver_manager = driver_manager
        self.driver = driver
        self.set_extensions()

    def get_extensions(self):
        return self.extensions

    def set_extensions(self):
        self.extensions = []

        extensions = os.getenv('EXTENSIONS_CHROME') or []

        if 'metamask' in extensions:
            self.set_wallet()
            if self.wallet is not None:
                self.extensions.append(self.wallet.get_path_extension())

    def set_wallet(self):
        from controller.extension.metamask import MetaMask

        self.wallet = MetaMask(self.path_asset, self.driver_manager, self.driver, self.browser)
        self.wallet.start()

    def get_waller(self):
        return self.wallet
