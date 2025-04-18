import cv2 as cv
import numpy as np
import base64
import datetime
import os
from flask import Flask, request, jsonify
import DB_managing as db
app = Flask(__name__)
images_folder = "D:/prg/pycharm/projects/zmeyuka/yolov5/coded_images"


def save_photo(image, license_plate, date_time):
    coded_image = vae_coding(image)
    image_path = os.path.join(images_folder, license_plate + date_time + '.bin')
    # mkdir(images_folder) exists=ok
    with open(image_path, 'wb') as file:
        file.write(coded_image)

    db.save_photo_to_db(image_path, license_plate, date_time)


# 2 заглушки пока нет реального vae
def vae_coding(image):
    _, coded_image = cv.imencode(".jpg", image)
    return coded_image


def vae_decoding(coded_image):
    decoded_image = cv.imdecode(coded_image, cv.IMREAD_COLOR)
    return decoded_image




def get_images(license_plate):
    paths = db.get_images_paths_from_db(license_plate)
    images = []
    for path in paths:
        with open(path, 'rb') as file:
            coded_image = np.frombuffer(file.read(), np.uint8)
            decoded_image = vae_decoding(coded_image)
            images.append(decoded_image)
    return tuple(images)


def is_correct_datetime(date_time):
    try:
        datetime.datetime.strptime(date_time, "%Y_%m_%d_%H_%M_%S")
        return True
    except ValueError:
        return False


@app.route('/')
def greeting():
    return '''Используйте /save с методом POST, чтобы сохранить изображение.
  Понадобится передать изображение, номер и дату+время.
  Используйте /<license_plate> GET, чтобы получить изображения по указанному номеру.'''


@app.route('/savephoto', methods=['POST'])
def save_photo_request():
    license_plate = request.form.get('license_plate')
    date_time = request.form.get('date_time')

    image_file = request.files['image']
    if (license_plate == ""
            or image_file.filename == "" or not is_correct_datetime(date_time)):
        return 'wrong request', 400

    image_array = np.frombuffer(image_file.read(), np.uint8)

    image = cv.imdecode(image_array, cv.IMREAD_COLOR)
    save_photo(image, license_plate, date_time)
    return "Success" + "| license-plate: " + license_plate + "| date-time: " + date_time


@app.route('/savecar', methods=['POST'])
def save_car_request():
    license_plate = request.form.get('license_plate')
    model = request.form.get('model')
    owner = request.form.get('owner')

    if license_plate == "":
        return 'wrong request', 400


    db.save_car_to_db(license_plate, model, owner)
    return "Success" + "| license-plate: " + license_plate


def send_images(images):
    result = []
    for image in images:
        res, coded_image = cv.imencode('.jpg', image)
        if not res:
            return 'cv.imencode error', 500
        result.append(base64.b64encode(coded_image).decode('utf-8'))
    return jsonify(result)


@app.route('/<license_plate>')
def get_by_license_plate_request(license_plate):
    images = get_images(license_plate)
    if len(images) == 0:
        return 'images not found', 404
    return send_images(images)


if __name__ == "__main__":
    db.start_validation()
    app.run(port=50505)
