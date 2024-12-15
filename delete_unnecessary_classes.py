import os

DATASET_DIR = "multiple_existing_cars"

classes_to_delete = ["99"]


def remove_unnecessary_classes(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()
    classes = [line.split()[0] for line in lines]
    suited_classes = []
    if len(classes) > 0:
        for i in range(len(classes)):
            if classes[i] not in classes_to_delete:
                suited_classes.append(i)
        if len(suited_classes) == 0:
            os.remove(file_path)
            # print(file_path)
            file_path = file_path.replace("labels", "images")[:-4] + ".jpg"
            # print(file_path)
            os.remove(file_path)
        else:
            with open(file_path, "w") as file:
                for index in suited_classes:
                    splitted_line = lines[index].split()
                    splitted_line[0] = "0"
                    lines[index] = ' '.join(splitted_line) + "\n"
                    file.write(lines[index])


def classes_removal(dataset_path):
    for root, dirs, files in os.walk(dataset_path):
        subdirs = str(root).split("\\")
        if len(subdirs) > 2:
            if subdirs[-2] == "labels":
                labels = os.listdir(root)
                for label in labels:
                    remove_unnecessary_classes(f"{root}/{label}")


classes_removal(DATASET_DIR)
