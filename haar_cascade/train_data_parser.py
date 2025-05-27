import scipy.io as sio  # библиотека для работы с разметкой
import cv2 as cv

DATASET_DIR = "dataset"  # путь к датасету


class DatasetImage:
    def __init__(self, data, dataset_dir):
        self.data = data
        self.index = 0
        self.dataset_dir = dataset_dir

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.data):
            raise None
        value = self.data[self.index]
        self.index += 1
        image_path = f"{self.dataset_dir}/cars_train/cars_train/{value['image'][0]}"
        return cv.imread(image_path), value["image"][1], value["bbox"]


# Парсер .mat
def parse_matlab(dataset_dir):
    cars_data = sio.loadmat(f"{dataset_dir}/car_devkit/devkit/cars_train_annos.mat")  # файл с разметкой изображений
    cars_classes = sio.loadmat(f"{dataset_dir}/car_devkit/devkit/cars_meta.mat")  # файл с разметкой изображений
    cars_data_struct = cars_data["annotations"]  # структура разметки изображений
    cars_classes_struct = cars_classes["class_names"]  # структура классов машин
    parsed_data = []  # данные в нормальном виде
    for data_rows in cars_data_struct:
        for row in data_rows:
            # координаты bounding box
            bbox_x1 = row["bbox_x1"][0][0]
            bbox_y1 = row["bbox_y1"][0][0]
            bbox_x2 = row["bbox_x2"][0][0]
            bbox_y2 = row["bbox_y2"][0][0]
            fname = row["fname"][0]  # имя изображения
            class_id = row["class"][0][0]  # класс машины на изображении (число)
            class_name = cars_classes_struct[0][class_id - 1][0]  # название машины (строка)
            img = [fname, class_name]
            bbox = [bbox_x1, bbox_y1, bbox_x2, bbox_y2]
            parsed_data.append({"image": img, "bbox": bbox})
    return parsed_data


# Объект с изображениями и их данными
def parse_data(dataset_dir):
    matlab_data = parse_matlab(dataset_dir)
    current_image = DatasetImage(matlab_data, dataset_dir)
    return current_image


# Пример использования
def test_usage():
    images = parse_data(DATASET_DIR)
    first_img, first_name, first_bb = next(images)
    second_img, second_name, second_bb = next(images)

    cv.rectangle(first_img, (first_bb[0], first_bb[1]), (first_bb[2], first_bb[3]), color=(0, 0, 255), thickness=2)
    cv.putText(first_img, first_name, (first_bb[0] + 10, first_bb[1] - 10), cv.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
    cv.imshow(first_name, first_img)
    cv.waitKey()
    cv.destroyWindow(first_name)

    cv.rectangle(second_img, (second_bb[0], second_bb[1]), (second_bb[2], second_bb[3]), color=(0, 0, 255), thickness=2)
    cv.putText(second_img, second_name, (second_bb[0] + 10, second_bb[1] - 10), cv.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0),2)
    cv.imshow(second_name, second_img)
    cv.waitKey()
    cv.destroyWindow(second_name)
