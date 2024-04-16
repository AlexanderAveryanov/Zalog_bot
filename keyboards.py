from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


class keyboards():
    # Главное меню
    def get_client() -> ReplyKeyboardMarkup:
        kb = ReplyKeyboardBuilder()
        kb.button(text="Новый клиент")
        kb.button(text="Клиент компании")
        # Количество кнопок в строке
        kb.adjust(2)
        return kb.as_markup(resize_keyboard=True,
                            input_field_placeholder="Выберите"
                            + " вариант ответа")

    # Способ залога?
    def get_pts_parking() -> ReplyKeyboardMarkup:
        kb_1 = ReplyKeyboardBuilder()
        kb_1.button(text="Под ПТС")
        kb_1.button(text="Под стоянку")
        kb_1.button(text="В главное меню")
        kb_1.adjust(2)
        return kb_1.as_markup(resize_keyboard=True,
                              input_field_placeholder="Выберите способ залога")

    # Ветка "Клиент компании"
    def get_order() -> ReplyKeyboardMarkup:
        kb_2 = ReplyKeyboardBuilder()
        kb_2.button(text="Оплата по договору")
        kb_2.button(text="Памятка клиента")
        kb_2.button(text="В главное меню")
        kb_2.adjust(2)
        return kb_2.as_markup(resize_keyboard=True,
                              input_field_placeholder="Выберите"
                              + " вариант ответа")

    def get_yes_no() -> ReplyKeyboardMarkup:
        kb_3 = ReplyKeyboardBuilder()
        kb_3.button(text="Да")
        kb_3.button(text="Нет")
        kb_3.button(text="В главное меню")
        kb_3.adjust(2)
        return kb_3.as_markup(resize_keyboard=True,
                              input_field_placeholder="Выберите"
                              + " вариант ответа")

    def get_power_of_attorney() -> ReplyKeyboardMarkup:
        kb_4 = ReplyKeyboardBuilder()
        kb_4.button(text="Доверенность есть")
        kb_4.button(text="Доверенности нет")
        kb_4.button(text="В главное меню")
        kb_4.adjust(2)
        return kb_4.as_markup(resize_keyboard=True,
                              input_field_placeholder="Выберите"
                              + " вариант ответа")

    # Собственник на сделке
    def get_deal_owner() -> ReplyKeyboardMarkup:
        kb_5 = ReplyKeyboardBuilder()
        kb_5.button(text="Сможет")
        kb_5.button(text="Не сможет")
        kb_5.button(text="В главное меню")
        kb_5.adjust(2)
        return kb_5.as_markup(resize_keyboard=True,
                              input_field_placeholder="Выберите"
                              + " вариант ответа")

# Номер телефона
    def get_phone() -> ReplyKeyboardMarkup:
        kb_6 = ReplyKeyboardBuilder()
        kb_6.button(text="Отправить номер телефона",
                    request_contact=True)
        kb_6.button(text="В главное меню")
        kb_6.adjust(1)
        return kb_6.as_markup(resize_keyboard=True,
                              input_field_placeholder="Выберите"
                              + " вариант ответа")

    # Продолжить общение здесь? или консультация специалиста?
    def get_message() -> ReplyKeyboardMarkup:
        kb_7 = ReplyKeyboardBuilder()
        kb_7.button(text="Продолжить оформление здесь")
        kb_7.button(text="Консультация специалиста (звонок Вам)")
        kb_7.button(text="В главное меню")
        kb_7.adjust(1)
        return kb_7.as_markup(resize_keyboard=True,
                              input_field_placeholder="Выберите"
                              + " вариант ответа")

    # Возврат в главное меню
    def get_end() -> ReplyKeyboardMarkup:
        kb_8 = ReplyKeyboardBuilder()
        kb_8.button(text="В главное меню")
        kb_8.adjust(1)
        return kb_8.as_markup(resize_keyboard=True,
                              input_field_placeholder="Выберите"
                              + " вариант ответа")
