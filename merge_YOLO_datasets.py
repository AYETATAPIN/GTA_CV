import os
import shutil

from data_yaml_maker import make_data_yaml

FIRST_DIR = "cars_train_to_YOLO"
SECOND_DIR = "empty_road_to_YOLO"


def makedir(first_path, second_path):
    combined_folder = f"{first_path[:-8]}_and_{second_path[:-8]}_to_YOLO"
    os.mkdir(combined_folder)
    os.mkdir(f"{combined_folder}/images")
    os.mkdir(f"{combined_folder}/images/train")
    os.mkdir(f"{combined_folder}/images/val")
    os.mkdir(f"{combined_folder}/labels")
    os.mkdir(f"{combined_folder}/labels/train")
    os.mkdir(f"{combined_folder}/labels/val")
    return combined_folder


def copy_and_rename(path, combined_folder):
    images_count = 0
    labels_count = 0
    for root, dirs, files in os.walk(path):
        print(root, dirs, files)
        subdirs = str(root).split("\\")
        if len(subdirs) > 1:
            if subdirs[-2] == "images":
                if subdirs[-1] == "train":
                    for file in files:
                        source_image = f"{root}/{file}"
                        source_image_name, source_image_extension = os.path.splitext(source_image)
                        new_image = f"{combined_folder}/images/train/{file}"
                        shutil.copy(source_image, f"{combined_folder}/images/train")
                        os.rename(new_image,
                                  f"{combined_folder}/images/train/{subdirs[0]}_{images_count}{source_image_extension}")
                        images_count += 1
                else:
                    for file in files:
                        source_image = f"{root}/{file}"
                        source_image_name, source_image_extension = os.path.splitext(source_image)
                        new_image = f"{combined_folder}/images/val/{file}"
                        shutil.copy(source_image, f"{combined_folder}/images/val")
                        os.rename(new_image,
                                  f"{combined_folder}/images/val/{subdirs[0]}_{images_count}{source_image_extension}")
                        images_count += 1
                print("1")
            elif subdirs[-2] == "labels":
                if subdirs[-1] == "train":
                    for file in files:
                        source_label = f"{root}/{file}"
                        source_label_name, source_label_extension = os.path.splitext(source_label)
                        new_label = f"{combined_folder}/labels/train/{file}"
                        shutil.copy(source_label, f"{combined_folder}/labels/train")
                        os.rename(new_label,
                                  f"{combined_folder}/labels/train/{subdirs[0]}_{labels_count}{source_label_extension}")
                        labels_count += 1
                else:
                    for file in files:
                        source_label = f"{root}/{file}"
                        source_label_name, source_label_extension = os.path.splitext(source_label)
                        new_label = f"{combined_folder}/labels/val/{file}"
                        shutil.copy(source_label, f"{combined_folder}/labels/val")
                        os.rename(new_label,
                                  f"{combined_folder}/labels/val/{subdirs[0]}_{labels_count}{source_label_extension}")
                        labels_count += 1


def dataset_zip(first_path, second_path):
    combined_folder = makedir(first_path, second_path)
    make_data_yaml(combined_folder)
    copy_and_rename(first_path, combined_folder)
    copy_and_rename(second_path, combined_folder)


dataset_zip(FIRST_DIR, SECOND_DIR)
