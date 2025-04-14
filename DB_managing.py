import sqlite3
db_name = "cars_v1.db"

def start_validation():
    # Удостоверились, что с базой всё в порядке
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Cars (
    license_plate TEXT NOT NULL,
    model TEXT,
    owner TEXT,
    PRIMARY KEY (license_plate)
    )''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Photoes (
    id INTEGER PRIMARY KEY,
    license_plate TEXT NOT NULL,
    date_time TEXT NOT NULL,
    image_path TEXT NOT NULL
    )''')
    #
    # date_time хранится в формате Year.Month.Date Hour:Min:Sec
    connection.commit()
    connection.close()


def save_photo_to_db(image_path, license_plate, date_time):  # str, str, str
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute('INSERT INTO Photoes (image_path, license_plate, date_time) VALUES (?, ?, ?)',
                   (image_path, license_plate, date_time))
    connection.commit()
    connection.close()

def save_car_to_db(license_plate, model=None, owner=None):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    ans = cursor.execute("SELECT 1 FROM Cars WHERE license_plate = ?",(license_plate,))
    if(len(ans.fetchall()) > 0):
        cursor.execute('UPDATE Cars SET model = ?, owner = ? WHERE license_plate = ?',
                       (model, owner, license_plate))
    else:
        cursor.execute('INSERT INTO Cars (license_plate, model, owner) VALUES (?, ?, ?)',
                       (license_plate, model, owner))
    connection.commit()
    connection.close()

def get_images_paths_from_db(license_plate):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute('SELECT image_path FROM Photoes WHERE license_plate = ?', (license_plate,))
    paths = cursor.fetchall()
    connection.close()
    result = tuple(element[0] for element in paths)
    return result

