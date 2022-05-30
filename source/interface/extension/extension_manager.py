"""
Extension Manager
"""
from abc import abstractmethod

import requests

from helper.complement import Complement
from interface.interface import Interface


class ExtensionManager(metaclass=Interface):
    """ Extension Manager Interface """
    path_file = None
    url_extension_firefox = None

    def __init__(self):
        self.driver = None

    # @abstractmethod
    def set_driver(self, driver):
        """ Set driver """
        self.driver = driver

    @abstractmethod
    def _get_info(self, url_base_extension):
        """ Get info extension """
        data_main = url_base_extension.split("/")
        file_name = data_main[-1]
        return {"file_name": file_name}

    @abstractmethod
    def generate_extension(self, url):
        """ Generate extension """
        # info_extension = self._get_info(url)
        # path_file = self._get_path_extension(url, info_extension)
        # self._download_extension(url, path_file)
        # return path_file

    # @abstractmethod
    def _get_path_extension(self, url_chrome_extension, info_extension=None):
        """ Get path extension """
        if info_extension is None:
            info_extension = self._get_info(url_chrome_extension)
        Complement.make_folder(self.path_file)
        path_file = f"{self.path_file}/{info_extension['file_name']}"
        return path_file

    # @abstractmethod
    def set_extension_path(self, url_base_extension):
        """ Set extension path """
        path_file = self._get_path_extension(url_base_extension)
        return path_file

    # @abstractmethod
    def exist_extension_by_url(self, url_base_extension):
        """ Exist extension by url """
        path_extension = self.set_extension_path(url_base_extension)
        return {
            "path_file": path_extension,
            "exist": Complement.check_file_exist(path_extension),
        }

    # @abstractmethod
    @staticmethod
    def _download_extension(url, path_file):
        """ Download extension """
        request_uri = requests.get(url)
        content = request_uri.content
        Complement.write_file(path_file, content, 'wb')
