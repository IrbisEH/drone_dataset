import os
import glob
import shutil
import datetime
import cv2
import re
import tqdm


class CutVideoManager:
    def __init__(self, app_config):
        self.AppConfig = app_config
        self.media_storage_file_paths = {
            'drone_view_img': [],
            'drone_view_video': [],
            'empty_img': [],
            'empty_video': [],
            'turel_view_img': [],
            'turel_view_video': []
        }
        self.unprocessed_file_paths = {
            'drone_view_video': [],
            'empty_video': [],
            'turel_view_video': []
        }
        self.processed_video_names = self.get_processed_video_names()
        self.get_all_media_storage_file_paths()
        self.get_unprocessed_video_file_paths()

    def get_all_media_storage_file_paths(self):
        self.media_storage_file_paths['drone_view_img'] = glob.glob(
            f'{self.AppConfig.drone_view_img_dir_path}/*.jpg'
        )
        self.media_storage_file_paths['empty_img'] = glob.glob(
            f'{self.AppConfig.empty_img_dir_path}/*jpg'
        )
        self.media_storage_file_paths['turel_view_img'] = glob.glob(
            f'{self.AppConfig.turel_view_img_dir_path}/*jpg'
        )
        for file_extension in self.AppConfig.video_file_extensions:
            self.media_storage_file_paths['drone_view_video'] += glob.glob(
                f'{self.AppConfig.drone_view_video_dir_path}/*{file_extension}'
            )
            self.media_storage_file_paths['empty_video'] += glob.glob(
                f'{self.AppConfig.empty_video_dir_path}/*{file_extension}'
            )
            self.media_storage_file_paths['turel_view_video'] += glob.glob(
                f'{self.AppConfig.turel_view_video_dir_path}/*{file_extension}'
            )

    def get_unprocessed_video_file_paths(self):
        processed_video_names = self.get_processed_video_names()
        for view_name, file_paths in self.media_storage_file_paths.items():
            if view_name == 'drone_view_img' or view_name == 'empty_img' or view_name == 'turel_view_img':
                continue
            for file_path in file_paths:
                file_name = file_path.split('/')[-1]
                if file_name not in processed_video_names:
                    self.unprocessed_file_paths[view_name].append(file_path)

    def get_processed_video_names(self):
        processed_video_file = open(self.AppConfig.processed_video_file_path, 'r')
        processed_video_file_names = processed_video_file.read().splitlines()
        processed_video_file.close()
        return processed_video_file_names

    def custom_change_names(self):
        new_file_path = self.AppConfig.MEDIA_STORAGE_DIR_PATH + '/' + 'new_file.txt'
        new_file = open(new_file_path, 'w')
        for view_name, file_paths in self.media_storage_file_paths.items():
            if view_name == 'drone_view_img' or view_name == 'empty_img' or view_name == 'turel_view_img':
                continue
            count = 0
            for file_path in file_paths:
                if file_path not in self.unprocessed_file_paths[view_name]:
                    date = datetime.datetime.now().date()
                    file_path_list = file_path.split('/')
                    file_name = file_path_list.pop()
                    path = '/'.join(file_path_list)
                    new_file_name = f'{view_name}_{date}_{count}{file_name[-4:]}'
                    new_file_path = f'{path}/{new_file_name}'
                    os.rename(file_path, new_file_path)
                    new_file.write(new_file_name + '\n')
                    count += 1
        new_file.close()

    def change_name(self, file_path):

        date = datetime.datetime.today().strftime("%Y-%m-%d")
        count_files = 0
        file_path_list = file_path.split('/')
        file_name = file_path_list.pop()
        view_name = file_path_list[6]
        path = '/'.join(file_path_list)

        processed_file_nums = []
        self.get_all_media_storage_file_paths()
        for exist_file_path in self.media_storage_file_paths[view_name]:
            exist_file_name = exist_file_path.split('/')[-1]
            if view_name in exist_file_name and exist_file_name == file_name:
                return file_path
        for exist_file_path in self.media_storage_file_paths[view_name]:
            exist_file_name = exist_file_path.split('/')[-1]
            if view_name in exist_file_name:
                date_in_file_name = exist_file_name.split('_')[-2]
                if date_in_file_name == date:
                    file_num = int(exist_file_name.split('_')[-1].split('.')[0])
                    processed_file_nums.append(file_num)

        if not len(processed_file_nums) == 0:
            count_files = max(processed_file_nums) + 1

        new_file_name = f'{view_name}_{date}_{count_files}{file_name[-4:]}'
        new_file_path = f'{path}/{new_file_name}'

        os.rename(file_path, new_file_path)

        return new_file_path

    def write_txt(self, file_path, text):
        file = open(file_path, 'a')
        file.write(text)
        file.close()

    def create_frames_dir(self, view_name, dir_num=0):
        date = datetime.datetime.now().date()
        frames_dir_name = f'frames_{view_name}_{date}_{dir_num}'
        frames_dir_path = f'{self.AppConfig.CUT_FRAMES_DIR_NAME}/{frames_dir_name}'
        if not os.path.exists(frames_dir_path):
            os.mkdir(frames_dir_path)
            return frames_dir_path
        dir_num += 1
        self.create_frames_dir(view_name, dir_num)


    def cut_video(self, source_file_path, target_dir_path):

        file_name = source_file_path.split('/')[-1][:-4]

        video_capture = cv2.VideoCapture()
        video_capture.open(source_file_path)
        fps = video_capture.get(cv2.CAP_PROP_FPS)
        frames = video_capture.get(cv2.CAP_PROP_FRAME_COUNT)

        for i in range(int(frames)):
            ret, frame = video_capture.read()
            export_file_path = f'{target_dir_path}/{file_name}_{i}.jpg'
            cv2.imwrite(export_file_path, frame)

    def delete_frames(self, dir_path):
        file_path_list = glob.glob(f'{dir_path}/*.jpg')
        count = 0
        for file_path in file_path_list:
            if not count % self.AppConfig.FRAMES == 0:
                os.remove(file_path)
            count += 1

    def run_cut_video(self):
        for view_name, file_paths in self.unprocessed_file_paths.items():
            print(f'Файлы {view_name} в обработке -->')
            if len(file_paths) == 0:
                continue
            target_dir_path = self.create_frames_dir(view_name)
            count_files = 0
            len_files = len(file_paths)
            for file_path in file_paths:
                print(f'-->({count_files}/{len_files}) {file_path}')
                file_path = self.change_name(file_path)
                try:
                    tmp_dir_path = f'{target_dir_path}/tmp'
                    os.mkdir(tmp_dir_path)
                    self.cut_video(file_path, tmp_dir_path)
                    self.delete_frames(tmp_dir_path)
                    frame_file_paths = glob.glob(f'{tmp_dir_path}/*.jpg')
                    for frame_file_path in frame_file_paths:
                        source_file_path = frame_file_path
                        target_file_path = f'{target_dir_path}/{frame_file_path.split("/")[-1]}'
                        shutil.move(source_file_path, target_file_path)
                    shutil.rmtree(tmp_dir_path)
                    self.write_txt(self.AppConfig.processed_video_file_path, f'{file_path.split("/")[-1]}\n')
                except Exception as err:
                    print(err)
                    shutil.rmtree(tmp_dir_path)
                    self.write_txt(self.AppConfig.error_video_files_path, f'{file_path}\n')
                count_files += 1

