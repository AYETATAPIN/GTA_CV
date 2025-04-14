import os
import cv2
import detect
import hashlib
import datetime
import requests
import subprocess

PATH_TO_MEDIAMTX = "D:/prg/pycharm/projects/zmeyuka/mediamtx/mediamtx.exe"
PATH_TO_STREAMING_FILE = "D:/prg/pycharm/projects/zmeyuka/yolov5/ts_streams/cars_test.ts"
PATH_TO_WEIGHTS = "D:/prg/pycharm/projects/zmeyuka/yolov5/saved_models/processor_died1337/best.pt"
PATH_TO_ORIGINS = "D:/prg/zalupen/origins"
PATH_TO_CROPS = "D:/prg/zalupen/crops"
CAMERA_URL = 'rtsp://localhost:8554/mystream'
#ffmpeg -re -stream_loop -1 -i cars_test.ts -c copy -f rtsp -rtsp_transport tcp rtsp://localhost:8554/mystream

img_names = dict() # 1 - processed, 0 - not

def run_command(cmd):
    result = subprocess.run(cmd)
    return result.stdout + result.stderr
    # os.system(cmd)
    #subprocess.Popen(["cat"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

def start_rtsp_port_simulation(path_to_mediamtx):
    cmd = f"{path_to_mediamtx}"
    result_output = run_command(cmd)
    print(f"RTSP port start result: {result_output}")

def start_camera_simulation(streaming_file):
    cmd = f"ffmpeg -re -stream_loop -1 -i {streaming_file} -c copy -f rtsp -rtsp_transport tcp rtsp://localhost:8554/mystream"
    result_output = run_command(cmd)
    print(f"Camera simulation start result: {result_output}")

def camera_handling(camera_url):
    cap = cv2.VideoCapture(camera_url)

    width_org = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height_org = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    print(f'Width: {width_org} | Height: {height_org} | FPS: {fps}')

    while True:
        ret, camera_frame = cap.read()
        # img = cv2.resize(img, (1280, 720))
        current_time = str(datetime.datetime.now()).replace("-", "_").replace(" ", "_").replace(":", "_").replace(".",
                                                                                                                  "_")
        os_random = hashlib.sha256(str(os.urandom(32)).encode())
        os_random_int = str(int.from_bytes(os_random.digest(), byteorder="big"))[:20]
        camera_name = (camera_url.split("/"))[-1]
        img_name = f"{PATH_TO_ORIGINS}/{camera_name}__{current_time}__{os_random_int}.jpg"
        img_names[img_name] = 0
        cv2.imwrite(img_name, camera_frame)
        crop_folder_name = f"{camera_name}__{current_time}__{os_random_int}"
        detect.run(source=img_name, weights=PATH_TO_WEIGHTS, project=PATH_TO_CROPS, save_crop=True,
                   name=crop_folder_name)
        img_names[img_name] = 1
        cv2.imshow("RTSP camera", camera_frame)
        cv2.waitKey(1)

        frame_with_detection_name = f"{PATH_TO_CROPS}"

if __name__ == "__main__":
    start_rtsp_port_simulation(PATH_TO_MEDIAMTX)
    start_camera_simulation(PATH_TO_STREAMING_FILE)
    camera_handling(CAMERA_URL)
