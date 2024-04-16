from aiogram.types import Message, PreCheckoutQuery, LabeledPrice
from aiogram.types import ReplyKeyboardRemove
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
import math
from router_1 import OrderFood
from keyboards import keyboards
from config import PAYMENTS_TOKEN, item_url
from router_1 import CONSTANT_MENEGER_ID
from text_bot import min_payment, quest_full_name_dog, question_payment
from text_bot import good_payment, max_payment


router = Router()


@router.message(OrderFood.choosing_order_and_memo,
                F.text == "Оплата по договору")
async def full_name(message: Message, state: FSMContext):
    await state.update_data(choosing_order_and_memo=message.text)
    await message.answer(quest_full_name_dog,
                         reply_markup=ReplyKeyboardRemove())
    await state.set_state(OrderFood.choosing_full_name_order)


@router.message(OrderFood.choosing_full_name_order, F.text)
async def choosing_order_and_memo(message: Message, state: FSMContext):
    await state.update_data(choosing_full_name_order=message.text)
    global full_name
    full_name = message.text
    await message.answer(question_payment,
                         reply_markup=ReplyKeyboardRemove())
    await state.set_state(OrderFood.choosing_order)


@router.message(OrderFood.choosing_order, F.text)
async def choosing_order(message: Message, state: FSMContext):
    global payment_res
    payment = (message.text).replace(",", ".")
    if float(payment) <= 99:
        await message.answer(min_payment)
        await message.answer(question_payment)
    elif float(payment) > 150000:
        await message.answer(max_payment)
        await message.answer(question_payment)
    else:
        payment_res = math.ceil(float(payment)) * 100
        PRICES = [
            LabeledPrice(label="Внесение средств на счет", amount=payment_res)
        ]
        await message.answer_invoice(title="Оплата по договору",
                                     description="Оплата товара",
                                     provider_token=PAYMENTS_TOKEN,
                                     currency='RUB',
                                     photo_url=item_url,
                                     photo_height=100,
                                     photo_size=100,
                                     need_name=True,
                                     need_email=True,
                                     need_phone_number=True,
                                     prices=PRICES,
                                     start_parameter='example',
                                     payload='some_invoice')
        await state.set_state(OrderFood.choosing_order_1)


@router.pre_checkout_query(OrderFood.choosing_order_1)
async def checkout_process(pre_checkout_query: PreCheckoutQuery, bot: Bot,
                           state: FSMContext):
    await bot.answer_pre_checkout_query(pre_checkout_query.id,
                                        ok=True)
    await state.set_state(OrderFood.choosing_order_2)


@router.message(OrderFood.choosing_order_2,
                F.successful_payment)
async def succesful_payment(message: Message, bot: Bot,):
    price = message.successful_payment.total_amount
    text = f"Оплата по договору\n"  \
           f"Ф.И.О: {full_name}\n" \
           f"Номер телефона: " \
           f"{message.successful_payment.order_info.phone_number}\n" \
           f"Сумма: {int(price/100)} рублей"
    await bot.send_message(chat_id=CONSTANT_MENEGER_ID,
                           text=text)
    await message.answer(good_payment,
                         reply_markup=keyboards.get_end())
