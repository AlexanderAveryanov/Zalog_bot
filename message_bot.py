# Сообщение Менеджеру
import sqlite


class message_kris():
    # Сообщение "Нужен звонок специалиста"
    def message_phone(id):
        sql = sqlite.sql_db
        full_name = sql.select_data("Фамилия_Имя_Отчество", id)
        phone = sql.select_data("Номер_телефона", id)
        PTS_and_Parking = sql.select_data("ПТС_или_Стоянка", id)
        car_owner = sql.select_data("Собственник_авто", id)
        power_of_attorney = sql.select_data("Наличие_доверенности", id)
        deal_owner = sql.select_data("Присутствие_собственника_на_сделке", id)
        text = f"ФИО: {full_name}\n" \
            f"Номер телефона: {phone}\n" \
            f"Тип залога: {PTS_and_Parking}\n" \
            f"Собственник авто: {car_owner}\n" \
            f"Доверенность: {power_of_attorney}\n" \
            f"Присутствие собственника на сделке: {deal_owner}\n" \
            "ОБРАТНЫЙ ЗВОНОК!"
        return text

    # Стандартное сообщение
    def message_data(id):
        sql = sqlite.sql_db
        full_name = sql.select_data("Фамилия_Имя_Отчество", id)
        phone = sql.select_data("Номер_телефона", id)
        PTS_and_Parking = sql.select_data("ПТС_или_Стоянка", id)
        car_owner = sql.select_data("Собственник_авто", id)
        power_of_attorney = sql.select_data("Наличие_доверенности", id)
        deal_owner = sql.select_data("Присутствие_собственника_на_сделке", id)
        money = sql.select_data("Желаемая_сумма_займа", id)
        text = f"ФИО: {full_name}\n" \
            f"Номер телефона: {phone}\n" \
            f"Тип залога: {PTS_and_Parking}\n" \
            f"Собственник авто: {car_owner}\n" \
            f"Доверенность: {power_of_attorney}\n" \
            f"Присутствие собственника на сделке: {deal_owner}\n" \
            f"Желаемая сумма займа: {money}"
        return text

    # Стандартное сообщение
    def message_photo(id):
        sql = sqlite.sql_db
        pts_sts_1 = sql.select_data("ПТС_или_СТС_1", id)
        pts_sts_2 = sql.select_data("ПТС_или_СТС_2", id)
        passport_1 = sql.select_data("Паспорт_1", id)
        passport_2 = sql.select_data("Паспорт_регистрация", id)
        dover_1 = sql.select_data("Доверенность_1", id)
        dover_2 = sql.select_data("Доверенность_2", id)
        file_id = [pts_sts_1, pts_sts_2, passport_1,
                   passport_2, dover_1, dover_2]
        return file_id
