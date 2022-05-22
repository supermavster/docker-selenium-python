# # import os
# # import time
# # import json
# # import sys
# #
# # from selenium import webdriver
# # from selenium.webdriver.firefox.options import Options
# # from selenium.webdriver.firefox.options import Options
# # from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# #
# #
# # try:
# #     root_path = os.path.dirname(os.path.abspath(__file__))
# #     path_asset = root_path + '/assets/'
# #     path_extension = path_asset + 'extensions/firefox/ether_metamask-10.12.4.xpi'
# #
# #     # Create profile with all extensions
# #     profile = webdriver.FirefoxProfile()
# #     profile.set_preference('xpinstall.signatures.required', False)
# #     # Enable extensions
# #     profile.add_extension(path_extension)
# #     # Add custom extensions
# #     profile.set_preference('extensions.metamask.enabled', True)
# #
# #     profile.set_preference("plugin.state.flash", 2)
# #     profile.add_extension(path_extension)
# #     profile.accept_untrusted_certs = True
# #     profile.assume_untrusted_cert_issuer = True
# #     policy = "security.fileuri.strict_origin_policy"
# #     profile.set_preference(policy, False)
# #     profile.update_preferences()
# #
# #     # Create options
# #     options = Options()
# #     options.add_argument("-profile")
# #     options.add_argument(profile.path)
# #     firefox_capabilities = DesiredCapabilities.FIREFOX
# #     firefox_capabilities['marionette'] = True
# #
# #     # set_preference and install_addons
# #     options.add_argument("--disable-infobars")
# #     options.add_argument("--disable-web-security")
# #     options.add_argument("--allow-running-insecure-content")
# #     options.add_argument("--ignore-certificate-errors")
# #     # install_addons options
# #     options.add_argument("--install-extension=" + path_extension)
# #     # options.add_argument('-headless')
# #     # options.add_argument('-no-sandbox')
# #     options.add_argument('-disable-dev-shm-usage')
# #     options.add_argument('-disable-setuid-sandbox')
# #     # options.add_argument('-disable-infobars')
# #     options.add_argument('-disable-web-security')
# #     options.add_argument('-allow-running-insecure-content')
# #     options.add_argument('-allow-insecure-localhost')
# #     # options.add_argument('-disable-gpu')
# #     # options.add_argument('--disable-extensions-except=' + path_extension)
# #     import uuid
# #     import json
# #
# #     options.accept_insecure_certs = True
# #     addon_id = "webextension@metamask.io"
# #     addon_dyn_id = str(uuid.uuid4())
# #     json_info = json.dumps({addon_id: addon_dyn_id})
# #     preference = "extensions.webextensions.uuids"
# #     options.set_preference(preference, json_info)
# #     options.add_argument('--disable-popup-blocking')
# #     options.add_argument('--load-extension=' + path_extension)
# #
# #     # Create driver
# #
# #     driver = webdriver.Remote(
# #         command_executor="http://selenium-hub:4444/wd/hub",
# #         options=options,
# #         desired_capabilities=firefox_capabilities
# #     )
# #
# #     driver.get("about:addons")
# #     time.sleep(20)
# #     driver.get("about:addons")
# #     time.sleep(100)
# #     driver.quit()
# # except Exception as e:
# #     print(e)
# #     try:
# #         driver.quit()
# #     except:
# #         pass
# import time
#
# from selenium import webdriver
# from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
#
# try:
#     import os
#
#     # Env
#     from dotenv import load_dotenv
#
#     load_dotenv()
#
#     root_path = os.path.dirname(os.path.abspath(__file__))
#     path_asset = root_path + '/assets/'
#     path_extension = path_asset + 'extensions/firefox/ether_metamask-10.12.4.xpi'
#
#     options = Options()
#     options.add_argument("--disable-web-security")
#     options.add_argument("--ignore-certificate-errors")
#     options.add_argument('--disable-web-security')
#     options.add_argument('--allow-insecure-localhost')
#     options.add_argument('--disable-popup-blocking')
#     options.add_argument('--disable-infobars')
#     options.add_argument('--disable-gpu')
#     options.add_argument('--disable-setuid-sandbox')
#     options.add_argument('--disable-dev-shm-usage')
#
#     options.set_preference('xpinstall.signatures.required', False)
#     options.set_preference('security.fileuri.strict_origin_policy', False)
#     options.set_preference("plugin.state.flash", 2)
#     options.accept_insecure_certs = True
#     options.assume_untrusted_cert_issuer = True
#     options.set_preference("security.cert_pinning.enforcement_level", 0)
#
#     import uuid
#     import json
#
#     addon_id = "webextension@metamask.io"
#     addon_dyn_id = str(uuid.uuid4())
#     json_info = json.dumps({addon_id: addon_dyn_id})
#     preference = "extensions.webextensions.uuids"
#     options.set_preference(preference, json_info)
#
#     # options.add_argument('--load-extension=' + path_extension)
#     # options.add_extension(path_extension)
#     options.profile = webdriver.FirefoxProfile()
#     options.profile.set_preference("webdriver_assume_untrusted_issuer", False)
#     options.profile.set_preference("webdriver_accept_untrusted_certs", True)
#     options.profile.set_preference("webdriver_unexpected_alert_behaviour", "accept")
#     # options.profile.add_extension(path_extension)
#
#
#     from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
#
#     from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
#
#     fp = FirefoxProfile()
#     fp.add_extension(path_extension)
#     fp.set_preference("webdriver_assume_untrusted_issuer", False)
#     fp.set_preference("webdriver_accept_untrusted_certs", True)
#     fp.set_preference("webdriver_unexpected_alert_behaviour", "accept")
#
#
#     driver = webdriver.Remote(
#         command_executor="http://selenium-hub:4444/wd/hub",
#         options=options
#     )
#
#     driver.get("about:addons")
#     # Download profile from firefox
#     time.sleep(50)
#     driver.quit()
# except Exception as e:
#     print(e)
#     try:
#         driver.quit()
#     except:
#         pass


# Copy file local to docker
# docker cp /home/selenium/profile.zip selenium-hub:/tmp/
import time

try:
    import os
    from dotenv import load_dotenv
    from selenium import webdriver
    # Firefox
    from selenium.webdriver.firefox.options import Options


    load_dotenv()

    root_path = os.path.dirname(os.path.abspath(__file__))
    path_asset = root_path + '/assets/'
    path_extension = path_asset + 'extensions/firefox/ether_metamask-10.12.4.xpi'

    # copy file to docker in python


    firefox_options = webdriver.FirefoxOptions()
    # firefox_options.add_argument("--disable-web-security")
    # firefox_options.add_argument("--ignore-certificate-errors")
    # firefox_options.accept_insecure_certs = True
    # firefox_options.assume_untrusted_cert_issuer = True
    # firefox_options.set_preference("security.cert_pinning.enforcement_level", 0)
    # firefox_options.set_preference("security.insecure_password.ui.enabled", False)
    # firefox_options.set_preference("security.insecure_field_warning.contextual.enabled", False)
    # firefox_options.set_preference("security.insecure_field_warning.filter.enabled", False)
    # firefox_options.set_preference("security.insecure_password.ui.enabled", False)



    driver = webdriver.Remote(
        command_executor="http://selenium-hub:4444/wd/hub",
        options=firefox_options
    )

    payload = {"path": path_extension}
    payload["temporary"] = True
    # The function returns an identifier of the installed addon.
    # This identifier can later be used to uninstall installed addon.
    var = driver.execute("INSTALL_ADDON", payload)["value"]
    print(var)

    driver.get("about:addons")
    # Download profile from firefox
    time.sleep(20)
    driver.quit()
except Exception as e:
    print(e)
    try:
        driver.quit()
    except:
        pass
