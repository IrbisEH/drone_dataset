import os
import shutil
import random
from datetime import datetime
from glob import glob

from .ConfigMainData import (
    IMAGE_DIR_NAME, LABELS_DIR_NAME, YAML_FILE_NAME, MAIN_DATA_NAME, EMPTY_DIR_NAME,
    CLASSES_NAMES, TRAIN_DIR_NAME, VALID_DIR_NAME, TEST_DIR_NAME
)


class DroneDataJobs:

    def test(self):
        print('test')

    def get_example_img_by_num_class(self, source, num_class):

        target_dir_path = DIR_PATH + '/' + EXPORT_DIR_NAME + '/' + EXAMPLE_DIR_NAME

        if not os.path.exists(target_dir_path):
            os.makedirs(target_dir_path)

        source_img_path = source + '/' + IMAGE_DIR_NAME
        source_label_path = source + '/' + LABELS_DIR_NAME

        source_label_file_names = os.listdir(source_label_path)
        for label_file_name in source_label_file_names:
            img_file_name = label_file_name[:-4] + '.jpg'

            source_label_file_path = source_label_path + '/' + label_file_name
            source_img_file_path = source_img_path + '/' + img_file_name

            label_file = open(source_label_file_path, 'r')
            lines = label_file.read().splitlines()

            for line in lines:
                line_list = line.split(' ')
                cur_num_class = int(line_list[0])
                if cur_num_class == num_class:
                    print('OK')

    def check_source_dir(self, import_path):
        """Проверяет директорию импорта на наличие всех необходимых файлов/директорий"""

        import_dir_names = os.listdir(import_path)

        if IMAGE_DIR_NAME not in import_dir_names:
            print('В IMPORT нет директории images')
            exit()
        if LABELS_DIR_NAME not in import_dir_names:
            print('В IMPORT нет директории labels')
            exit()
        if YAML_FILE_NAME not in import_dir_names:
            print('В IMPORT нет файла yaml')
            exit()

    def get_classes_from_yaml(self, yaml_file_path):
        """Читает файл yaml и возращает словарь с номерами и именами классов"""

        yaml_file = open(yaml_file_path, 'r')
        lines = yaml_file.read().splitlines()
        yaml_file.close()

        names_line = ''
        for line in lines:
            if 'names:' in line:
                names_line = line
        if names_line == '':
            print('некорректный файл yaml')
            exit()
        names_line = names_line[7:]
        names_line = names_line.strip("[']")
        cur_classes_names = names_line.split("', '")
        cur_classes = {}
        for idx, name in enumerate(cur_classes_names):
            cur_classes[str(idx)] = name

        return cur_classes

    def change_classes_nums(self, changes_dic, label_dir_path):

        label_file_names = os.listdir(label_dir_path)

        for label_file_name in label_file_names:
            label_file_path = label_dir_path + '/' + label_file_name
            label_file = open(label_file_path, 'r')
            lines = label_file.read().splitlines()
            label_file.close()

            changes = False
            label_file_data = []
            for line in lines:
                line = line.split(' ')
                cur_num_class = line[0]
                for key, value in changes_dic.items():
                    for item in value:
                        if cur_num_class == item:
                            line[0] = str(key)
                            changes = True
                line = ' '.join(line)
                label_file_data.append(line)

            if changes:
                label_file = open(label_file_path, 'w')
                for item in label_file_data:
                    label_file.write(item + '\n')
                label_file.close()

    def get_roboflow_yaml_file(self, yaml_dir, classes_names):
        yaml_file_path = yaml_dir + '/' + YAML_FILE_NAME

        cur_classes_names = []
        count = 0
        while str(count) in classes_names.keys():
            cur_classes_names.append(classes_names[str(count)])
            count += 1
        cur_classes_names_str = "', '".join(cur_classes_names)
        yaml_file = open(yaml_file_path, 'w')
        yaml_file.write(f'nc: {len(cur_classes_names)}\nnames: [\'{cur_classes_names_str}\']')
        yaml_file.close()

    def get_yaml_file(self, classes_data, target_dir_path, valid_data, test_data):

        yaml_file_name = 'data.yaml'
        yaml_file_path = target_dir_path + '/' + yaml_file_name

        new_folder_name = target_dir_path.split('/')[-1]

        yaml_file = open(yaml_file_path, 'w')
        yaml_file.write(f'train: ../{new_folder_name}/images/train/\n')
        if valid_data:
            yaml_file.write(f'val: ../{new_folder_name}/images/valid/\n')
        if test_data:
            yaml_file.write(f'test: ../{new_folder_name}/images/test/\n')
        yaml_file.write(f'\nnc: {len(classes_data.keys()) - 1}\n\nnames: [')

        count = 0
        for key, value in classes_data.items():
            if count == (len(classes_data.keys()) - 1):
                yaml_file.write(f"'{value}']")
            else:
                yaml_file.write(f"'{value}', ")
            count += 1

        yaml_file.close()

    def change_file_names(self, dir_path):
        """
        Меняет названия label и img файлов.
        Нужно для экспорта в базу и индентификации группы импорта.
        """
        cur_date = str(datetime.now().date())

        img_dir_path = dir_path + '/' + IMAGE_DIR_NAME
        label_dir_path = dir_path + '/' + LABELS_DIR_NAME

        img_file_names = os.listdir(img_dir_path)

        count = 1
        for file_name in img_file_names:

            check_name = file_name.split('.')
            if check_name[-1] != 'jpg':
                continue

            name = file_name[:-4]
            img_file_path = img_dir_path + '/' + name + '.jpg'
            label_file_path = label_dir_path + '/' + name + '.txt'

            new_name_img_file_path = img_dir_path + '/' + f'{cur_date}-{count}' + '.jpg'
            new_name_label_file_path = label_dir_path + '/' + f'{cur_date}-{count}' + '.txt'

            os.rename(img_file_path, new_name_img_file_path)
            os.rename(label_file_path, new_name_label_file_path)

            count += 1

    def input_new_in_main_data(self, source_path, target_path, classes_names, changes_dic):
        """

        :param source_path: директория которую экспортируем
        :param target_path: директория куда импортируем
        :param classes_names: словарь номер кдасса - имя класса
        :param changes_dic:  изменения номеров классов в экспортируемых данных
        :return:
        """

        self.check_source_dir(source_path)

        source_yaml_path = source_path + '/' + YAML_FILE_NAME
        source_label_dir_path = source_path + '/' + LABELS_DIR_NAME
        source_img_dir_path = source_path + '/' + IMAGE_DIR_NAME

        target_label_dir_path = target_path + '/' + LABELS_DIR_NAME
        target_img_dir_path = target_path + '/' + IMAGE_DIR_NAME

        source_classes = self.get_classes_from_yaml(source_yaml_path)

        if changes_dic:
            self.change_classes_nums(changes_dic, source_label_dir_path)

        self.change_file_names(source_path)

        source_label_file_names = os.listdir(source_label_dir_path)

        for source_label_file_name in source_label_file_names:

            source_label_file_path = source_label_dir_path + '/' + source_label_file_name
            target_label_file_path = target_label_dir_path + '/' + source_label_file_name

            source_label_file = open(source_label_file_path, 'r')
            lines = source_label_file.read().splitlines()
            source_label_file.close()
            file_data = []
            for line in lines:
                line = line.split(' ')
                cur_class_num = line[0]
                cur_class_name = source_classes[cur_class_num]
                for key, value in classes_names.items():
                    if cur_class_name == value:
                        line[0] = key
                line = ' '.join(line)
                file_data.append(line)

            source_label_file = open(source_label_file_path, 'w')
            for item in file_data:
                source_label_file.write(item + '\n')
            source_label_file.close()

            shutil.move(source_label_file_path, target_label_file_path)

        source_img_file_names = os.listdir(source_img_dir_path)
        for source_img_file_name in source_img_file_names:
            source_img_file_path = source_img_dir_path + '/' + source_img_file_name
            target_img_file_path = target_img_dir_path + '/' + source_img_file_name

            shutil.move(source_img_file_path, target_img_file_path)

    def get_count_classes(self, dir_path, write_txt_file_name='count_classes.txt'):
        """
        Принимает путь и название txt файла.
        По указанному пути находит директорию labels и yaml файл.
        Функция считает кол-во аннотаций в указанной директории, записывает результаты в
        txt файл в соответствии с именами классов из yaml файла, если файла yaml нет, то записывает из кофига.
        """

        dir_path_file_names = os.listdir(dir_path)

        if LABELS_DIR_NAME not in dir_path_file_names:
            print('Нет директории labels')
            exit()

        source_labels_dir = dir_path + '/' + LABELS_DIR_NAME

        if YAML_FILE_NAME not in dir_path_file_names:
            classes_names_dic = CLASSES_NAMES
        else:
            yaml_file_path = dir_path + '/' + YAML_FILE_NAME
            classes_names_dic = self.get_classes_from_yaml(yaml_file_path)

        label_file_names = os.listdir(source_labels_dir)

        count_classes_dic = {}
        for label_file_name in label_file_names:
            check_name = label_file_name.split('.')
            if check_name[-1] != 'txt':
                continue
            label_file_path = source_labels_dir + '/' + label_file_name
            label_file = open(label_file_path, 'r', encoding='utf-8')
            lines = label_file.read().splitlines()
            label_file.close()
            for line in lines:
                line = line.split(' ')
                class_num = line[0]
                class_name = classes_names_dic[class_num]
                if class_name not in count_classes_dic.keys():
                    count_classes_dic[class_name] = 1
                else:
                    count_classes_dic[class_name] += 1

        write_txt_file_path = dir_path + '/' + write_txt_file_name
        txt_file = open(write_txt_file_path, 'w', encoding='utf-8')
        for key, value in count_classes_dic.items():
            txt_file.write(f'{key} - {value}\n')
        txt_file.close()

        for key, value in count_classes_dic.items():
            print(f'{key} - {value}')

    def get_new_data(
            self, source_path, new_data_path, export_yaml_classes, export_classes_names,
            empty_train_percent=0, empty_valid_percent=0, valid_percent=0, test_percent=0
    ):

        source_label_dir_path = source_path + '/' + LABELS_DIR_NAME
        source_img_dir_path = source_path + '/' + IMAGE_DIR_NAME

        target_img_folder = new_data_path + '/' + IMAGE_DIR_NAME
        target_label_folder = new_data_path + '/' + LABELS_DIR_NAME

        train_img_dir_path = target_img_folder + '/' + TRAIN_DIR_NAME
        valid_img_dir_path = target_img_folder + '/' + VALID_DIR_NAME
        test_img_dir_path = target_img_folder + '/' + TEST_DIR_NAME

        train_label_dir_path = target_label_folder + '/' + TRAIN_DIR_NAME
        valid_label_dir_path = target_label_folder + '/' + VALID_DIR_NAME
        test_label_dir_path = target_label_folder + '/' + TEST_DIR_NAME

        # проверяем данные для yaml файла
        if len(export_yaml_classes) == 0:
            print('Не переданы данные для yaml файла')

        # проверяем наличие имен классов
        if len(export_classes_names) == 0:
            print('Не переданны данные экспортируемыз класслв')
            exit()

        # список стандартных значений имен
        default_class_names = []
        for value in CLASSES_NAMES.values():
            default_class_names.append(value)

        # проверяем папку Export
        if os.path.exists(new_data_path):
            print('Папка EXPORT уже содержит такой запрос')
            exit()
        else:
            os.makedirs(train_label_dir_path)
            os.makedirs(train_img_dir_path)



        source_label_file_names = os.listdir(source_label_dir_path)

        for source_label_file_name in source_label_file_names:

            check_name = source_label_file_name.split('.')
            if check_name[-1] != 'txt':
                continue

            file_name = source_label_file_name[:-4]
            source_img_file_path = source_img_dir_path + '/' + file_name + '.jpg'
            source_label_file_path = source_label_dir_path + '/' + source_label_file_name

            target_img_file_path = train_img_dir_path + '/' + file_name + '.jpg'
            target_label_file_path = train_label_dir_path + '/' + source_label_file_name

            source_label_file = open(source_label_file_path, 'r')
            lines = source_label_file.read().splitlines()
            source_label_file.close()

            file_data = []
            for line in lines:
                line = line.split(' ')
                cur_class_num = line[0]
                for key, value in export_classes_names.items():
                    for item in value:
                        if cur_class_num == item:
                            line[0] = key
                            line = ' '.join(line)
                            file_data.append(line)

            if file_data:
                target_label_file = open(target_label_file_path, 'w')
                for item in file_data:
                    target_label_file.write(item + '\n')
                target_label_file.close()

                shutil.copyfile(source_img_file_path, target_img_file_path)


        #формируем valid dataset и test_dataset
        source_img_dir_path = train_img_dir_path
        source_label_dir_path = train_label_dir_path

        source_file_names = os.listdir(train_label_dir_path)
        amount_source_files = len(source_file_names)

        amount_empty_train_files = int((amount_source_files / 100) * empty_train_percent)
        amount_empty_valid_files = int((amount_source_files / 100) * empty_valid_percent)
        amount_valid_files = int((amount_source_files / 100) * valid_percent)
        amount_test_files = int((amount_source_files / 100) * test_percent)

        while amount_valid_files != 0:
            if not os.path.exists(valid_img_dir_path):
                os.makedirs(valid_img_dir_path)
            if not os.path.exists(valid_label_dir_path):
                os.makedirs(valid_label_dir_path)

            # source_file_names = os.listdir(train_label_dir_path)
            amount_source_files = len(source_file_names)
            file_idx = random.randint(0, amount_source_files - 1)
            cur_file_name = source_file_names.pop(file_idx)

            if not cur_file_name[-4:] == '.txt':
                amount_valid_files -= 1
                continue

            source_label_file_path = source_label_dir_path + '/' + cur_file_name
            source_img_file_path = source_img_dir_path + '/' + cur_file_name[:-4] + '.jpg'

            target_label_file_path = valid_label_dir_path + '/' + cur_file_name
            target_img_file_path = valid_img_dir_path + '/' + cur_file_name[:-4] + '.jpg'

            shutil.move(source_label_file_path, target_label_file_path)
            shutil.move(source_img_file_path, target_img_file_path)

            amount_valid_files -= 1

        while amount_test_files != 0:
            if not os.path.exists(test_img_dir_path):
                os.makedirs(test_img_dir_path)
            if not os.path.exists(test_label_dir_path):
                os.makedirs(test_label_dir_path)

            # source_file_names = os.listdir(train_label_dir_path)
            amount_source_files = len(source_file_names)
            file_idx = random.randint(0, amount_source_files - 1)
            cur_file_name = source_file_names.pop(file_idx)

            if not cur_file_name[-4:] == '.txt':
                amount_test_files -= 1
                continue

            source_label_file_path = source_label_dir_path + '/' + cur_file_name
            source_img_file_path = source_img_dir_path + '/' + cur_file_name[:-4] + '.jpg'

            target_label_file_path = test_label_dir_path + '/' + cur_file_name
            target_img_file_path = test_img_dir_path + '/' + cur_file_name[:-4] + '.jpg'

            shutil.move(source_label_file_path, target_label_file_path)
            shutil.move(source_img_file_path, target_img_file_path)

            amount_test_files -= 1

        # добавляем пустые файлы
        source_empty_dir = source_path + '/' + EMPTY_DIR_NAME
        empty_file_names = os.listdir(source_empty_dir)
        amount_empty_all_files = amount_empty_valid_files + amount_empty_train_files
        if amount_empty_all_files > len(empty_file_names):
            print(f'Не хватает empty files')
            exit()

        empty_file_names_for_train = []
        empty_file_names_for_valid = []

        random.shuffle(empty_file_names)

        for _ in range(amount_empty_train_files):
            file_name = empty_file_names.pop()
            empty_file_names_for_train.append(file_name)

        for _ in range(amount_empty_valid_files):
            file_name = empty_file_names.pop()
            empty_file_names_for_valid.append(file_name)

        for file_name in empty_file_names_for_train:
            source_empty_file_path = source_empty_dir + '/' + file_name
            target_empty_file_path = train_img_dir_path + '/' + file_name
            shutil.copyfile(source_empty_file_path, target_empty_file_path)
            empty_label_file_path = train_label_dir_path + '/' + file_name[:-4] + '.txt'
            file = open(empty_label_file_path, 'w')
            file.close()

        for file_name in empty_file_names_for_valid:
            source_empty_file_path = source_empty_dir + '/' + file_name
            target_empty_file_path = valid_img_dir_path + '/' + file_name
            shutil.copyfile(source_empty_file_path, target_empty_file_path)
            empty_label_file_path = valid_label_dir_path + '/' + file_name[:-4] + '.txt'
            file = open(empty_label_file_path, 'w')
            file.close()



        #формируем yaml файл
        # TODO переделать логику метода с учетом имен классов
        export_names = {0: 'human'}
        valid_data = True
        test_data = False
        self.get_yaml_file(export_names, new_data_path, valid_data, test_data)

