import DB_managing as db
import pytest
import sqlite3


def clear_table():
    db.db_name = "test.db"
    connection = sqlite3.connect(db.db_name)
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS Cars")
    cursor.execute("DROP TABLE IF EXISTS Photos")
    connection.commit()
    connection.close()


def table_exists(table_name):
    connection = sqlite3.connect(db.db_name)
    cursor = connection.cursor()
    try:
        cursor.execute(f"SELECT 1 FROM {table_name} LIMIT 1")
        connection.close()
        return True
    except sqlite3.OperationalError:
        connection.close()
        return False


def test_start():  # Успешно ли создается таблица
    clear_table()
    assert not table_exists('Cars')
    assert not table_exists('Photos')
    db.start_validation()
    assert table_exists('Cars')
    assert table_exists('Photos')
    db.start_validation()  # Не крашится ли после второго использования
    assert table_exists('Cars')
    assert table_exists('Photos')


def test_save_car_1():  # Корректно ли добавляется запись и не меняется ли при втором использовании
    clear_table()
    db.start_validation()
    db.save_car_to_db("123", "camry", "pepe")
    connect = sqlite3.connect(db.db_name)
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM Cars WHERE license_plate = 123")
    l = cursor.fetchall()
    assert len(l) == 1
    assert l[0][0] == '123'
    assert l[0][1] == 'camry'
    assert l[0][2] == 'pepe'
    db.save_car_to_db("123", "camry", "pepe")
    cursor.execute("SELECT * FROM Cars WHERE license_plate = 123")
    l = cursor.fetchall()
    assert len(l) == 1
    assert l[0][0] == '123'
    assert l[0][1] == 'camry'
    assert l[0][2] == 'pepe'
    connect.close()


def test_save_car_2():  # Не ломается ли при отсутствии model и успешно ли перезаписывается
    clear_table()
    db.start_validation()
    db.save_car_to_db("123", owner='pepe')
    connect = sqlite3.connect(db.db_name)
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM Cars WHERE license_plate = 123")
    l = cursor.fetchall()
    assert len(l) == 1
    assert l[0][0] == '123'
    assert l[0][1] == None
    assert l[0][2] == 'pepe'
    db.save_car_to_db("123", "camry", "pepe")
    cursor.execute("SELECT * FROM Cars WHERE license_plate = 123")
    l = cursor.fetchall()
    assert len(l) == 1
    assert l[0][0] == '123'
    assert l[0][1] == 'camry'
    assert l[0][2] == 'pepe'
    connect.close()


def test_save_car_3():  # Не ломается ли при отсутствии owner и успешно ли перезаписывается
    clear_table()
    db.start_validation()
    db.save_car_to_db("123", model='camry')
    connect = sqlite3.connect(db.db_name)
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM Cars WHERE license_plate = 123")
    l = cursor.fetchall()
    assert len(l) == 1
    assert l[0][0] == '123'
    assert l[0][1] == 'camry'
    assert l[0][2] == None
    db.save_car_to_db("123", "camry", "pepe")
    cursor.execute("SELECT * FROM Cars WHERE license_plate = 123")
    l = cursor.fetchall()
    assert len(l) == 1
    assert l[0][0] == '123'
    assert l[0][1] == 'camry'
    assert l[0][2] == 'pepe'
    connect.close()


def test_save_car_4():  # Не ломается ли при отсутствии всех необязательных полей и успешно ли перезаписывается
    clear_table()
    db.start_validation()
    db.save_car_to_db("123")
    connect = sqlite3.connect(db.db_name)
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM Cars WHERE license_plate = 123")
    l = cursor.fetchall()
    assert len(l) == 1
    assert l[0][0] == '123'
    assert l[0][1] == None
    assert l[0][2] == None
    db.save_car_to_db("123", "camry", "pepe")
    cursor.execute("SELECT * FROM Cars WHERE license_plate = 123")
    l = cursor.fetchall()
    assert len(l) == 1
    assert l[0][0] == '123'
    assert l[0][1] == 'camry'
    assert l[0][2] == 'pepe'
    connect.close()


def test_save_photo_1():  # корректность добавления фотки
    clear_table()
    db.start_validation()
    db.save_photo_to_db("just_folder/pupupu.bin", "123", "1871.1.17 12:0:0")
    connect = sqlite3.connect(db.db_name)
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM Photos WHERE license_plate = 123")
    l = cursor.fetchall()
    assert len(l) == 1
    assert l[0][3] == 'just_folder/pupupu.bin'
    assert l[0][1] == '123'
    assert l[0][2] == "1871.1.17 12:0:0"
    cursor.execute("SELECT * FROM Photos")
    l = cursor.fetchall()
    assert len(l) == 1
    connect.close()


def test_save_photo_2():  # корректность добавления нескольких фоток с разными номерами
    clear_table()
    db.start_validation()
    db.save_photo_to_db("just_folder/pupupu.bin", "123", "1871.1.17 12:0:0")
    db.save_photo_to_db("just_folder/asd.bin", "234", "1871.1.17 12:12:0")
    connect = sqlite3.connect(db.db_name)
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM Photos WHERE license_plate = 123")
    l = cursor.fetchall()
    assert len(l) == 1
    assert l[0][3] == 'just_folder/pupupu.bin'
    assert l[0][1] == '123'
    assert l[0][2] == "1871.1.17 12:0:0"
    cursor.execute("SELECT * FROM Photos WHERE license_plate = 234")
    l = cursor.fetchall()
    assert len(l) == 1
    assert l[0][3] == 'just_folder/asd.bin'
    assert l[0][1] == '234'
    assert l[0][2] == "1871.1.17 12:12:0"
    cursor.execute("SELECT * FROM Photos")
    l = cursor.fetchall()
    assert len(l) == 2
    connect.close()


def test_save_photo_2():  # корректность добавления нескольких фоток с одинаковым номерами
    clear_table()
    db.start_validation()
    db.save_photo_to_db("just_folder/pupupu.bin", "123", "1871.1.17 12:0:0")
    db.save_photo_to_db("just_folder/asd.bin", "123", "1871.1.17 12:12:0")
    connect = sqlite3.connect(db.db_name)
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM Photos WHERE license_plate = 123")
    l = cursor.fetchall()
    assert len(l) == 2
    assert l[0][3] == 'just_folder/pupupu.bin'
    assert l[0][1] == '123'
    assert l[0][2] == "1871.1.17 12:0:0"
    assert len(l) == 2
    assert l[1][3] == 'just_folder/asd.bin'
    assert l[1][1] == '123'
    assert l[1][2] == "1871.1.17 12:12:0"
    cursor.execute("SELECT * FROM Photos")
    l = cursor.fetchall()
    assert len(l) == 2
    connect.close()


def test_get_images_paths_1():  # проверка при пустой таблице
    clear_table()
    db.start_validation()
    l = db.get_images_paths_from_db("123")
    assert len(l) == 0


def test_get_images_paths_2():  # проверка при отстутствии искомого
    clear_table()
    db.start_validation()
    db.save_photo_to_db("just_folder/pupupu.bin", "123", "1871.1.17 12:0:0")
    db.save_photo_to_db("just_folder/asd.bin", "123", "1871.1.17 12:12:0")
    l = db.get_images_paths_from_db("1234")
    assert len(l) == 0


def test_get_images_paths_3():  # проверка при таблице из одного искомого
    clear_table()
    db.start_validation()
    db.save_photo_to_db("just_folder/pupupu.bin", "123", "1871.1.17 12:0:0")
    l = db.get_images_paths_from_db("123")
    assert len(l) == 1
    assert l[0] == 'just_folder/pupupu.bin'


def test_get_images_paths_4():  # проверка при непустой таблице, где есть одно искомое
    clear_table()
    db.start_validation()
    db.save_photo_to_db("just_folder/pupupu.bin", "123", "1871.1.17 12:0:0")
    db.save_photo_to_db("just_folder/asd.bin", "234", "1871.1.17 12:12:0")
    db.save_photo_to_db("just_folder/amogus.bin", "567", "2025.1.17 12:12:0")
    l = db.get_images_paths_from_db("123")
    assert len(l) == 1
    assert l[0] == 'just_folder/pupupu.bin'


def test_get_images_paths_4():  # проверка при пустой таблице, где есть много искомых
    clear_table()
    db.start_validation()
    db.save_photo_to_db("just_folder/pupupu.bin", "123", "1871.1.17 12:0:0")
    db.save_photo_to_db("just_folder/asd.bin", "123", "1871.1.17 12:12:0")
    l = db.get_images_paths_from_db("123")
    assert len(l) == 2
    assert l[0] == 'just_folder/pupupu.bin'
    assert l[1] == 'just_folder/asd.bin'


def test_get_images_paths_4():  # проверка при непустой таблице, где есть много искомых
    clear_table()
    db.start_validation()
    db.save_photo_to_db("just_folder/pupupu.bin", "123", "1871.1.17 12:0:0")
    db.save_photo_to_db("just_folder/asd.bin", "123", "1871.1.17 12:12:0")
    db.save_photo_to_db("just_folder/amogus.bin", "567", "2025.1.17 12:12:0")
    db.save_photo_to_db("just_folder/pepegus.bin", "1", "2025.1.17 12:12:12")
    l = db.get_images_paths_from_db("123")
    assert len(l) == 2
    assert l[0] == 'just_folder/pupupu.bin'
    assert l[1] == 'just_folder/asd.bin'
