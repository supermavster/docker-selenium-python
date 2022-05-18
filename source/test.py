import os
import time
import json
import sys

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

try:
    root_path = os.path.dirname(os.path.abspath(__file__))
    path_asset = root_path + '/assets/'
    path_extension = path_asset + 'extensions/firefox/metamask-10.12.4-an+fx.xpi'

    desired_cap = DesiredCapabilities.FIREFOX

    options = webdriver.FirefoxOptions()

    driver = webdriver.Remote(
        command_executor="http://selenium-hub:4444/wd/hub",
        desired_capabilities=desired_cap,
        options=options,
    )

    driver.install_addon(path_extension, temporary=True)

    driver.get("about:addons")
    time.sleep(20)
    driver.quit()
except Exception as e:
    print(e)
    try:
        driver.quit()
    except:
        pass