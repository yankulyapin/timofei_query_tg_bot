from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

import config

from ClassQueue import queue


router = Router()
router.message.filter(F.chat.id == int(config.CHAT_ID))
if config.THREAD_ID:
    router.message.filter(F.message_thread_id == int(config.THREAD_ID))


@router.message(Command("start"))
async def chat_cmd_start(message: Message):
    await message.answer("<b>Здравствуй!</b>\n\nЯ бот очереди написанный для курьеров ВкусВила.\nЯ пока-что в разработке...")

@router.message(Command("menu"))
async def chat_cmd_menu(message: Message):
    await message.delete()
    await queue.send_queue()

@router.message(Command("clear"))
async def chat_cmd_menu(message: Message):
    await message.delete()
    await queue.clear_queue()

@router.callback_query(F.message.chat.id != config.CHAT_ID)
async def callback_queue(callback_query: CallbackQuery):
    if "del" in callback_query.data:
        for district in queue.districs_list:
            if callback_query.data.replace('del', '') == district:
                queue.districs_list.remove(callback_query.data.replace('del', ''))
                await callback_query.answer(f"Вы удалили район {callback_query.data.replace('del', '')}", show_alert=True)
                return True
        await callback_query.answer("Нет такого района, какая-то ошибка...", show_alert=True)
    else:
        await queue.press_button(callback_query)