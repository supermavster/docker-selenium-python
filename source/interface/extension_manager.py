from abc import abstractmethod

import requests

import helpers.complement as complement
from interface.interface import Interface


class ExtensionManager(metaclass=Interface):
    path_file = None
    url_extension_firefox = None

    def __init__(self):
        self.driver = None

    @abstractmethod
    def set_driver(self, driver):
        self.driver = driver

    @abstractmethod
    def _get_info(self, url_base_extension):
        data_main = url_base_extension.split("/")
        file_name = data_main[-1]
        return {"file_name": file_name}

    @abstractmethod
    def generate_extension(self, url):
        info_extension = self._get_info(url)
        path_file = self._get_path_extension(url, info_extension)
        self._download_extension(url, path_file)
        return path_file

    @abstractmethod
    def _get_path_extension(self, url_chrome_extension, info_extension=None):
        if info_extension is None:
            info_extension = self._get_info(url_chrome_extension)
        path_file = "{path_file}/{file_name}".format(
            path_file=self.path_file, file_name=info_extension["file_name"]
        )
        return path_file

    @abstractmethod
    def set_extension_path(self, url_base_extension):
        path_file = self._get_path_extension(url_base_extension)
        return path_file

    @abstractmethod
    def exist_extension_by_url(self, url_base_extension):
        path_extension = self.set_extension_path(url_base_extension)
        return {
            "path_file": path_extension,
            "exist": complement.exist_file(path_extension),
        }

    @abstractmethod
    def _download_extension(self, url, path_file):
        print(url)
        request_uri = requests.get(url)
        content = request_uri.content
        complement.write_file(content, path_file, "wb")