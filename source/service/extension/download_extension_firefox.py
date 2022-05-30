"""
Download Extension - Firefox
"""
import requests

from interface.extension.extension_manager import ExtensionManager


def get_main_url(url_extension, name_extension):
    """ Get Main Url """
    response = requests.get(url_extension)
    response_json = response.json()
    url_extension = ""
    for item in response_json["results"]:
        if item["slug"] == name_extension:
            url_extension = item["current_version"]["file"]["url"]
            break
    return url_extension


class DownloadExtensionFirefox(ExtensionManager):
    """ Download Extensions Firefox  """

    path_file = "extensions/firefox"
    # Firefox
    url_extension_firefox = (
        "https://addons.mozilla.org/api/v5/addons/search/"
        "?app=firefox&author={user_ids}"
        "&exclude_addons={name_extension}"
        "&page=1&page_size=10&sort=hotness"
        "&type=extension&lang=en-US"
    )

    def __init__(self, path_assets):
        super().__init__()
        self.path_file = f"{path_assets}/{self.path_file}"

    def get_base_url(self, object_url):
        """ Get Base Url """
        name_extension = object_url["collection_url"].split("/")[-1]
        user_ids = "%2C".join(str(x) for x in object_url["user_id"])
        url_extension = self.url_extension_firefox.format(
            user_ids=user_ids, name_extension=name_extension
        )
        return url_extension

    def get_url_extension(self, object_url):
        """ Get Url Extensions"""
        url_extension = self.get_base_url(object_url)
        name_real_extension = object_url["url"].split("/")[-1]
        main_url = get_main_url(url_extension, name_real_extension)
        return main_url

    # Override
    def _get_info(self, url_base_extension):
        """ Get Info """
        data_main = url_base_extension.split("/")
        file_name = data_main[-1]
        return {"file_name": file_name}

    def generate_extension(self, url):
        """ Generate extension """
        info_extension = self._get_info(url)
        path_file = self._get_path_extension(url, info_extension)
        self._download_extension(url, path_file)
        return path_file
