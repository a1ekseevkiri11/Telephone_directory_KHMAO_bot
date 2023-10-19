import sqlite3
from sqlite3 import Error
from parsing import getArraySotrForDB

CREATE_SOTR_TABLE = """CREATE TABLE sotr (
    familia text,
    fio text,
    kab text,
    telefon text,
    email text,
    card text
)
"""

def createConnection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    
    return connection

def executeQuery(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


def updateDB(connection):
    arraySotrForDB = getArraySotrForDB()
    if len(arraySotrForDB) == 0:
        return
    executeQuery(connection, "DELETE FROM sotr")
    cursor = connection.cursor()
    try:
        cursor.executemany("INSERT INTO sotr VALUES(?, ?, ?, ?, ?, ?)", arraySotrForDB)
        connection.commit()
        print("Query executemany successfully")
    except Error as e:
        print(f"The error '{e}' occurred")



def searchInDB(connection, inputUser, filter):
    cursor = connection.cursor()
    result = None
    try:
        match filter:
            case "fio":
                cursor.execute("SELECT card FROM sotr WHERE fio = ?", (inputUser,))
            case "familia":
                cursor.execute("SELECT card FROM sotr WHERE familia = ?", (inputUser,))
            case "kab":
                cursor.execute("SELECT card FROM sotr WHERE kab = ?", (inputUser,))
            case "tel":
                cursor.execute("SELECT card FROM sotr WHERE telefon = ?", (inputUser,))
            case "email":
                cursor.execute("SELECT card FROM sotr WHERE email = ?", (inputUser,))
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")
    

# def searchFIOInDB(connection, inputUser):
#     cursor = connection.cursor()
#     result = None
#     try:
#         cursor.execute("SELECT card FROM sotr WHERE fio = ?", (inputUser,))
#         result = cursor.fetchall()
#         return result
#     except Error as e:
#         print(f"The error '{e}' occurred")
    


# def searchFamiliaInDB(connection, inputUser):
#     cursor = connection.cursor()
#     result = None
#     try:
#         cursor.execute("SELECT card FROM sotr WHERE familia = ?", (inputUser,))
#         result = cursor.fetchall()
#         return result
#     except Error as e:
#         print(f"The error '{e}' occurred")


# def searchKabInDB(connection, inputUser):
#     cursor = connection.cursor()
#     result = None
#     try:
#         cursor.execute("SELECT card FROM sotr WHERE kab = ?", (inputUser,))
#         result = cursor.fetchall()
#         return result
#     except Error as e:
#         print(f"The error '{e}' occurred")


# def searchTelefonInDB(connection, inputUser):
#     cursor = connection.cursor()
#     result = None
#     try:
#         cursor.execute("SELECT card FROM sotr WHERE telefon = ?", (inputUser,))
#         result = cursor.fetchall()
#         return result
#     except Error as e:
#         print(f"The error '{e}' occurred")


# def searchEmailInDB(connection, inputUser):
#     cursor = connection.cursor()
#     result = None
#     try:
#         cursor.execute("SELECT card FROM sotr WHERE email = ?", (inputUser,))
#         result = cursor.fetchall()
#         return result
#     except Error as e:
#         print(f"The error '{e}' occurred")




if __name__ == "__main__":
    connection = createConnection('data base.db')
    #updateDB(connection)

    # while True:
    #     command = int(input("Введите номер команды: "))
    #     if command == 1:
    #         inputUser = str(input("Введите ФИО:"))
    #         answer = searchFIOInDB(connection, inputUser)
    #         if len(answer) == 0:
    #             print("Ничего не найдено!")
    #         for a in answer:
    #             print(a)
    #     elif command == 2:
    #         inputUser = str(input("Введите фамилию:"))
    #         answer = searchFamiliaInDB(connection, inputUser)
    #         if len(answer) == 0:
    #             print("Ничего не найдено!")
    #         for a in answer:
    #             print(a)
    #     else:
    #         break