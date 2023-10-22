import asyncio
from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from aiogram import exceptions
from time import sleep
import datetime

import config, buttons, text


class Queue:

    bot = Bot(config.BOT_TOKEN, parse_mode="HTML")

    def __init__(self, queues_list: list, districs_list: list, chat_id, thread_id):
        self.queue_list                 = queues_list
        self.districs_list              = districs_list
        self.chat_id                    = chat_id
        self.thread_id                  = thread_id
        self.last_menu_districts        = None
        self.last_menu_directions       = None
        self.message_time_control: dict = {}
        
        self.queue                  = {}
        for i in queues_list:
            self.queue[i] = {}    

    async def send_message(self, message_text: str, message_markup=None):
        while True:
            try:
                time_now = datetime.datetime.now().strftime("%H:%M")
                if time_now not in self.message_time_control.keys():
                    self.message_time_control = {}
                    self.message_time_control = {time_now: 0}
                if self.message_time_control.get(time_now) > 18:
                    print("Флуд контроль!")
                    warning_message = await self.bot.send_message(chat_id=self.chat_id, text=text.TO_MANY_MESSAGES, message_thread_id=self.thread_id)
                    while datetime.datetime.now().strftime("%H:%M") == time_now:
                        sleep(5)
                    await self.bot.delete_message(config.CHAT_ID, warning_message.message_id)
                message = await self.bot.send_message(chat_id=self.chat_id, text=message_text, message_thread_id=self.thread_id, reply_markup=message_markup)
                last_message = message
                self.message_time_control[time_now] = self.message_time_control.get(time_now) + 1
            except exceptions.TelegramRetryAfter:
                print("Флуд телеграм ошибка.")
                sleep(35)
            else:
                return message
                

    async def send_queue(self):
        if self.last_menu_districts:
            try:
                await self.bot.delete_message(self.chat_id, self.last_menu_districts.message_id)
            except exceptions.TelegramBadRequest:
                print("Не смог удалить меню выбора очереди.")

        #self.last_menu_districts = await self.bot.send_message(self.chat_id, text.DISTRICS_MENU_TEXT, message_thread_id=self.thread_id, reply_markup=buttons.districs_buttons(self.districs_list))
        self.last_menu_districts = await self.send_message(text.DISTRICS_MENU_TEXT, buttons.districs_buttons(self.districs_list))
        if self.last_menu_directions:
            try:
                await self.bot.delete_message(self.chat_id, self.last_menu_directions.message_id)
            except exceptions.TelegramBadRequest:
                print("Не смог удалить меню выбора направления.")
        #self.last_menu_directions = await self.bot.send_message(chat_id=self.chat_id, text=text.queues_menu_text(self.queue), message_thread_id=self.thread_id, reply_markup=buttons.queue_buttons(queue_list=self.queue_list))
        self.last_menu_directions = await self.send_message(text.queues_menu_text(self.queue), buttons.queue_buttons(queue_list=self.queue_list))
    
    async def add_queue(self, district: str, user_id, first_name, last_name, username) -> str:
        active_users = []
        for i_queue in self.queue.keys():
            if i_queue != district:
                for user in self.queue[i_queue].keys():
                    active_users.append(user)
        
        if user_id in self.queue[district].keys():
            return text.already_in_queue(district)
        elif user_id in active_users:
            return text.ALREADY_IN_OTHER_QUEUE
        else:
            self.queue[district][user_id] = {"first_name":  first_name,
                                            "last_name":    last_name,
                                            "username":     username,
                                            "districs":     [],
                                            "time":         datetime.datetime.now()}
            user_info = self.queue[district][user_id]
            type, first_name, last_name, username = district, user_info.get('first_name'), user_info.get('last_name'), user_info.get('username')
            #await self.bot.send_message(self.chat_id, text=text.chat_add_queue(type, first_name, last_name, username), message_thread_id=self.thread_id)
            await self.send_message(text.chat_add_queue(type, first_name, last_name, username))
            await self.send_queue()
            return text.added_to_queue(district)

    async def select_district(self, user_id, district) -> str:
        for i_queue in self.queue.keys():
            for i_user_id in self.queue[i_queue].keys():
                if i_user_id == user_id:
                    if district not in list(self.queue[i_queue][i_user_id].get("districs")): # Если нет района в юзере
                        self.queue[i_queue][i_user_id]['districs'].append(district)
                        await self.send_queue()
                        return text.added_district(district)
                    else:
                        self.queue[i_queue][i_user_id]['districs'].remove(district)
                        await self.send_queue()
                        return text.remove_district(district)
        return text.NOT_IN_LIST

    async def leave_queue(self, user_id) -> str:
        for i_queue in self.queue.keys():
            for i_user_id in self.queue[i_queue].keys():
                if i_user_id == user_id:
                    user_info = self.queue[i_queue][i_user_id]
                    queue_type, first_name, last_name, username = i_queue, user_info.get('first_name'), user_info.get('last_name'), user_info.get('username')
                    self.queue[i_queue].pop(i_user_id)
                    #await self.bot.send_message(chat_id=self.chat_id, text=text.chat_leave_queue(queue_type, first_name, last_name, username), message_thread_id=self.thread_id)
                    await self.send_message(text.chat_leave_queue(queue_type, first_name, last_name, username))
                    await self.send_queue()
                    return text.remove_from_queue(i_queue)

    async def timer_checker(self):
        for type_queue in self.queue.keys():
            users_id = list(self.queue[type_queue].keys())
            for user_id in users_id:
                addition_time = self.queue[type_queue][user_id].get('time')
                delta = datetime.datetime.now() - addition_time
                if delta.seconds > config.MAX_QUEUE_TIME:
                    await self.leave_queue(user_id)

    async def clear_queue(self, admin: str):
        for type in self.queue.keys():
            self.queue[type] = {}
        await self.send_message(f"Список очистил администратор - {admin}.")
        await self.send_queue()
        return "Списки очищены."

    async def press_button(self, callback_query: CallbackQuery):
        await self.timer_checker()
        if callback_query.data in self.queue_list: # Кнока выбора очереди
            add_user = await self.add_queue(callback_query.data, callback_query.from_user.id, callback_query.from_user.first_name, callback_query.from_user.last_name, callback_query.from_user.username)
            if config.TEST:
                await self.bot.answer_callback_query(callback_query.id, text=add_user, show_alert=False)
            else:
                await self.bot.answer_callback_query(callback_query.id, text=add_user, show_alert=True)
        elif callback_query.data in self.districs_list: # Кнопка выбора района
            select = self.select_district(callback_query.from_user.id, callback_query.data)
            if config.TEST:
                await self.bot.answer_callback_query(callback_query.id, text=await select, show_alert=False)
            else:
                await self.bot.answer_callback_query(callback_query.id, text=await select, show_alert=True)
        else: # Выход из очереди
            if config.TEST:
                await self.bot.answer_callback_query(callback_query.id, text=await self.leave_queue(callback_query.from_user.id), show_alert=False)
            else:
                await self.bot.answer_callback_query(callback_query.id, text=await self.leave_queue(callback_query.from_user.id), show_alert=True)
    

















queue = Queue(config.QUEUES_LIST, config.DISTRICS_LIST, config.CHAT_ID, config.THREAD_ID)