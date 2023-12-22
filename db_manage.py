import sqlite3
from _datetime import datetime


def creation():
    connection = sqlite3.connect('storage.db')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE "Storage" (
    "id"	INTEGER,
    "slot"	TEXT UNIQUE,
    "place"	TEXT UNIQUE,
    "place2"	TEXT UNIQUE,
    PRIMARY KEY("id")
    );''')

    # Сохраняем изменения и закрываем соединение
    connection.commit()
    connection.close()


def update(slot, number):
    connection = sqlite3.connect('storage.db')
    cursor = connection.cursor()

    cursor.execute('UPDATE Storage SET place = ? WHERE slot = ?', (number, slot))

    # Сохраняем изменения и закрываем соединение
    with open("log.txt", "a") as file:
        file.write(f'{datetime.now().strftime("%d-%m-%Y %H:%M")}  комплект  {number}  перенесен на место  {slot}\n')
    connection.commit()
    connection.close()


def db_delete(number):
    connection = sqlite3.connect('storage.db')
    cursor = connection.cursor()

    slot = db_search(number)

    cursor.execute('UPDATE Storage SET place = NULL WHERE slot = ?', (slot,))
    cursor.execute('UPDATE Storage SET place2 = NULL WHERE slot = ?', (slot,))

    with open("log.txt", "a") as file:
        file.write(f'{datetime.now().strftime("%d-%m-%Y %H:%M")}  комплект  {number}  удален с места  {slot}\n')
    # Сохраняем изменения и закрываем соединение

    connection.commit()
    connection.close()


def new_place(slot, number):
    connection = sqlite3.connect('storage.db')
    cursor = connection.cursor()

    cursor.execute("SELECT place FROM Storage WHERE slot = ?", (slot,))
    perviy_slot = cursor.fetchall()
    cursor.execute("SELECT place2 FROM Storage WHERE slot = ?", (slot,))
    vtoroy_slot = cursor.fetchall()

    if perviy_slot[0][0] is None:
        cursor.execute('UPDATE Storage SET place = ? WHERE slot = ?', (number, slot))
    elif vtoroy_slot[0][0] is not None:
        return False
    else:
        cursor.execute('UPDATE Storage SET place2 = ? WHERE slot = ?', (number, slot))

    with open("log.txt", "a") as file:
        file.write(f'{datetime.now().strftime("%d-%m-%Y %H:%M")}  комплект  {number}  добавлен на место  {slot}\n')
    # Сохраняем изменения и закрываем соединение
    connection.commit()
    connection.close()
    return True


def db_search(number):
    connection = sqlite3.connect('storage.db')
    cursor = connection.cursor()

    cursor.execute('SELECT slot FROM Storage WHERE place = ?', (number,))
    result = cursor.fetchall()
    cursor.execute('SELECT slot FROM Storage WHERE place2 = ?', (number,))
    result2 = cursor.fetchall()

    # Сохраняем изменения и закрываем соединение
    connection.commit()
    connection.close()

    if result != []:
        return result[0]
    elif result2 != []:
        return result2[0]
    else:
        return "None"


def get_all():
    connection = sqlite3.connect('storage.db')
    cursor = connection.cursor()

    cursor.execute("SELECT slot, place, place2 FROM Storage")
    places = cursor.fetchall()

    connection.commit()
    connection.close()
    return places


def db_new_row(place):
    connection = sqlite3.connect('storage.db')
    cursor = connection.cursor()

    cursor.execute("INSERT INTO Storage (slot, place, place2) VALUES (?, Null, Null);", (place,))

    connection.commit()
    connection.close()


def filling():
    for i in range(1, 9):
        for j in range(0, 41):
            f = i*100+j
            db_new_row(f)
