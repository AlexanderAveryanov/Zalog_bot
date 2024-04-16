from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from router_1 import OrderFood
from keyboards import keyboards

router = Router()


# Начало работы после перезапуска бота либо введения несуществующей команды
@router.message()
async def test(message: Message, state: FSMContext):
    await message.answer(f"""<b>
{message.from_user.full_name}, вы возвращены в главное меню!</b>""",
                         reply_markup=keyboards.get_client())
    await state.set_state(OrderFood.choosing_client)
