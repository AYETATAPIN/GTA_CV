import os
import uuid
import ast
import cv2
import detect_configured
import datetime
import math
import json
import requests

from combine_plates import combine_plates
from os import mkdir

PATH_TO_RESULT_SERVER = "ResultServer.py"
PATH_TO_CLIENT_SERVER = "client/client_app.py"
PATH_TO_MEDIAMTX = "mediamtx.exe"
PATH_TO_STREAMING_FILE = "cars_test.ts"
CAMERA_URL = 'rtsp://localhost:8554/mystream'

PATH_TO_WEIGHTS = "best.pt"

PATH_TO_ORIGINS = "origins"
PATH_TO_CROPS = "crops"

MAX_BOUNDS_DIFFERENCE = 5

REGION = "RUS"


def makedirs():
    if os.path.exists(PATH_TO_ORIGINS) == False:
        mkdir(PATH_TO_ORIGINS)
    if os.path.exists(PATH_TO_CROPS) == False:
        mkdir(PATH_TO_CROPS)


def get_texts_from_letters(letters, plate_names_and_y_coords):
    ans = dict()
    plate_names_and_y_coords = sorted(plate_names_and_y_coords, key=lambda x: x[1])
    letters = sorted(letters, key=lambda x: (x[0][1]['y_min'], x[0][1]['x_min']))

    for i in range(len(plate_names_and_y_coords)):
        word = ""
        current_y = plate_names_and_y_coords[i][1]

        if i < len(plate_names_and_y_coords) - 1:
            next_y = plate_names_and_y_coords[i + 1][1]
        else:
            next_y = float('inf')

        line_letters = []

        for letter in letters:
            y_center = (letter[0][1]['y_min'] + letter[0][1]['y_max']) / 2
            if current_y <= y_center < next_y:
                line_letters.append(letter)

        line_letters = sorted(line_letters, key=lambda x: x[0][1]['x_min'])

        for letter in line_letters:
            char = letter[0][0]
            if REGION == "RUS" and char in "RUS":
                continue
            word += char

        ans[plate_names_and_y_coords[i][0]] = word
    return ans


def correct_plate_texts(corresponding_plates_texts):
    letter_replacements = {
        '4': 'A',
        '8': 'B',
        'R': 'K',
        'N': 'M',
        '0': 'O',
        'Q': 'O',
        'D': 'O',
        'F': 'P',
        'W': 'Y',
        'U': 'Y',
        'V': 'X'
    }

    digit_replacements = {
        'O': '0',
        'Q': '0',
        'D': '0',
        'I': '1',
        'T': '1',
        'Z': '2',
        'A': '4',
        'S': '5',
        'B': '8',
        'E': '8'
    }

    valid_letters = set("ABEKMHOPCTYX")
    valid_digits = set("0123456789")
    max_length = 6

    corrected_plates_texts = dict()

    for plate_name, plate_text in corresponding_plates_texts.items():
        text = plate_text.upper()
        corrected_text = ""
        i = 0
        j = 0

        while i < max_length and (i + j) < len(text):
            current_char = text[i + j]
            current_pos = i

            if current_pos in {0, 4, 5}:
                if current_char in letter_replacements:
                    corrected_text += letter_replacements[current_char]
                    i += 1
                elif current_char in valid_letters:
                    corrected_text += current_char
                    i += 1
                else:
                    j += 1
            else:
                if current_char in valid_digits:
                    corrected_text += current_char
                    i += 1
                elif current_char in digit_replacements:
                    corrected_text += digit_replacements[current_char]
                    i += 1
                else:
                    j += 1

        corrected_plates_texts[plate_name] = corrected_text

    return corrected_plates_texts


def plate_inside_car(plate_coords, car_coords):
    if (plate_coords[0] >= car_coords[0] or abs(
            plate_coords[0] - car_coords[0]) < MAX_BOUNDS_DIFFERENCE) and (
            plate_coords[2] <= car_coords[2] or abs(
        plate_coords[2] - car_coords[2]) < MAX_BOUNDS_DIFFERENCE) and (
            plate_coords[1] >= car_coords[1] or abs(
        plate_coords[1] - car_coords[1]) < MAX_BOUNDS_DIFFERENCE) and (
            plate_coords[3] <= car_coords[3] or abs(
        plate_coords[3] - car_coords[3]) < MAX_BOUNDS_DIFFERENCE):
        return True
    return False


def calc_distance(plate_coords, car_coords):
    x11, y11, x12, y12 = plate_coords
    x21, y21, x22, y22 = car_coords

    mean_x1 = (x11 + x12) / 2
    mean_y1 = (y11 + y12) / 2

    mean_x2 = (x21 + x22) / 2
    mean_y2 = (y21 + y22) / 2

    return math.sqrt((mean_x2 - mean_x1) ** 2 + (mean_y2 - mean_y1) ** 2)


def find_nearest_centroid(plate_name, cars_labels, cars_folder):
    corresponding_car_image = ""
    plate_label = f"{plate_name}.txt"

    with open(plate_label, "r") as file:
        plate_coords = [int(coord) for coord in file.readline().split()]

    min_distance_value = -1

    for car_label in cars_labels:
        car_name, img_extension = os.path.splitext(car_label)
        car_name = f"{cars_folder}/{car_name}"
        car_label = f"{car_name}.txt"
        car_img = car_label.replace("txt", "jpg")

        with open(car_label, "r") as file:
            car_coords = [int(coord) for coord in file.readline().split()]

        if plate_inside_car(plate_coords, car_coords) == True:
            current_distance = calc_distance(plate_coords, car_coords)

            if min_distance_value == -1:
                min_distance_value = current_distance
                corresponding_car_image = car_img
            else:
                if current_distance < min_distance_value:
                    min_distance_value = current_distance
                    corresponding_car_image = car_img

    corresponding_car_label = corresponding_car_image.replace("jpg", "txt")

    with open(corresponding_car_label, "r") as file:
        corresponding_car_coords = [int(coord) for coord in file.readline().split()]

    return corresponding_car_image, corresponding_car_coords


def start_camera_simualtion(path_to_media_mtx, path_to_streaming_file):
    os.system(f"start {path_to_media_mtx}")
    os.system(f"start ffmpeg "
              f"-re -stream_loop "
              f"-1 -i {path_to_streaming_file} -c copy "
              f"-f rtsp -rtsp_transport tcp "
              f"rtsp://localhost:8554/mystream"
              )


def start_result_server(path_to_result_server):
    os.system(f"start python {path_to_result_server}")


def start_client_server(path_to_client_server):
    os.system(f"start python {path_to_client_server}")


def get_license_plate_text(path_to_license_plate):
    url = "https://www.sigmaltd.space/translator/ScreenTranslatorAPI/process"
    headers = {
        "accept": "application/json",
    }

    params = {
        "size": 1500,
        "conf": 0.2,
        "iou": 0.3,
        "agnostic": True,
        "multi_label": False,
        "max_det": 3000,
        "amp": True,
        "half_precision": True,
        "rough_text_recognition": True
    }

    files = {
        "File": (path_to_license_plate, open(path_to_license_plate, "rb"), "image/jpeg"),
        "Params": (None, json.dumps(params), "application/json")
    }

    return requests.post(url, headers=headers, files=files)


def post_to_result_server(path_to_image, json_with_plate_text, current_time):
    with open(json_with_plate_text, "r") as file:
        json_data = json.load(file)

    extracted_text = json_data["detected_text"]
    files = {"image": open(path_to_image, "rb")}
    data = {"license_plate": extracted_text,
            "date_time": current_time}

    return requests.post("http://127.0.0.1:50505/savephoto", files=files, data=data)


def start_footage_processing(camera_url):
    cap = cv2.VideoCapture(camera_url)
    stream_name = camera_url.replace("/", " ").replace(".", " ").split()[-1]
    width_org = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height_org = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    print(f'Width: {width_org} | Height: {height_org} | FPS: {fps}')

    out_video_name = f"{stream_name}.mp4"
    out_video = cv2.VideoWriter(out_video_name,
                                cv2.VideoWriter_fourcc(*'mp4v'),
                                fps,
                                (1800, 1000))

    while True:
        ret, camera_frame = cap.read()  # blocking operation

        if not ret:
            break

        camera_frame = cv2.resize(camera_frame, (1800, 1000))

        current_time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        os_random_int = uuid.uuid4()

        img_name = f"{PATH_TO_ORIGINS}/{stream_name}__{current_time}__{os_random_int}.jpg"

        cv2.imwrite(img_name, camera_frame)
        crop_folder_name = f"{stream_name}__{current_time}__{os_random_int}"

        detect_configured.run(source=img_name,
                              weights=PATH_TO_WEIGHTS,
                              project=PATH_TO_CROPS,
                              save_crop=True,
                              save_txt=True,
                              save_format=1,
                              name=crop_folder_name,
                              conf_thres=0.5,
                              device="0"
                              )

        img_with_detection_name = f"{PATH_TO_CROPS}/{crop_folder_name}/{crop_folder_name}.jpg"
        img_with_detection = cv2.imread(img_with_detection_name)

        plates_folder = f"{PATH_TO_CROPS}/{crop_folder_name}/License plate"
        cars_folder = f"{PATH_TO_CROPS}/{crop_folder_name}/car"

        if os.path.isdir(plates_folder) is False:
            print("No license plates detected")
            out_video.write(img_with_detection)
            cv2.imshow("RTSP camera", img_with_detection)
            cv2.waitKey(1)
            continue

        plates_images = [f for f in os.listdir(plates_folder) if
                         f[-3:] != "txt" and os.path.isfile(os.path.join(plates_folder, f))]
        plates_labels = [f for f in os.listdir(plates_folder) if
                         f[-3:] == "txt" and os.path.isfile(os.path.join(plates_folder, f))]

        cars_images = [f for f in os.listdir(cars_folder) if
                       f[-3:] != "txt" and os.path.isfile(os.path.join(cars_folder, f))]
        cars_labels = [f for f in os.listdir(cars_folder) if
                       f[-3:] == "txt" and os.path.isfile(os.path.join(cars_folder, f))]

        combined_plates_img, plate_names_and_y_coords = combine_plates(plates_folder)

        if len(plate_names_and_y_coords) == 0:
            print(combined_plates_img)
            exit(1)
        else:
            plate_response_body = get_license_plate_text(combined_plates_img).json()["recognized_text"]
            detected_letters = ast.literal_eval(plate_response_body)

            letters = []
            letters_ct = 0

            while True:
                try:
                    new_letter = []
                    keys = []

                    current_letter = detected_letters[letters_ct]
                    letters_ct += 1

                    for key in current_letter.keys():
                        keys.append(key)

                    if len(keys) > 1:
                        raise Exception("More than 1 letter for 1 coordinate")

                    new_letter.append(keys[0])
                    new_letter.append(current_letter[keys[0]])

                    letters.append([new_letter])
                except Exception as E:
                    if E.args[0] == letters_ct:
                        break
                    else:
                        print(E)
                        exit(1)

        corresponding_plates_texts = get_texts_from_letters(letters, plate_names_and_y_coords)
        corresponding_plates_texts = correct_plate_texts(corresponding_plates_texts)

        for plate_image in plates_images:
            plate_name, img_extension = os.path.splitext(plate_image)
            plate_name = f"{plates_folder}/{plate_name}"
            plate_img_path = f"{plate_name}.jpg"
            plate_label = f"{plate_name}.txt"

            json_with_plate_text = f"{plate_name}.json"
            extracted_text = corresponding_plates_texts[plate_img_path].upper()
            print(f"\n\n\n {type(extracted_text), extracted_text, plate_name} \n\n\n")

            with open(json_with_plate_text, "w") as file:
                file.write(f"{{\n\t\"detected_text\": \"{extracted_text}\"\n}}")

            with open(plate_label, "r") as file:
                plate_coords = [int(coord) for coord in file.readline().split()]

            corresponding_car_image, corresponding_car_coords = find_nearest_centroid(plate_name, cars_labels,
                                                                                      cars_folder)

            if corresponding_car_image == "":
                print(f"No car for plate {plate_name} with coordinates {plate_coords} was found")
                continue

            post_to_result_server(corresponding_car_image, json_with_plate_text, current_time)

            cv2.putText(img_with_detection,
                        f"License plate: {extracted_text}",
                        (int(corresponding_car_coords[0] + 10), int(corresponding_car_coords[1] + 45)),
                        cv2.FONT_HERSHEY_DUPLEX,
                        1,
                        (0, 0, 255),
                        2)

        out_video.write(img_with_detection)
        cv2.imshow("RTSP camera", img_with_detection)
        cv2.waitKey(1)
    cap.release()
    out_video.release()


def main():
    start_camera_simualtion(PATH_TO_MEDIAMTX, PATH_TO_STREAMING_FILE)
    start_result_server(PATH_TO_RESULT_SERVER)
    start_client_server(PATH_TO_CLIENT_SERVER)
    makedirs()
    start_footage_processing(CAMERA_URL)


if __name__ == "__main__":
    main()
