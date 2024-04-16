from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from keyboards import keyboards
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import sqlite
import message_bot
from text_bot import good, back_to_top, good_1, question_1, question_2
from text_bot import question_3, question_full_name, customer_memo
from text_bot import question_4, question_5, question_phone_1, question_6
from text_bot import question_7, good_request, error, good_request_1
from text_bot import question_phone_2, doc, doc_sts_pts_1, doc_sts_pts_2
from text_bot import doc_pass_1, doc_pass_2, doc_power_of_attorney_1
from text_bot import doc_power_of_attorney_2

# роутер уровня модуля
router = Router()
CONSTANT_USER_ID = 1111111111  # ID call-центра (менеджера)
CONSTANT_MENEGER_ID = 1111111111  # ID Менеджера (сообщение о платеже)


class OrderFood(StatesGroup):
    choosing_client = State()  # Клиент компании или нет
    choosing_order_and_memo = State()  # Оплата по договору или Памятка клиента
    choosing_full_name_order = State()  # ФИО клиента
    choosing_order = State()  # Оплата по договору
    choosing_order_1 = State()
    choosing_order_2 = State()
    choosing_pledge_method = State()  # Выбор способа залога (статус)
    choosing_car_owner = State()  # Собственник авто? (статус)
    choosing_full_name = State()  # ФИО (статус)
    choosing_message = State()  # Консул. спец. или продолжить общение?
    choosing_power_of_attorney = State()  # Доверенность? (статус)
    choosing_phone = State()  # Номер телефона для связи специалиста (статус)
    choosing_summa = State()  # Желаемая сумма займа
    choosing_data_dover_1 = State()  # Фото Доверенности стр.1
    choosing_data_dover_2 = State()  # Фото Доверенности стр.2
    choosing_data_pts_sts_1 = State()  # Фото ПТС/СТС лицевая сторона
    choosing_data_pts_sts_2 = State()  # Фото ПТС/СТС оборотная сторона
    choosing_data_passport_1 = State()  # Фото паспорта стр. 1-2
    choosing_data_passport_2 = State()  # Фото паспорта регистрация
    choosing_phone_2 = State()  # Номер телефона для обычного случая
    choosing_attendance_at_the_deal = State()  # Собственник на сделке
    choosing_customer_memo = State()  # Памятка клиента


# Хэндлер на команду /start
@router.message(Command("start"))
# state: FSMContext - для статуса
async def cmd_start(message: Message, state: FSMContext):
    # await message.delete()  # Удаляет команду пользователя
    user_id = message.from_user.id
    # проверка, есть ли в БД такой id пользователя
    result_id = sqlite.sql_db.sql_id_client(user_id)
    if result_id == []:
        # запись в БД ID пользователя
        column = 'Id_клиента'  # В какой столбец таблицы БД добавлять
        sqlite.sql_db.sql_ins_line(column, int(user_id))
    # Узнаем имя пользователя
    user_fullname = message.from_user.full_name
    await message.answer(text=f"<b>{user_fullname}, "
                         + "компания ZALOG_TEST приветствует Вас!</b>",
                         reply_markup=keyboards.get_client())
    # Устанавливаем пользователю состояние "клиент компании или нет"
    await state.set_state(OrderFood.choosing_client)


# Клиент компании или нет
@router.message(OrderFood.choosing_client, F.text == "Клиент компании")
async def client(message: Message, state: FSMContext):
    await message.answer(text=question_1,
                         reply_markup=keyboards.get_order())
    await state.set_state(OrderFood.choosing_order_and_memo)


@router.message(OrderFood.choosing_client, F.text == "Новый клиент")
async def new_client(message: Message, state: FSMContext):
    await message.answer(text=question_2,
                         reply_markup=keyboards.get_pts_parking())
    await state.set_state(OrderFood.choosing_pledge_method)


# Этап выбора ПТС или СТОЯНКА
@router.message(OrderFood.choosing_pledge_method, F.text == "Под ПТС")
async def answer_yes(message: Message, state: FSMContext):
    await state.update_data(chosen_pledge_method=message.text)
    # запись результата выбора "под птс" в БД
    column = 'ПТС_или_Стоянка'
    data = message.text
    # Проверяем id пользователя с которым идет диалог,
    # т.к. возможно общение одновременно с несколькими пользователями
    # и необходимо понять, кому именно записать выбранное значение
    id = message.from_user.id
    sqlite.sql_db.sql_ins_new(column, data, int(id))
    await message.answer(text=good_1)
    await message.answer(text=question_3,
                         reply_markup=keyboards.get_yes_no())
    # Переход к следующему статусу (Собственник авто?)
    await state.set_state(OrderFood.choosing_car_owner)


@router.message(OrderFood.choosing_pledge_method, F.text == "Под стоянку")
async def filter_parking(message: Message, state: FSMContext):
    await state.update_data(chosen_pledge_method=message.text)
    # запись результата выбора выбора "под стоянку" в БД
    column = 'ПТС_или_Стоянка'
    data = message.text
    id = message.from_user.id
    sqlite.sql_db.sql_ins_new(column, data, int(id))
    await message.answer(text=good_1)
    await message.answer(text=question_3,
                         reply_markup=keyboards.get_yes_no())
    await state.set_state(OrderFood.choosing_car_owner)


# Второй уровень
@router.message(OrderFood.choosing_car_owner, F.text == "Да")
async def filter_yes(message: Message, state: FSMContext):
    await state.update_data(chosen_car_owner=message.text)
    # Собственник авто - запись результата выбора "да" в БД
    column = 'Собственник_авто'
    data = message.text
    id = message.from_user.id
    sqlite.sql_db.sql_ins_new(column, data, int(id))
    await message.answer(text=good)
    await message.answer(text=question_full_name,
                         reply_markup=ReplyKeyboardRemove())
    await state.set_state(OrderFood.choosing_full_name)


@router.message(OrderFood.choosing_car_owner, F.text == "Нет")
async def filter_no(message: Message, state: FSMContext):
    await state.update_data(chosen_car_owner=message.text)
    # Собственник авто - запись результата выбора "нет" в БД
    column = 'Собственник_авто'
    data = message.text
    id = message.from_user.id
    sqlite.sql_db.sql_ins_new(column, data, int(id))
    await message.answer(text=good)
    await message.answer(text=question_4,
                         reply_markup=keyboards.get_power_of_attorney())
    await state.set_state(OrderFood.choosing_power_of_attorney)


# Если выбрал "ДА"
@router.message(OrderFood.choosing_full_name, F.text)
async def text_bot(message: Message, state: FSMContext):
    await state.update_data(chosen_full_name=message.text)
    await message.answer(text=good)
    # Запись в БД ФИО
    column = 'Фамилия_Имя_Отчество'
    data = message.text
    id = message.from_user.id
    sqlite.sql_db.sql_ins_new(column, data, int(id))
    await message.answer(text=question_5,
                         reply_markup=keyboards.get_message())
    await state.set_state(OrderFood.choosing_message)


# Ответвление: если выбрал "звонок специалиста"
@router.message(OrderFood.choosing_message,
                F.text == "Консультация специалиста (звонок Вам)")
async def specialist(message: Message, state: FSMContext):
    await state.update_data(chosen_message=message.text)
    await message.answer(text=good)
    # Запись в БД "нужен звонок специалиста"
    column = 'Обратный_звонок'
    data = message.text
    id = message.from_user.id
    sqlite.sql_db.sql_ins_new(column, data, int(id))
    await message.answer(text=question_phone_1,
                         reply_markup=keyboards.get_phone())
    await state.set_state(OrderFood.choosing_phone)


# Вытащить номер телефона
@router.message(OrderFood.choosing_phone, F.contact)
async def filter_phone(message: Message, bot: Bot, state: FSMContext):
    if message.contact.user_id == message.from_user.id:
        phone = message.contact.phone_number
        # запись номера в БД
        column = 'Номер_телефона'
        id = message.from_user.id
        sqlite.sql_db.sql_ins_new(column, phone, int(id))
        # Сообщение менеджеру
        await bot.send_message(chat_id=CONSTANT_USER_ID,
                               text=message_bot.message_kris.message_phone(id))
        # Очистка строки пользователя в БД (кроме номера телефона и ID)
        sqlite.sql_db.cleaning_bd(id)
        await message.answer(text=good_request,
                             reply_markup=keyboards.get_end())
        await state.clear()


# Ответвление: если выбрал "Продолжить общение здесь"
@router.message(OrderFood.choosing_message,
                F.text == "Продолжить оформление здесь")
async def clearance_here(message: Message, state: FSMContext):
    # можно не запоминать статус данного шага (ниже)
    await state.update_data(chosen_message=message.text)
    await message.answer(text=good)
    await message.answer(text=question_6,
                         reply_markup=ReplyKeyboardRemove())
    await state.set_state(OrderFood.choosing_summa)


# Желаемая сумма займа
@router.message(OrderFood.choosing_summa, F.text)
async def summa(message: Message, state: FSMContext):
    await state.update_data(chosen_summa=message.text)
    await message.answer(text=good)
    # Запись в БД Желаемой суммы займа
    column = 'Желаемая_сумма_займа'
    data = message.text
    id = message.from_user.id
    sqlite.sql_db.sql_ins_new(column, data, int(id))
    await message.answer(text=doc)
    await message.answer(text=doc_sts_pts_1)
    await state.set_state(OrderFood.choosing_data_pts_sts_1)


# т.к. нам необходим другой ответ после получения номера телефона,
# мы используем новый статус с телефоном
# Получение номера телефона №1
@router.message(OrderFood.choosing_phone_2, F.contact)
async def filter_phone_1(message: Message, bot: Bot, state: FSMContext):
    if message.contact.user_id == message.from_user.id:
        await state.update_data(choosing_phone_2=message.contact.phone_number)
        phone = message.contact.phone_number
        # Запись номера в БД
        column = 'Номер_телефона'
        id = message.from_user.id
        sqlite.sql_db.sql_ins_new(column, phone, int(id))
        # Сообщение менеджеру
        await bot.send_message(chat_id=CONSTANT_USER_ID,
                               text=message_bot.message_kris.message_data(id))
        file = message_bot.message_kris.message_photo(id)
        for i in file:
            if i != "-":
                full_name = sqlite.sql_db.select_data("Фамилия_Имя_Отчество",
                                                      id)
                await bot.send_message(chat_id=CONSTANT_USER_ID,
                                       text=f"Документ - {full_name}")
                await bot.send_photo(chat_id=CONSTANT_USER_ID,
                                     photo=i)
        # Очистка строки пользователя в БД (кроме номера телефона и ID)
        sqlite.sql_db.cleaning_bd(id)
        await message.answer(good_request_1,
                             reply_markup=keyboards.get_end())
    await state.clear()


# Линия "Нет"
# Доверенность есть/нет
@router.message(OrderFood.choosing_power_of_attorney,
                F.text == "Доверенность есть")
async def power_of_attorney_yes(message: Message, state: FSMContext):
    await state.update_data(choosing_power_of_attorney=message.text)
    await message.answer(good)
    # Запись в БД "доверенность есть"
    column = 'Наличие_доверенности'
    data = message.text
    id = message.from_user.id
    sqlite.sql_db.sql_ins_new(column, data, int(id))
    await message.answer(text=question_full_name,
                         reply_markup=ReplyKeyboardRemove())
    await state.set_state(OrderFood.choosing_full_name)


@router.message(OrderFood.choosing_power_of_attorney,
                F.text == "Доверенности нет")
async def power_of_attorney_no(message: Message, state: FSMContext):
    await state.update_data(choosing_power_of_attorney=message.text)
    # Запись в БД "доверенности нет"
    column = 'Наличие_доверенности'
    data = message.text
    id = message.from_user.id
    sqlite.sql_db.sql_ins_new(column, data, int(id))
    await message.answer(text=good)
    await message.answer(text=question_7,
                         reply_markup=keyboards.get_deal_owner())
    await state.set_state(OrderFood.choosing_attendance_at_the_deal)


# Собственник сможет присутствовать на сделке
@router.message(OrderFood.choosing_attendance_at_the_deal,
                F.text == "Сможет")
async def deal_owner_yes(message: Message, state: FSMContext):
    await state.update_data(choosing_attendance_at_the_deal=message.text)
    # Запись в БД "сможет"
    column = 'Присутствие_собственника_на_сделке'
    data = message.text
    id = message.from_user.id
    sqlite.sql_db.sql_ins_new(column, data, int(id))
    await message.answer(text=good)
    await message.answer(text=question_full_name,
                         reply_markup=ReplyKeyboardRemove())
    await state.set_state(OrderFood.choosing_full_name)


@router.message(OrderFood.choosing_attendance_at_the_deal,
                F.text == "Не сможет")
async def deal_owner_no(message: Message, state: FSMContext):
    await state.update_data(choosing_attendance_at_the_deal=message.text)
    # Запись в БД "Не сможет"
    await message.answer(text=error,
                         reply_markup=keyboards.get_end())


# Вернуться в начало
@router.message(F.text == "В главное меню")
async def filter_back(message: Message, state: FSMContext):
    await message.answer(text=back_to_top,
                         reply_markup=keyboards.get_client())
    await state.clear()
    await state.set_state(OrderFood.choosing_client)


# Фото документов
@router.message(OrderFood.choosing_data_pts_sts_1, F.photo)
async def data_1(message: Message, state: FSMContext):
    await state.update_data(chosen_data_pts_sts_1=message.photo)
    photo = message.photo[-1].file_id
    # Запись в БД код фото, кот. хранится на серверах Telegram
    column = 'ПТС_или_СТС_1'
    id = message.from_user.id
    sqlite.sql_db.sql_ins_new(column, photo, int(id))
    await message.answer(text=good)
    await message.answer(text=doc_sts_pts_2)
    await state.set_state(OrderFood.choosing_data_pts_sts_2)


@router.message(OrderFood.choosing_data_pts_sts_2, F.photo)
async def data_2(message: Message, state: FSMContext):
    await state.update_data(chosen_data_pts_sts_2=message.photo)
    photo = message.photo[-1].file_id
    column = 'ПТС_или_СТС_2'
    id = message.from_user.id
    sqlite.sql_db.sql_ins_new(column, photo, int(id))
    await message.answer(text=good)
    await message.answer(text=doc_pass_1)
    await state.set_state(OrderFood.choosing_data_passport_1)


@router.message(OrderFood.choosing_data_passport_1, F.photo)
async def data_3(message: Message, state: FSMContext):
    await state.update_data(chosen_data_passport_1=message.photo)
    photo = message.photo[-1].file_id
    column = 'Паспорт_1'
    id = message.from_user.id
    sqlite.sql_db.sql_ins_new(column, photo, int(id))
    await message.answer(text=good)
    await message.answer(text=doc_pass_2)
    await state.set_state(OrderFood.choosing_data_passport_2)


@router.message(OrderFood.choosing_data_passport_2, F.photo)
async def data_4(message: Message, state: FSMContext):
    await state.update_data(chosen_data_passport_2=message.photo)
    photo = message.photo[-1].file_id
    column = 'Паспорт_регистрация'
    id = message.from_user.id
    sqlite.sql_db.sql_ins_new(column, photo, int(id))
    await message.answer(text=good)
    power_of_attorney_bd = sqlite.sql_db.select_data("Наличие_доверенности",
                                                     id)
    if power_of_attorney_bd == "Доверенность есть":
        await message.answer(text=doc_power_of_attorney_1)

        await state.set_state(OrderFood.choosing_data_dover_1)
    else:
        await message.answer(text=question_phone_2,
                             reply_markup=keyboards.get_phone())
        await state.set_state(OrderFood.choosing_phone_2)


@router.message(OrderFood.choosing_data_dover_1, F.photo)
async def data_5(message: Message, state: FSMContext):
    await state.update_data(chosen_data_passport_2=message.photo)
    photo = message.photo[-1].file_id
    column = 'Доверенность_1'
    id = message.from_user.id
    sqlite.sql_db.sql_ins_new(column, photo, int(id))
    await message.answer(text=good)
    await message.answer(text=doc_power_of_attorney_2)
    await state.set_state(OrderFood.choosing_data_dover_2)


@router.message(OrderFood.choosing_data_dover_2, F.photo)
async def data_6(message: Message, state: FSMContext):
    await state.update_data(chosen_data_passport_2=message.photo)
    photo = message.photo[-1].file_id
    column = 'Доверенность_2'
    id = message.from_user.id
    sqlite.sql_db.sql_ins_new(column, photo, int(id))
    await message.answer(text=good)
    await message.answer(text=question_phone_2,
                         reply_markup=keyboards.get_phone())
    await state.set_state(OrderFood.choosing_phone_2)


@router.message(OrderFood.choosing_order_and_memo,
                F.text == "Памятка клиента")
async def cust_memo(message: Message, state: FSMContext):
    await message.answer(text=customer_memo,
                         reply_markup=keyboards.get_end())
