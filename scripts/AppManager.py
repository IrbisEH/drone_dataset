import os


class AppManager:
    def __init__(self, app_config):
        self.AppConfig = app_config

    def check_app_structure(self):
        app_config_atr = self.AppConfig.__dict__
        for name, value in app_config_atr.items():
            if 'PATH' in name or 'path' in name:
                if not os.path.isdir(value) and not os.path.isfile(value):
                    print(f'Директории или файла {value} не существует.')
                    exit()

