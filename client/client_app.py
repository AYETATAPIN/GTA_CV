from flask import Flask, render_template, request
import requests
from io import BytesIO

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/save', methods=['POST'])
def handle_save():
    license_plate = request.form.get('license_plate')
    date_time = request.form.get('date_time')
    image = request.files['image']

    if not license_plate or not date_time or not image:
        return "Все поля обязательны для заполнения", 400

    try:
        image_data = image.read()
        files = {'image': (image.filename, BytesIO(image_data), image.content_type)}
        data = {'license_plate': license_plate, 'date_time': date_time}

        response = requests.post(
            'http://localhost:50505/save',
            data=data,
            files=files
        )
        response.raise_for_status()
        return response.text
    except Exception as e:
        return f"Ошибка: {str(e)}", 500


@app.route('/display')
def display():
    license_plate = request.args.get('license_plate')
    if not license_plate:
        return "Введите номер автомобиля", 400

    try:
        response = requests.get(f'http://localhost:50505/{license_plate}')
        if response.status_code == 200:
            return render_template('display.html',
                                   images=response.json(),
                                   license_plate=license_plate)
        return f"Ошибка сервера: {response.status_code}", response.status_code
    except Exception as e:
        return f"Ошибка подключения: {str(e)}", 500


if __name__ == '__main__':
    app.run(port=5000)
