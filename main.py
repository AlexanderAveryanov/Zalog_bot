import asyncio
import logging
from aiogram import Bot, Dispatcher
import router_1
import router_2
import order
from config import TOKEN_API


# Запуск процесса поллинга новых апдейтов (поиска)
async def main():
    # Включаем логирование, чтобы не пропустить важные сообщения
    logging.basicConfig(level=logging.INFO)
    # Объект бота
    bot = Bot(token=TOKEN_API,
              parse_mode="HTML")  # чтобы не указывать везде parse_mode
    # Диспетчер
    dp = Dispatcher()
    # Запуск роутеров имеет значение! (очередь поиска)
    dp.include_routers(router_1.router, order.router, router_2.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    asyncio.run(main())

# allowed_updates=dp.resolve_used_update_types() - от диспетчера,
# который пройдёт по всем роутерам, узнает, хэндлеры на какие типы есть в коде,
#  и попросит Telegram присылать только их.
