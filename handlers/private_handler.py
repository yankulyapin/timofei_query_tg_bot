from aiogram import Router, F
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

import config

from ClassQueue import queue


router = Router()
router.message.filter(F.chat.type == "private")


@router.message(Command("start"))
async def private_cmd_start(message: Message):
    if message.from_user.id in config.ADMIN_LIST:
        message_text = "<b>Добро пожаловать!</b>\n\nКоманды администратора:\n"
        message_text += "   1) /clear - очистить очередь принудительно.\n"
        message_text += "   2) /addadmin (id пользователя) - добавить пользователя в список администраторов.\n"
        message_text += "   3) /deladmin (id пользователя) - удалить пользователя из списка администраторов.\n"
        message_text += "   4) /adminslist - список администраторов.\n"
        message_text += "   5) /adddistrict (название района) - добавить район.\n"
        message_text += "   6) /deldistrict - удалить район.\n"
        await message.answer(message_text)
    else:
        await message.answer("<b>Здравствуй!</b>\n\nЯ бот очереди написанный для курьеров ВкусВила.\nЯ пока-что в разработке...")


ADMIN_COMMANDS = Command("clear", "addadmin", "deladmin", "adminslist", "adddistrict", "deldistrict")

@router.message(ADMIN_COMMANDS)
async def admin_cmd(message: Message, command: CommandObject):
    if message.from_user.id in config.ADMIN_LIST:
        input_command = command.command
        if command.command == "clear":
            await message.answer(await queue.clear_queue(str(message.from_user.username)))
        elif command.command == "addadmin":
            try:
                config.ADMIN_LIST.append(int(command.args))
            except Exception:
                await message.answer("Не верно ввели ID пользователя.")
            else:
                await message.answer(f"{command.args} - успешно добавлен в список администраторов.")
        elif command.command == "deladmin":
            try:
                if int(command.args) in config.ADMIN_LIST:
                    config.ADMIN_LIST.remove(int(command.args))
            except Exception:
                await message.answer("Не верно вели ID администратора")
            else:
                await message.answer(f"Администратор {command.args} удален.")
        elif command.command == "adminslist":
            await message.answer(str(config.ADMIN_LIST))
        elif command.command == "adddistrict":
            if command.args != None:
                try:
                    config.DISTRICS_LIST.append(str(command.args))
                except Exception:
                    await message.answer("Не верно ввели название района.")
                else:
                    await message.answer(f"Район {str(command.args)} успешно добавлен в список районов.")
            else:
                await message.answer("Вы не ввели название района, повторите /adddistrict (название района) - добавить район.")
        elif command.command == "deldistrict":
            districs_list = queue.districs_list
            len_districs_list = len(districs_list)
            keyboard = []
            for i in range(len_districs_list):
        
                button = InlineKeyboardButton(text=districs_list[i], callback_data=f"del{districs_list[i]}")

                if i == 0 or i % 2 == 0:
                    button1 = button
                else:
                    button2 = button
                    keyboard.append([button1, button2])
        
            if len_districs_list % 2 != 0:
                button = button = InlineKeyboardButton(text=districs_list[-1], callback_data=f"del{districs_list[i]}")
                keyboard.append([button])
            
            await message.answer("Нажмите на район который хотите удалит:", reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard))

        else:
            await message.answer("Нет такой команды.")
