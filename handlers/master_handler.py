from aiogram import Router

from handlers import private_handler, chat_handler


router = Router()

def add_routers():
    print("Добавляем к мастер роутеру приват роутер...")
    router.include_router(private_handler.router)
    print("Добавляем к мастер роутеру чат роутер...")
    router.include_router(chat_handler.router)