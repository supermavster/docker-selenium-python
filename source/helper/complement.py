class Complement:

    @staticmethod
    def browser_is_chrome(browser):
        return browser == "chrome"

    @staticmethod
    def browser_is_firefox(browser):
        return browser == "firefox"

    @staticmethod
    def check_file_exist(path):
        import os
        return os.path.isfile(path)

    @staticmethod
    def make_folder(path):
        import os
        if not os.path.exists(path):
            os.makedirs(path)

    @staticmethod
    def move_file(src, dest):
        import shutil
        shutil.move(src, dest)

    @staticmethod
    def write_file(path, content):
        with open(path, "w") as f:
            f.write(content)

    @staticmethod
    def read_file(path):
        with open(path, "r") as f:
            return f.read()
