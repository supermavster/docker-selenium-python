import os

from selenium import webdriver


class ConfigurationChrome:
    driver = None
    path_driver = None
    environment = 'local'

    def __init__(self, path_driver, environment):
        self.path_driver = path_driver
        self.environment = environment

    def set_driver(self):
        options_browser = self._get_options()
        self.driver = self._get_manager_driver(options_browser)

    def get_driver(self):
        return self.driver

    def _get_manager_driver(self, options_browser):
        match self.environment:
            case 'local':
                return self._get_driver_local(options_browser)
            case 'docker':
                return self._get_driver_docker(options_browser)
            case 'remote':
                return self._get_driver_remote(options_browser)
            case default:
                return None

    def _get_driver_local(self, options_browser):
        service = self._get_service()
        return webdriver.Chrome(service=service, options=options_browser)

    def _get_driver_docker(self, options_browser):
        return webdriver.Chrome(options=options_browser)

    def _get_driver_remote(self, options_browser):
        remote_url = os.getenv("REMOTE_URL") or "http://selenium-hub:4444/wd/hub"
        return webdriver.Remote(
            command_executor=remote_url,
            options=options_browser
        )

    def _get_service(self):
        from selenium.webdriver.chrome.service import Service as ServiceChrome
        service_browser = ServiceChrome(self.path_driver)
        return service_browser

    def _get_options(self):
        options_browser = self._set_service_option()
        options_browser = self._get_options_general(options_browser)
        options_browser = self._get_manager_options(options_browser)
        return options_browser

    def _set_service_option(self):
        return webdriver.ChromeOptions()

    def _get_manager_options(self, options_browser):
        match self.environment:
            case 'local':
                return self._get_options_local(options_browser)
            case 'docker':
                return self._get_options_docker(options_browser)
            case 'remote':
                return self._get_options_remote(options_browser)
            case default:
                return options_browser

    def _get_options_general(self, options_browser):
        options_browser.add_argument("--lang=en-US")
        options_browser.add_argument("--disable-infobars")
        options_browser.add_experimental_option(
            "prefs",
            {
                "intl.accept_languages": "en,en_US",
                "download.default_directory": os.getcwd(),
                "download.prompt_for_download": False,
            },
        )
        options_browser.add_experimental_option("excludeSwitches", ["enable-logging"])
        options_browser.add_experimental_option("excludeSwitches", ["enable-automation"])
        options_browser.add_experimental_option("useAutomationExtension", False)
        return options_browser

    def _get_options_local(self, options_browser):
        # options_browser.add_argument("--no-sandbox")
        options_browser.add_argument("--log-level=3")
        options_browser.add_argument("--disable-gpu")
        options_browser.add_argument("--no-first-run")
        options_browser.add_argument("--start-maximized")
        options_browser.add_argument("--disk-cache-size=1")
        options_browser.add_argument("--media-cache-size=1")
        options_browser.add_argument("--no-service-autorun")
        options_browser.add_argument("--password-store=basic")
        # options_browser.add_argument("--disable-dev-shm-usage")
        options_browser.add_argument("--disable-application-cache")
        options_browser.add_argument("--disable-blink-features=AutomationControlled")
        return options_browser

    def _get_options_docker(self, options_browser):
        options_browser.add_argument("--headless")
        return options_browser

    def _get_options_remote(self, options_browser):
        return options_browser

    def get_single_drive(self):
        return None
