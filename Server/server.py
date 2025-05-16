from flask import Flask, render_template, request, jsonify, send_file, send_from_directory
import os
import shutil
import subprocess
from flasgger import Swagger, swag_from

app = Flask(__name__)
swagger = Swagger(app)

UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
PROCESSED_FOLDER = os.path.join(app.root_path, 'static', 'processed')
BOXED_FOLDER = os.path.join(PROCESSED_FOLDER, 'boxed')
TRANSLATED_FOLDER = os.path.join(PROCESSED_FOLDER, 'translated')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)
os.makedirs(BOXED_FOLDER, exist_ok=True)
os.makedirs(TRANSLATED_FOLDER, exist_ok=True)
CLEAN_UP_FILES = True


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ScreenTranslatorAPI/imageDetect', methods=['POST'])
@swag_from('apidocs/imageDetect.yml')
def imageDetect():
    if 'File' not in request.files or request.files['File'].filename == '':
        return jsonify({'Error': 'No file uploaded'}), 400

    file = request.files['File']
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    try:
        run_yolo(filepath)
        recognized_text = parse_yolo_labels(os.path.join(BOXED_FOLDER, 'labels', f"{file.filename.rsplit('.', 1)[0]}.txt"))
        return jsonify({"Detected text": recognized_text})

    except Exception as e:
        return jsonify({'Error': 'Processing failed', 'Error details': str(e)}), 500
    

def run_yolo(filepath):
    command = [
        "python", "D:/prg/pycharm/projects/zmeyuka/yolov5/Server/yolo/detect.py",
        "--weights", "D:/prg/pycharm/projects/zmeyuka/yolov5/Server/yolo/best.pt",
        "--source", filepath,
        "--line-thickness", "1",
        "--img", "1500",
        "--exist-ok",
        "--save-txt",
        "--save-conf",
        "--name", BOXED_FOLDER,
        "--project", "."
    ]
    subprocess.run(command, check=True)


def parse_yolo_labels(file_path, conf_thres=0.5):
    names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.', ',', '?', '!', '@']
    entries = []
    if os.path.isfile(file_path) == False:
        with open(file_path, "w") as file:
            file.write(f"{{\n\t\"Detected text\": \"Unable to identify\"\n}}")
            return "Unable to identify"
    else:
        with open(file_path, 'r') as file:
            for line in file:
                parts = line.strip().split()
                confidence = float(parts[5])
                if confidence >= conf_thres:
                    class_id = int(float(parts[0]))
                    x_center = float(parts[1])
                    entries.append((x_center, class_id))

        entries.sort(key=lambda x: x[0])
    return ''.join([names[class_id] for x_center, class_id in entries])


def clean_directory(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Не удалось удалить {file_path}. Причина: {e}')

def clean_up_on_start():
    if CLEAN_UP_FILES:
        for folder in [UPLOAD_FOLDER, BOXED_FOLDER, TRANSLATED_FOLDER]:
            clean_directory(folder)



if __name__ == "__main__":
    if CLEAN_UP_FILES:
        clean_up_on_start()
    app.run(host="0.0.0.0", port=5000, debug=True)
