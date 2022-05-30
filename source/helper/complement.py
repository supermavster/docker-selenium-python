"""
Helper module - Complement.
"""
import os
import shutil


class Complement:
    """ Complement class. """

    @staticmethod
    def browser_is_chrome(browser):
        """ Check if browser is chrome. """
        return browser == "chrome"

    @staticmethod
    def browser_is_firefox(browser):
        """ Check if browser is firefox. """
        return browser == "firefox"

    @staticmethod
    def check_file_exist(path):
        """ Check if file exist. """
        return os.path.isfile(path)

    @staticmethod
    def make_folder(path):
        """ Create folder. """
        if not os.path.exists(path):
            os.makedirs(path)

    @staticmethod
    def move_file(src, dest):
        """ Move file. """
        shutil.move(src, dest)

    @staticmethod
    def write_file(path, content, mode="w", encoding="utf8"):
        """ Write file. """
        if mode == 'wb':
            # pylint: skip-file
            with open(path, mode) as file:
                file.write(content)
        else:
            with open(path, mode, encoding=encoding) as file:
                file.write(content)

    @staticmethod
    def read_file(path, encoding="utf8"):
        """ Read file. """
        with open(path, 'r', encoding=encoding) as file:
            return file.read()

    @staticmethod
    def convertENVArray(env_array):
        """ Convert ENV[] to Array """
        return env_array.replace('[', '').replace(']', '') \
            .replace('"', '') \
            .replace(', ', ',').replace(' ,', ',') \
            .split(',')
