# import time
# from selenium.webdriver.chrome.options import Options
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
#
# chrome_options = Options()
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_prefs = {}
# chrome_options.experimental_options["prefs"] = chrome_prefs
# chrome_prefs["profile.default_content_settings"] = {"images": 2}
#
# driver = webdriver.Chrome(options=chrome_options)
# driver.set_window_size(800, 600)
#
#
# url = 'https://www.google.com/'
# driver.get(url)
# title = driver.title
# print(title)

import os

from controller.runner import Runner

if __name__ == "__main__":
    root_path = os.path.dirname(os.path.abspath(__file__))
    Runner(root_path)

# from pyvirtualdisplay import Display
#
# display = Display(visible=0, size=(800, 600))
# display.start()
#
#
# display.stop()
