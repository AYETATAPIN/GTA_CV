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