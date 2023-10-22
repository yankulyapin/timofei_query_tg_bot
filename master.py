import asyncio
from aiogram import Bot, Dispatcher
from time import sleep 
from handlers import master_handler

import config


# Запуск бота
async def main():

    bot = Bot(token = config.BOT_TOKEN, parse_mode="HTML")
    dp = Dispatcher()


    print("Добавляем в диспетчер мастер роутер...")
    dp.include_router(master_handler.router)
    print("Запускаем функцию присоединения роутеров к мастер роутеру")
    master_handler.add_routers()

    # Удаляем накопившиеся сообщения для избежания флуда от бота
    print("Очищаем запросы поступившие до запуска бота...")
    await bot.delete_webhook(drop_pending_updates=True)
    print("Запускаем бота...")
    while True:
        try:
            await dp.start_polling(bot)
        except Exception as e:
            print("Критическая ошибка!!!", e)
            sleep(1)

if __name__ == "__main__":
    asyncio.run(main())