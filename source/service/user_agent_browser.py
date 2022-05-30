"""
User Agent Browser Service
"""
from helper.complement import Complement


class UserAgentBrowser:
    """ UserAgentBrowser class """
    path_file = None

    def __init__(self, path_asset, browser, driver):
        self.path_file = f"{path_asset}/user_agent_{browser}.txt"
        self.driver = driver

    def _get_user_agent(self):
        """ Get the user agent """
        command = "return navigator.userAgent"
        data_user_agent = self.driver.execute_script(command)
        Complement.write_file(self.path_file, data_user_agent)

    def exist_user_agent(self):
        """ Check if the file exist """
        return Complement.check_file_exist(self.path_file)

    def data_user_agent(self):
        """ Return the data of the file """
        if self.exist_user_agent():
            return Complement.read_file(self.path_file)

        self._get_user_agent()
        return self.data_user_agent()
