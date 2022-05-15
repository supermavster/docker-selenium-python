from helper.complement import Complement


class UserAgentBrowser:
    path_file = None

    def __init__(self, path_asset):
        self.path_file = f"{path_asset}/user_agent.txt"
        self.driver = None

    def set_driver(self, driver):
        self.driver = driver

    def _get_user_agent(self):
        command = "return navigator.userAgent"
        data_user_agent = self.driver.execute_script(command)
        Complement.write_file(self.path_file, data_user_agent)

    def exist_user_agent(self):
        return Complement.check_file_exist(self.path_file)

    def data_user_agent(self):
        if self.exist_user_agent():
            return Complement.read_file(self.path_file)
        else:
            self._get_user_agent()
            return self.data_user_agent()

# # TEST
# def main(web_driver=None):
#     import os
#     from helper.web_driver import WebDriver
#
#     # Get path asset
#     path_asset = os.path.dirname(os.path.abspath(__file__))
#     path_asset = path_asset.replace("helper", "assets")
#     user_agent_browser = UserAgentBrowser(path_asset)
#     if not user_agent_browser.exist_user_agent():
#         if web_driver is None:
#             chrome_driver = WebDriver(path_asset, "chrome")
#             web_driver = chrome_driver.get_driver()
#         user_agent_browser.set_driver(web_driver)
#     user_agent = user_agent_browser.get_data_user_agent()
#     return user_agent
#
#
# if __name__ == "__main__":
#     main()
