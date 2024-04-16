import sqlite3

DB_NAME = "sqlite_db.db"
column = ["Фамилия_Имя_Отчество",
          "ПТС_или_Стоянка",
          "Собственник_авто",
          "Наличие_доверенности",
          "Присутствие_собственника_на_сделке",
          "Желаемая_сумма_займа",
          "Обратный_звонок",
          "ПТС_или_СТС_1",
          "ПТС_или_СТС_2",
          "Паспорт_1",
          "Паспорт_регистрация",
          "Доверенность_1",
          "Доверенность_2"]


class sql_db():
    def sql_conn(self):
        with sqlite3.connect(DB_NAME):
            print("Успешное подключение к БД.")

    # Создание таблицы
    def sql_create_table(self):
        with sqlite3.connect(DB_NAME) as sqlite_conn:
            sql_req = """CREATE TABLE "Клиенты" (
            "Id" INTEGER,
            "Id_клиента"	INTEGER,
            "Фамилия, Имя, Отчество"	TEXT,
            "ПТС или Стоянка"	TEXT,
            "Собственник авто"	TEXT,
            "Наличие доверенности"	TEXT,
            "Присутствие собственника на сделке"	TEXT,
            "Желаемая сумма займа"	TEXT,
            "Номер телефона"	TEXT,
            PRIMARY KEY("Id" AUTOINCREMENT)
            );"""
            sqlite_conn.execute(sql_req)
        return print("Таблица успешно создана.")

    # Удаление таблицы
    def sql_del_table(self, name):
        with sqlite3.connect(DB_NAME) as sqlite_conn:
            sql_req = "DROP TABLE {};".format(name)
            sqlite_conn.execute(sql_req)
        return print("Таблица {} успешно удалена.".format(name))

    # Добавление в таблицу данных
    def sql_ins_data(self, table, column, data):
        with sqlite3.connect(DB_NAME) as sqlite_conn:
            sql_req = "INSERT INTO {} ({}) VALUES ('{}');".format(table,
                                                                  column, data)
            sqlite_conn.execute(sql_req)
        return print("Запись успешно добавлена в таблицу {}.".format(table))

    # Узнать текущий ID для добавления дальнейших данных в строку
    def sql_id():
        with sqlite3.connect(DB_NAME) as sqlite_conn:
            sql_req = "SELECT * FROM Client ORDER BY id DESC LIMIT 1;"
            sql_cursor = sqlite_conn.execute(sql_req)
            result = sql_cursor.fetchall()
            id = result[0][0]
            return id

    # Добавление в таблицу данных (ДОПОЛНЕНИЕ в определенный ID)
    def sql_ins_new(column, data, id):
        # Добавление
        with sqlite3.connect(DB_NAME) as sqlite_conn:
            sql_req = """
            UPDATE Клиенты set {} = '{}' where Id_клиента = {};""".format(
                                                                      column,
                                                                      data,
                                                                      id)
            sqlite_conn.execute(sql_req)
        return print("Запись успешно добавлена в таблицу Клиенты.")

    # Создание новой строки
    def sql_ins_line(column, data):
        with sqlite3.connect(DB_NAME) as sqlite_conn:
            sql_req = "INSERT INTO Клиенты ({}) VALUES ('{}');".format(column,
                                                                       data)
            sqlite_conn.execute(sql_req)
        return print("Запись успешно добавлена в таблицу Клиенты.")

    # Проверка ID пользователя в БД
    def sql_id_client(data):
        with sqlite3.connect(DB_NAME) as sqlite_conn:
            sql_req = """
            SELECT Id_клиента FROM Клиенты WHERE Id_клиента = {};
            """.format(data)
            sql_cursor = sqlite_conn.execute(sql_req)
            result = sql_cursor.fetchall()
        return result

    # Для сообщения менеджеру (получение значения из определенного столбца)
    def select_data(column, id):
        with sqlite3.connect(DB_NAME) as sqlite_conn:
            sql_req = "SELECT {} FROM Клиенты WHERE \
                Id_клиента = {};".format(column, id)
            sql_cursor = sqlite_conn.execute(sql_req)
            result = sql_cursor.fetchall()
            full_result = result[0][0]
        return full_result

    # Очистка строки БД клиента (кроме телефона и ID)
    def cleaning_bd(id):
        with sqlite3.connect(DB_NAME) as sqlite_conn:
            for i in column:
                sql_req = "UPDATE Клиенты set {} = '-' \
                    where Id_клиента = {};".format(i, id)
                sqlite_conn.execute(sql_req)
        return print("Строка пользователя {} успешно очищена.".format(id))
