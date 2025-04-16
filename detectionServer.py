import os
import uuid
from time import sleep

import cv2
import detect
import datetime
import multiprocessing
import requests

PATH_TO_MEDIAMTX = "D:/prg/pycharm/projects/zmeyuka/mediamtx/mediamtx.exe"
PATH_TO_STREAMING_FILE = "D:/prg/pycharm/projects/zmeyuka/yolov5/ts_streams/cars_test.ts"
PATH_TO_WEIGHTS = "D:/prg/pycharm/projects/zmeyuka/yolov5/saved_models/processor_died1337/best.pt"
PATH_TO_ORIGINS = "D:/prg/zalupen/origins"
PATH_TO_CROPS = "D:/prg/zalupen/crops"
CAMERA_URL = 'rtsp://localhost:8554/mystream'
# ffmpeg -re -stream_loop -1 -i cars_test.ts -c copy -f rtsp -rtsp_transport tcp rtsp://localhost:8554/mystream

img_names = dict()  # 1 - processed, 0 - not


def start_camera_simualtion(path_to_media_mtx, path_to_streaming_file):
    os.system(f"start {path_to_media_mtx}")
    sleep(1)
    os.system(f"start ffmpeg "
              f"-re -stream_loop "
              f"-1 -i {path_to_streaming_file} -c copy "
              f"-f rtsp -rtsp_transport tcp "
              f"rtsp://localhost:8554/mystream"
              )


def get_license_plate_text(path_to_license_plate, json_with_plate_text):
    os.system(f"curl "
              f"-X POST http://127.0.0.1:5000/ScreenTranslatorAPI/detect "
              f"-H accept: application/json "
              f"-H Content-Type: multipart/form-data "
              f"-F file=@{path_to_license_plate};type=image/jpeg"
              f"-o {os.path.splitext(os.path.basename(path_to_license_plate))[0]}"
              f"{json_with_plate_text}.json"
              )

def post_to_result_server(path_to_image):



def camera_handling(camera_url):
    cap = cv2.VideoCapture(camera_url)

    width_org = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height_org = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    print(f'Width: {width_org} | Height: {height_org} | FPS: {fps}')

    while True:
        ret, camera_frame = cap.read()  # blocking operation
        # img = cv2.resize(img, (1280, 720))

        current_time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        os_random_int = uuid.uuid4()
        camera_name = (camera_url.split("/"))[-1]
        img_name = f"{PATH_TO_ORIGINS}/{camera_name}__{current_time}__{os_random_int}.jpg"
        img_names[img_name] = 0

        cv2.imwrite(img_name, camera_frame)
        crop_folder_name = f"{camera_name}__{current_time}__{os_random_int}"

        detect.run(source=img_name,
                   weights=PATH_TO_WEIGHTS,
                   project=PATH_TO_CROPS,
                   save_crop=True,
                   name=crop_folder_name
                   )
        img_names[img_name] = 1
        cv2.imshow("RTSP camera", camera_frame)
        cv2.waitKey(1)

        plates_folder = f"{PATH_TO_CROPS}/{crop_folder_name}/license plate"
        plates_images = [f for f in os.listdir(plates_folder) if os.path.isfile(os.path.join(plates_folder, f))]

        for plate_image in plates_images:
            img_name, img_extension = os.path.splitext(plate_image)
            json_with_plate_text = f"{img_name}.json"
            get_plate_routine = multiprocessing.Process(target=get_license_plate_text,
                                                        args=(plate_image, json_with_plate_text,))
            get_plate_routine.start()
            get_plate_routine.join()


if __name__ == "__main__":
    start_camera_simualtion(PATH_TO_MEDIAMTX, PATH_TO_STREAMING_FILE)
    sleep(1)
    camera_handling(CAMERA_URL)
