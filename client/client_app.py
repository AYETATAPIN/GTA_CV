from flask import Flask, render_template, request
import requests

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


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
