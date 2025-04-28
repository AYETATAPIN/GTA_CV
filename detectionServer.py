import os
import uuid
from time import sleep

import cv2
import detect_configured
import datetime
import multiprocessing
import json
import requests

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

img_names = dict()  # 1 - processed, 0 - not

crossed_endpoint = dict()  # [0 - none, 1 - first, 2 - second ; crossed timecode ; speed]

MAX_BOUNDS_DIFFERENCE = 20


def start_camera_simualtion(path_to_media_mtx, path_to_streaming_file):
    os.system(f"start {path_to_media_mtx}")
    sleep(1)
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


def get_license_plate_text(path_to_license_plate, json_with_plate_text):
    # with open(json_with_plate_text, "w") as file:  # temporarily
    #     file.write('{\n\t"detected_text": "911GG"\n}')
    files = {"File": open(path_to_license_plate, "rb")}
    return requests.post("http://127.0.0.1:5000/ScreenTranslatorAPI/imageDetect", files=files)


def post_to_result_server(path_to_image, json_with_plate_text, current_time):
    with open(json_with_plate_text, "r") as file:
        json_data = json.load(file)
    extracted_text = json_data["detected_text"]
    files = {"image": open(path_to_image, "rb")}
    data = {"license_plate": extracted_text,
            "date_time": current_time}
    return requests.post("http://127.0.0.1:50505/savephoto", files=files, data=data)


def camera_handling(camera_url):
    # cap = cv2.VideoCapture(camera_url)
    cap = cv2.VideoCapture("cars.mp4")

    width_org = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height_org = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frames_ct = 0
    print(f'Width: {width_org} | Height: {height_org} | FPS: {fps}')

    crossed_endpoint["example"] = [0, 0, 0]

    while True:
        ret, camera_frame = cap.read()  # blocking operation
        # img = cv2.resize(img, (1280, 720))
        frames_ct += 1
        current_timecode = frames_ct / fps

        current_time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        os_random_int = uuid.uuid4()
        camera_name = (camera_url.split("/"))[-1]
        img_name = f"{PATH_TO_ORIGINS}/{camera_name}__{current_time}__{os_random_int}.jpg"
        img_names[img_name] = 0

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
        img_names[img_name] = 1
        img_with_detection_name = f"{PATH_TO_CROPS}/{crop_folder_name}/{crop_folder_name}.jpg"
        img_with_detection = cv2.imread(img_with_detection_name)
        # img_with_detection = cv2.resize(img_with_detection, (1280, 720))
        # cv2.imshow("RTSP camera", camera_frame)
        # cv2.imshow("RTSP camera", img_with_detection)
        # cv2.waitKey(1)

        plates_folder = f"{PATH_TO_CROPS}/{crop_folder_name}/License plate"
        if os.path.isdir(plates_folder) is False:
            print("No license plates detected")
            continue
        plates_images = [f for f in os.listdir(plates_folder) if
                         f[-3:] != "txt" and os.path.isfile(os.path.join(plates_folder, f))]
        plates_labels = [f for f in os.listdir(plates_folder) if
                         f[-3:] == "txt" and os.path.isfile(os.path.join(plates_folder, f))]

        cars_folder = f"{PATH_TO_CROPS}/{crop_folder_name}/car"
        cars_images = [f for f in os.listdir(cars_folder) if
                       f[-3:] != "txt" and os.path.isfile(os.path.join(cars_folder, f))]
        cars_labels = [f for f in os.listdir(cars_folder) if
                       f[-3:] == "txt" and os.path.isfile(os.path.join(cars_folder, f))]

        for plate_image in plates_images:
            plate_name, img_extension = os.path.splitext(plate_image)
            plate_img_path = f"{plates_folder}/{plate_image}"
            plate_name = f"{plates_folder}/{plate_name}"
            json_with_plate_text = f"{plate_name}.json"
            # get_plate_routine = multiprocessing.Process(target=get_license_plate_text,
            #                                             args=(plate_image, json_with_plate_text,))
            # get_plate_routine.start()
            # get_plate_routine.join()
            plate_response_body = get_license_plate_text(plate_img_path, json_with_plate_text).json()
            extracted_text = plate_response_body["Detected text"]
            print(f"\n\n\n {type(extracted_text), extracted_text, plate_name} \n\n\n")
            with open(json_with_plate_text, "w") as file:
                file.write(f"{{\n\t\"detected_text\": \"{extracted_text}\"\n}}")

            # with open(json_with_plate_text, "r") as file:
            #     json_data = json.load(file)
            # extracted_text = json_data["detected_text"

            if crossed_endpoint.get(extracted_text, -1) == -1:
                # crossed_endpoint[extracted_text] = {0, 0, 0}
                crossed_endpoint[extracted_text] = [0, 0, "undefined"]

            plate_label = f"{plate_name}.txt"
            with open(plate_label, "r") as file:
                plate_coords = [int(coord) for coord in file.readline().split()]
            plate_inside_car = False
            current_car_speed = "undefined"
            for car_label in cars_labels:
                car_name, img_extension = os.path.splitext(car_label)
                car_name = f"{cars_folder}/{car_name}"
                car_label = f"{car_name}.txt"
                with open(car_label, "r") as file:
                    car_coords = [int(coord) for coord in file.readline().split()]

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
                                current_car_speed = current_timecode - crossed_endpoint[extracted_text][1]
                    crossed_endpoint[extracted_text][2] = current_car_speed
                    if (plate_coords[0] >= car_coords[0] or abs(
                            plate_coords[0] - car_coords[0]) < MAX_BOUNDS_DIFFERENCE) and (
                            plate_coords[2] <= car_coords[2] or abs(
                        plate_coords[2] - car_coords[2]) < MAX_BOUNDS_DIFFERENCE) and (
                            plate_coords[1] >= car_coords[1] or abs(
                        plate_coords[1] - car_coords[1]) < MAX_BOUNDS_DIFFERENCE) and (
                            plate_coords[3] <= car_coords[3] or abs(
                        plate_coords[3] - car_coords[3]) < MAX_BOUNDS_DIFFERENCE):
                        plate_inside_car = True
                    if plate_inside_car == True:
                        corresponding_car_image = car_label.replace("txt", "jpg")
                        break
            if plate_inside_car == False:
                print(f"No car for plate {plate_name} with coordinates {plate_coords} was found")
                continue
            post_result = post_to_result_server(corresponding_car_image, json_with_plate_text, current_time)
            print(post_result)
            if crossed_endpoint[extracted_text][2] != "undefined" and crossed_endpoint[extracted_text][2] < 0:
                print(
                    f"Unexpected speed '{crossed_endpoint[extracted_text][2]}' of car with license plate {extracted_text}")
            cv2.putText(img_with_detection,
                        f"License plate: {extracted_text}",
                        (int(car_coords[0] + 10), int(car_coords[1] + 40)),
                        cv2.FONT_HERSHEY_DUPLEX,
                        1,
                        (0, 0, 255),
                        2)
            cv2.putText(img_with_detection,
                        f"Speed: {str(crossed_endpoint[extracted_text][2])}",
                        (int(car_coords[0] + 10), int(car_coords[1] + 90)),
                        cv2.FONT_HERSHEY_DUPLEX,
                        1,
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
    sleep(1)
    camera_handling(CAMERA_URL)

if __name__ == "__main__":
    main()
