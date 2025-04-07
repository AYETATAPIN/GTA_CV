import sqlite3
import cv2 as cv
import numpy as np
import base64
import datetime
import os
from flask import Flask, request, jsonify, abort

app = Flask(__name__)
images_folder = 'coded_images'


def save_image(image, license_plate, date_time):
    coded_image = vae_coding(image)
    image_path = os.path.join(images_folder, license_plate + date_time + '.bin')

    with open(image_path, 'wb') as file:
        file.write(coded_image)

    save_to_db(image_path, license_plate, date_time)


# 2 заглушки пока нет реального vae
def vae_coding(image):
    _, coded_image = cv.imencode(".jpg", image)
    return coded_image


def vae_decoding(coded_image):
    decoded_image = cv.imdecode(coded_image, cv.IMREAD_COLOR)
    return decoded_image


def save_to_db(image_path, license_plate, date_time):  # str, str, str
    connection = sqlite3.connect('cars_v0.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO Cars (image_path, license_plate, date_time) VALUES (?, ?, ?)',
                   (image_path, license_plate, date_time))
    connection.commit()
    connection.close()


def get_images_paths_from_db(license_plate):
    connection = sqlite3.connect('cars_v0.db')
    cursor = connection.cursor()
    cursor.execute('SELECT image_path FROM Cars WHERE license_plate = ?', (license_plate,))
    paths = cursor.fetchall()
    connection.close()
    result = tuple(element[0] for element in paths)
    return result


def get_images(license_plate):
    paths = get_images_paths_from_db(license_plate)
    if len(paths) == 0:
        abort(404)
    images = []
    for path in paths:
        with open(path, 'rb') as file:
            coded_image = np.frombuffer(file.read(), np.uint8)
            decoded_image = vae_decoding(coded_image)
            images.append(decoded_image)
    return tuple(images)


def is_correct_datetime(date_time):
    try:
        datetime.datetime.strptime(date_time, "%Y.%m.%d %H:%M:%S")
        return True
    except ValueError:
        return False


@app.route('/')
def greeting():
    return '''Используйте /save с методом POST, чтобы сохранить изображение.
  Понадобится передать изображение, номер и дату+время.
  Используйте /<license_plate> GET, чтобы получить изображения по указанному номеру.'''


@app.route('/save', methods=['POST'])
def save_request():
    license_plate = request.form.get('license_plate')
    date_time = request.form.get('date_time')

    image_file = request.files['image']
    if (license_plate == ""
            or image_file.filename == "" or not is_correct_datetime(date_time)):
        abort(400)

    image_array = np.frombuffer(image_file.read(), np.uint8)

    image = cv.imdecode(image_array, cv.IMREAD_COLOR)
    save_image(image, license_plate, date_time)
    return "Success" + "| license-plate: " + license_plate + "| date-time: " + date_time


def send_images(images):
    result = []
    for image in images:
        res, coded_image = cv.imencode('.jpg', image)
        if not res:
            abort(500)
        result.append(base64.b64encode(coded_image).decode('utf-8'))
    return jsonify(result)


@app.route('/<license_plate>')
def get_by_license_plate_request(license_plate):
    images = get_images(license_plate)
    return send_images(images)


if __name__ == "__main__":
    # Удостоверились, что с базой всё в порядке
    connection = sqlite3.connect('cars_v0.db')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Cars (
    id INTEGER PRIMARY KEY,
    image_path TEXT NOT NULL,
    license_plate TEXT NOT NULL,
    date_time TEXT NOT NULL 
    )''')
    #
    # date_time хранится в формате Year.Month.Date Hour:Min:Sec
    connection.commit()
    connection.close()

    app.run(port=50505)
