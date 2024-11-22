import os
import shutil
from PIL import Image

from train_data_parser import parse_matlab

DATASET_DIR = "dataset/cars_train/cars_train"


# создание директории с датасетом в формате YOLO
def makedir(dataset_path):
    source_name = dataset_path.split("/")[-1]
    yolo_dataset_path = f"{source_name}_to_YOLO"
    os.mkdir(yolo_dataset_path)
    os.mkdir(f"{yolo_dataset_path}/images")
    os.mkdir(f"{yolo_dataset_path}/images/train")
    os.mkdir(f"{yolo_dataset_path}/images/val")
    os.mkdir(f"{yolo_dataset_path}/labels")
    os.mkdir(f"{yolo_dataset_path}/labels/train")
    os.mkdir(f"{yolo_dataset_path}/labels/val")
    return yolo_dataset_path


# создание файла data.yaml
def make_data_yaml(yolo_dataset_path):
    yaml_path = f"{yolo_dataset_path}/data.yaml"
    with open(yaml_path, "w") as file:
        file.write(
            f"path: {yolo_dataset_path}\n"
            f"train: images/train\n"
            f"val: images/val\n\n"
            f"names:\n"
            f"    0: Car\n"
            f"    1: License plate\n")


# преобразование данных из .matlab в YOLO
def data_refactoring(dataset_path):
    prefix_literal = dataset_path.split("/")[0]
    parsed_data = parse_matlab(prefix_literal)
    dataset_size = len(parsed_data)
    train_size = int(dataset_size * 0.9)
    yolo_dataset_path = makedir(DATASET_DIR)
    make_data_yaml(yolo_dataset_path)
    for i in range(train_size): # преобразование подмножества train
        source_image = f"{DATASET_DIR}/{parsed_data[i]['image'][0]}"
        new_image = f"{yolo_dataset_path}/images/train"
        shutil.copy(source_image, new_image)
        source_bbox = f"{parsed_data[i]['image'][0][:-4]}.txt"
        new_bbox = f"{yolo_dataset_path}/labels/train/{source_bbox}"
        source_coordinates = parsed_data[i]['bbox']
        with Image.open(source_image) as img:
            width, height = img.size
            if width <= 0 or height <= 0:
                raise ValueError(f"Invalid image size: {width}x{height}")
            if not (0 <= source_coordinates[0] < source_coordinates[2] <= width and
                    0 <= source_coordinates[1] < source_coordinates[3] <= height):
                raise ValueError(f"Invalid bbox coordinates: {source_coordinates}")
            width = float(width)
            height = float(height)
            source_coordinates = [float(coord) for coord in source_coordinates]
            new_coordinates = (f"0 "
                               f"{(source_coordinates[0] + source_coordinates[2]) / (2 * width)} " # преобразование координат bbox'а
                               f"{(source_coordinates[1] + source_coordinates[3]) / (2 * height)} "
                               f"{(source_coordinates[2] - source_coordinates[0]) / width} "
                               f"{(source_coordinates[3] - source_coordinates[1]) / height} ")
            with open(new_bbox, "w") as file:
                file.write(new_coordinates)

    for i in range(train_size, dataset_size): # преобразование подмножества validation
        source_image = f"{DATASET_DIR}/{parsed_data[i]['image'][0]}"
        new_image = f"{yolo_dataset_path}/images/val"
        shutil.copy(source_image, new_image)
        source_bbox = f"{parsed_data[i]['image'][0][:-4]}.txt"
        new_bbox = f"{yolo_dataset_path}/labels/val/{source_bbox}"
        source_coordinates = parsed_data[i]['bbox']
        with Image.open(source_image) as img:
            width, height = img.size
            if width <= 0 or height <= 0:
                raise ValueError(f"Недопустимые размеры изображения: {width}x{height}")
            if not (0 <= source_coordinates[0] < source_coordinates[2] <= width and
                    0 <= source_coordinates[1] < source_coordinates[3] <= height):
                raise ValueError(f"Invalid bbox coordinates: {source_coordinates}")
            width = float(width)
            height = float(height)
            source_coordinates = [float(coord) for coord in source_coordinates]
            new_coordinates = (f"0 "
                               f"{(source_coordinates[0] + source_coordinates[2]) / (2 * width)} " # преобразование координат bbox'а
                               f"{(source_coordinates[1] + source_coordinates[3]) / (2 * height)} "
                               f"{(source_coordinates[2] - source_coordinates[0]) / width} "
                               f"{(source_coordinates[3] - source_coordinates[1]) / height} ")
            with open(new_bbox, "w") as file:
                file.write(new_coordinates)
