import os


class ExtensionManager:
    path_asset = None
    browser = None
    wallet = None
    extensions = []

    def __init__(self, path_asset, browser):
        self.path_asset = path_asset
        self.browser = browser
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

        self.wallet = MetaMask(self.path_asset, browser=self.browser)
        self.wallet.start()

    def get_waller(self):
        return self.wallet
