class AppConfig:
    def __init__(self, main_dir):

        self.APP_DIR = main_dir

        self.MEDIA_STORAGE_DIR_NAME = 'MEDIA_STORAGE'
        self.MEDIA_STORAGE_DIR_PATH = f'{self.APP_DIR}/{self.MEDIA_STORAGE_DIR_NAME}'
        self.drone_view_img_dir_path = f'{self.MEDIA_STORAGE_DIR_PATH}/drone_view_img'
        self.drone_view_video_dir_path = f'{self.MEDIA_STORAGE_DIR_PATH}/drone_view_video'
        self.empty_img_dir_path = f'{self.MEDIA_STORAGE_DIR_PATH}/empty_img'
        self.empty_video_dir_path = f'{self.MEDIA_STORAGE_DIR_PATH}/empty_video'
        self.turel_view_img_dir_path = f'{self.MEDIA_STORAGE_DIR_PATH}/turel_view_img'
        self.turel_view_video_dir_path = f'{self.MEDIA_STORAGE_DIR_PATH}/turel_view_video'
        self.processed_video_file_path = f'{self.MEDIA_STORAGE_DIR_PATH}/processed_video_names.txt'
        self.error_video_files_path = f'{self.MEDIA_STORAGE_DIR_PATH}/error_video_files.txt'

        self.video_file_extensions = ['.mp4', '.MP4', 'mov', 'MOV', 'm4v', 'M4V']

        self.CUT_FRAMES_DIR_NAME = 'CUT_FRAMES'
        self.CUT_FRAMES_DIR_PATH = f'{self.APP_DIR}/{self.CUT_FRAMES_DIR_NAME}'

        self.FRAMES = 20

        self.CLASSES_NAMES = {
            '0': 'drone_view_BMP',
            '1': 'drone_view_tank',
            '2': 'drone_view_military_truck',
            '3': 'drone_view_armored_car',
            '4': 'drone_view_artillery',
            '5': 'drone_view_ZRK',
            '6': 'drone_view_SAU',
            '7': 'drone_view_RSZO',
            '8': 'drone_view_TRK',
            '9': 'drone_view_maybe_tank',
            '10': 'drone_view_medical_military',
            '11': 'drone_view_medical_civil',
            '12': 'drone_view_police_car',
            '13': 'drone_view_police_truck',
            '14': 'drone_view_fire_engine',
            '15': 'drone_view_car',
            '16': 'drone_view_civil_truck',
            '17': 'drone_view_bus',
            '18': 'drone_view_minibus',
            '19': 'drone_view_vnedorozhnik',
            '20': 'drone_view_airplane',
            '21': 'drone_view_helicopter',
            '22': 'drone_view_train',
            '23': 'drone_view_wagon',
            '24': 'drone_view_tractor',
            '25': 'drone_view_unrecognized_human',
            '26': 'drone_view_military_human',
            '27': 'drone_view_civil_human',
            '28': 'turel_view_BMP',
            '29': 'turel_view_tank',
            '30': 'turel_view_military_truck',
            '31': 'turel_view_armored_car',
            '32': 'turel_view_artillery',
            '33': 'turel_view_ZRK',
            '34': 'turel_view_SAU',
            '35': 'turel_view_RSZO',
            '36': 'turel_view_TRK',
            '37': 'turel_view_maybe_tank',
            '38': 'turel_view_medical_military',
            '39': 'turel_view_medical_civil',
            '40': 'turel_view_police_car',
            '41': 'turel_view_police_truck',
            '42': 'turel_view_fire_engine',
            '43': 'turel_view_car',
            '44': 'turel_view_civil_truck',
            '45': 'turel_view_bus',
            '46': 'turel_view_minibus',
            '47': 'turel_view_vnedorozhnik',
            '48': 'turel_view_airplane',
            '49': 'turel_view_helicopter',
            '50': 'turel_view_train',
            '51': 'turel_view_wagon',
            '52': 'turel_view_tractor',
            '53': 'turel_view_unrecognized_human',
            '54': 'turel_view_military_human',
            '55': 'turel_view_civil_human',
}



