import os
import uuid
import cv2
import detect_configured
import datetime
import math
import json
import requests

from combine_plates import combine_plates

PATH_TO_RESULT_SERVER = "D:/prg/pycharm/projects/zmeyuka/yolov5/ResultServer.py"
PATH_TO_TEXT_EXTRACTION_SERVER = "D:/prg/pycharm/projects/zmeyuka/yolov5/Server/server.py"
PATH_TO_MEDIAMTX = "D:/prg/pycharm/projects/zmeyuka/mediamtx/mediamtx.exe"
PATH_TO_STREAMING_FILE = "D:/prg/pycharm/projects/zmeyuka/yolov5/ts_streams/cars_road.ts"
CAMERA_URL = 'rtsp://localhost:8554/mystream'

PATH_TO_WEIGHTS = "D:/prg/pycharm/projects/zmeyuka/yolov5/saved_models/kaggle_trained/weights/best.pt"

PATH_TO_ORIGINS = "D:/prg/zalupen/origins"
PATH_TO_CROPS = "D:/prg/zalupen/crops"
# ffmpeg -re -stream_loop -1 -i cars_test.ts -c copy -f rtsp -rtsp_transport tcp rtsp://localhost:8554/mystream

FIRST_ENDPOINT_X = 100
FIRST_ENDPOINT_Y = 100

SECOND_ENDPOINT_X = 200
SECOND_ENDPOINT_Y = 200

DISTANCE_BETWEEN_ENDPOINTS = 5

crossed_endpoint = dict()  # [0 - none, 1 - first, 2 - second ; crossed timecode ; speed]

MAX_BOUNDS_DIFFERENCE = 5

REGION = "RUS"


def get_texts_from_letters(letters, plate_names_and_y_coords):
    ans = {}
    plate_names_and_y_coords = sorted(plate_names_and_y_coords, key=lambda y: y[1])
    letters = sorted(letters, key=lambda x: x[1][0])
    for i in range(len(plate_names_and_y_coords)):
        word = ""
        for new_el in letters:
            if (new_el[1][1] >= plate_names_and_y_coords[i][1]
                    and (i == len(plate_names_and_y_coords) - 1 or new_el[1][1] <= plate_names_and_y_coords[i + 1][1])):
                if (REGION == "RUS"):
                    s = new_el[0]
                    if (s == "R" or s == "U" or s == "S"):
                        continue
                word = word + new_el[0]
        ans[plate_names_and_y_coords[0]] = word
    return ans


def calc_distance(plate_coords, car_coords):
    x11, y11, x12, y12 = plate_coords
    x21, y21, x22, y22 = car_coords

    mean_x1 = (x11 + x12) / 2
    mean_y1 = (y11 + y12) / 2

    mean_x2 = (x21 + x22) / 2
    mean_y2 = (y21 + y22) / 2

    return math.sqrt((mean_x2 - mean_x1) ** 2 + (mean_y2 - mean_y1) ** 2)


def calc_speed(plate_coords, extracted_text, current_timecode):
    current_car_speed = "undefined"
    mean_x = (plate_coords[0] + plate_coords[2]) / 2
    mean_y = (plate_coords[1] + plate_coords[3]) / 2

    if crossed_endpoint.get(extracted_text, 0)[0] == 0:
        if mean_x >= FIRST_ENDPOINT_X and mean_y >= FIRST_ENDPOINT_Y:
            crossed_endpoint[extracted_text] = [1, current_timecode, current_car_speed]
    if mean_x >= SECOND_ENDPOINT_X and mean_y >= SECOND_ENDPOINT_Y:
        if crossed_endpoint.get(extracted_text, 0)[0] != 1:
            print(f"Unable to calculate speed for {extracted_text}")
        else:
            if crossed_endpoint[extracted_text][1] == current_timecode:
                crossed_endpoint[extracted_text][2] = -1
            else:
                crossed_endpoint[extracted_text][0] = 2
                current_car_speed = DISTANCE_BETWEEN_ENDPOINTS / (
                        (current_timecode - crossed_endpoint[extracted_text][1]) * 3.6)
    crossed_endpoint[extracted_text][2] = current_car_speed


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


def start_text_extraction_server(path_to_extraction_server):
    os.system(f"start python {path_to_extraction_server}")


def get_license_plate_text(path_to_license_plate):
    files = {"File": open(path_to_license_plate, "rb")}
    return requests.post("https://sigmaltd.space/translator/", files=files)
    # return requests.post("http://127.0.0.1:5000/ScreenTranslatorAPI/imageDetect", files=files)


def post_to_result_server(path_to_image, json_with_plate_text, current_time):
    with open(json_with_plate_text, "r") as file:
        json_data = json.load(file)

    extracted_text = json_data["detected_text"]
    files = {"image": open(path_to_image, "rb")}
    data = {"license_plate": extracted_text,
            "date_time": current_time}

    return requests.post("http://127.0.0.1:50505/savephoto", files=files, data=data)


def start_footage_processing(camera_url):
    cap = cv2.VideoCapture("cars.mp4")
    # cap = cv2.VideoCapture(camera_url)

    width_org = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height_org = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frames_ct = 0
    print(f'Width: {width_org} | Height: {height_org} | FPS: {fps}')

    crossed_endpoint["example"] = [0, 0, 0]

    while True:
        ret, camera_frame = cap.read()  # blocking operation
        frames_ct += 1
        current_timecode = frames_ct / fps

        current_time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        os_random_int = uuid.uuid4()
        camera_name = (camera_url.split("/"))[-1]

        img_name = f"{PATH_TO_ORIGINS}/{camera_name}__{current_time}__{os_random_int}.jpg"

        cv2.imwrite(img_name, camera_frame)
        crop_folder_name = f"{camera_name}__{current_time}__{os_random_int}"

        detect_configured.run(source=img_name,
                              weights=PATH_TO_WEIGHTS,
                              project=PATH_TO_CROPS,
                              save_crop=True,
                              save_txt=True,
                              save_format=1,
                              name=crop_folder_name,
                              conf_thres=0.5
                              )

        img_with_detection_name = f"{PATH_TO_CROPS}/{crop_folder_name}/{crop_folder_name}.jpg"
        img_with_detection = cv2.imread(img_with_detection_name)

        plates_folder = f"{PATH_TO_CROPS}/{crop_folder_name}/License plate"
        cars_folder = f"{PATH_TO_CROPS}/{crop_folder_name}/car"

        if os.path.isdir(plates_folder) is False:
            print("No license plates detected")
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
        else:
            plate_response_body = get_license_plate_text(combined_plates_img).json()
            letters = []
            letters_ct = 0
            while True:
                try:
                    new_letter = []
                    keys = []
                    current_letter = plate_response_body[str(letters_ct)]
                    for key in current_letter.keys():
                        keys.append(key)
                    if len(keys) > 1:
                        raise Exception("More than 1 letter for 1 coordinate")
                    new_letter.append(keys[0])
                    new_letter.append(current_letter[keys[0]])
                    letters.append([new_letter])
                except Exception as E:
                    if E.args[0] == "Missing property exception":
                        break
                    else:
                        print(E)

        corresponding_plates_texts = get_texts_from_letters(letters, plate_names_and_y_coords)

        for plate_image in plates_images:
            plate_name, img_extension = os.path.splitext(plate_image)
            plate_name = f"{plates_folder}/{plate_name}"
            plate_img_path = f"{plate_name}.jpg"
            plate_label = f"{plate_name}.txt"

            json_with_plate_text = f"{plate_name}.json"
            extracted_text = corresponding_plates_texts[plate_img_path].lower()
            print(f"\n\n\n {type(extracted_text), extracted_text, plate_name} \n\n\n")

            with open(json_with_plate_text, "w") as file:
                file.write(f"{{\n\t\"detected_text\": \"{extracted_text}\"\n}}")

            if crossed_endpoint.get(extracted_text, -1) == -1:
                crossed_endpoint[extracted_text] = [0, 0, "undefined"]

            with open(plate_label, "r") as file:
                plate_coords = [int(coord) for coord in file.readline().split()]

            calc_speed(plate_coords, extracted_text, current_timecode)

            corresponding_car_image, corresponding_car_coords = find_nearest_centroid(plate_name, cars_labels,
                                                                                      cars_folder)

            if corresponding_car_image == "":
                print(f"No car for plate {plate_name} with coordinates {plate_coords} was found")
                continue

            post_result = post_to_result_server(corresponding_car_image, json_with_plate_text, current_time)
            print(post_result)

            if crossed_endpoint[extracted_text][2] != "undefined" and crossed_endpoint[extracted_text][2] < 0:
                print(
                    f"Unexpected speed '{crossed_endpoint[extracted_text][2]}' of car with license plate {extracted_text}")

            cv2.putText(img_with_detection,
                        f"License plate: {extracted_text}",
                        (int(corresponding_car_coords[0] + 10), int(corresponding_car_coords[1] + 45)),
                        cv2.FONT_HERSHEY_DUPLEX,
                        2,
                        (0, 0, 255),
                        2)

            cv2.putText(img_with_detection,
                        f"Speed: {str(crossed_endpoint[extracted_text][2])}",
                        (int(corresponding_car_coords[0] + 10), int(corresponding_car_coords[1] + 95)),
                        cv2.FONT_HERSHEY_DUPLEX,
                        2,
                        (0, 0, 255),
                        2)

        img_with_detection = cv2.resize(img_with_detection, (1280, 720))
        cv2.imshow("RTSP camera", img_with_detection)
        cv2.waitKey(1)
    cap.release()


def main():
    start_camera_simualtion(PATH_TO_MEDIAMTX, PATH_TO_STREAMING_FILE)
    start_result_server(PATH_TO_RESULT_SERVER)
    start_text_extraction_server(PATH_TO_TEXT_EXTRACTION_SERVER)
    start_footage_processing(CAMERA_URL)


if __name__ == "__main__":
    main()
