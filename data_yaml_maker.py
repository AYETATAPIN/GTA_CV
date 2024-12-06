# создание файла data.yaml
def make_data_yaml(yolo_dataset_path):
    yaml_path = f"{yolo_dataset_path}/data.yaml"
    with open(yaml_path, "w") as file:
        file.write(
            f"path: {yolo_dataset_path}\n"  # корневая директория
            f"train: images/train\n"  # изображения для обучения
            f"val: images/val\n\n"  # изображения для валидации
            f"names:\n"  # названия классов
            f"    0: Car\n"
            f"    1: License plate\n")
