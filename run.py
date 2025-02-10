import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import TOKEN
from app.handlers import router  # импорт роутера из run.py
from app.database.models import async_main




async def main():
    await async_main()
    bot = Bot(TOKEN)  # бот получает токен и подключается к ТГ
    dp = Dispatcher()  # Обработка входящих сообщений
    dp.include_router(router)
    await dp.start_polling(bot)  # ожидает ответ от ТГ

if __name__=='__main__':
    logging.basicConfig(level=logging.INFO)  # !!! не стоит использовать в продакшн
    try:
        asyncio.run(main())  # запуск асинхронной функции возможен через 'async' и ее метод 'run'
    except KeyboardInterrupt:
        print('Бот прощается с Вами')
