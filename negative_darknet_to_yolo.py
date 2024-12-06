import os
import shutil

from darknet_parser import parse_darknet
from data_yaml_maker import make_data_yaml

DATASET_DIR = "empty_road/train"  # путь к датасету


# создание директории с датасетом в формате YOLO
def makedir(dataset_path):
    source_name = dataset_path.split("/")[0]
    yolo_dataset_path = f"{source_name}_to_YOLO"
    os.mkdir(yolo_dataset_path)
    os.mkdir(f"{yolo_dataset_path}/images")
    os.mkdir(f"{yolo_dataset_path}/images/train")
    os.mkdir(f"{yolo_dataset_path}/images/val")
    os.mkdir(f"{yolo_dataset_path}/labels")
    os.mkdir(f"{yolo_dataset_path}/labels/train")
    os.mkdir(f"{yolo_dataset_path}/labels/val")
    return yolo_dataset_path


# преобразование данных из .matlab в YOLO
def data_refactoring(dataset_path):
    prefix_literal = dataset_path.split("/")[0]
    parsed_data = parse_darknet(f"{prefix_literal}/train")
    dataset_size = len(parsed_data)
    train_size = int(dataset_size * 0.9)
    yolo_dataset_path = makedir(DATASET_DIR)
    make_data_yaml(yolo_dataset_path)
    for i in range(train_size):  # преобразование подмножества train
        source_image = f"{DATASET_DIR}/{parsed_data[i]['image']}"
        new_image = f"{yolo_dataset_path}/images/train"
        source_bbox = f"{parsed_data[i]['image'][:-4]}.txt"
        new_bbox = f"{yolo_dataset_path}/labels/train/{source_bbox}"
        source_coordinates = parsed_data[i]['bbox']
        if len(source_coordinates) != 0:
            continue
        shutil.copy(source_image, new_image)
        with open(new_bbox, "w") as file:
            file.write("")

    for i in range(train_size, dataset_size):  # преобразование подмножества validation
        source_image = f"{DATASET_DIR}/{parsed_data[i]['image']}"
        new_image = f"{yolo_dataset_path}/images/val"
        source_bbox = f"{parsed_data[i]['image'][:-4]}.txt"
        new_bbox = f"{yolo_dataset_path}/labels/val/{source_bbox}"
        source_coordinates = parsed_data[i]['bbox']
        if len(source_coordinates) != 0:
            continue
        shutil.copy(source_image, new_image)
        with open(new_bbox, "w") as file:
            file.write("")
