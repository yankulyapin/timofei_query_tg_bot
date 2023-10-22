from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def districs_buttons(districs_list: list) -> InlineKeyboardMarkup:

    len_districs_list = len(districs_list)
    keyboard = []
    for i in range(len_districs_list):
        
        button = InlineKeyboardButton(text=districs_list[i], callback_data=districs_list[i])

        if i == 0 or i % 2 == 0:
            button1 = button
        else:
            button2 = button
            keyboard.append([button1, button2])
        
    if len_districs_list % 2 != 0:
        button = button = InlineKeyboardButton(text=districs_list[-1], callback_data=districs_list[-1])
        keyboard.append([button])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def queue_buttons(queue_list: list) -> InlineKeyboardMarkup:
    keyboard = []
    
    list = []

    for i in range(len(queue_list)):
        button = InlineKeyboardButton(text=queue_list[i], callback_data=queue_list[i])
        list.append(button)
    
    keyboard.append(list)
    keyboard.append([InlineKeyboardButton(text="Покинуть очередь", callback_data="Покинуть очередь")])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)