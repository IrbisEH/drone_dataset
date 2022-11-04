import os
from scripts.AppManager import AppManager
from scripts.ConfigManager import AppConfig
from scripts.CutVideoManger import CutVideoManager

DIR = os.path.dirname(__file__)


class App:
    def __init__(self, main_dir):
        self.dir = main_dir
        self.AppConfig = AppConfig(self.dir)
        self.AppManager = AppManager(self.AppConfig)
        self.CutVideoManager = CutVideoManager(self.AppConfig)


if __name__ == '__main__':
    App = App(DIR)
    App.AppManager.check_app_structure()

    App.CutVideoManager.run_cut_video()
