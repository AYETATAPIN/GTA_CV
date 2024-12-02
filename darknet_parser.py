import os

DATASET_DIR = "empty_road/train"


def parse_darknet(dataset_path):
    parsed_data = []
    files = os.listdir(dataset_path)
    paired_files = zip(files[::2], files[1::2])
    cnt = 0
    for file1, file2 in paired_files:
        name1, extension1 = os.path.splitext(file1)
        name2, extension2 = os.path.splitext(file2)
        with open(f"{dataset_path}/{file2}") as bb:
            parsed_data.append({"image": f"{name1}{extension1}", "bbox": bb.readlines()})
            bbox_cnt = len(parsed_data[cnt]["bbox"])
            for i in range(bbox_cnt):
                bbox = parsed_data[cnt]["bbox"][i]
                if bbox_cnt > 1 and i != bbox_cnt - 1:
                    parsed_data[cnt]["bbox"][i] = bbox[:-1]
        cnt += 1
    return parsed_data
