DISTRICS_MENU_TEXT = "<b>Меню редактирования маршрута.</b>\n\nНажмите на нужный вам район для добавление/удаление из вашего маршрута."

def queues_menu_text(queue: dict) -> str: # Меню очереди
    text_queue = ""
    for type_transport in queue.keys():
        text_queue += f"<b>{type_transport}:</b>\n"
        for i in range(len(queue[type_transport].keys())):
            user_id         = list(queue[type_transport].keys())[i]
            user_info: dict = queue[type_transport][user_id]
            text_queue += f"  {i+1}) <b>{user_info.get('first_name')}</b>"
            if user_info.get('last_name'):
                text_queue += f" <b>{user_info.get('last_name')}</b>"
            if user_info.get('districs'):
                text_queue += " - (" + ', '.join(user_info.get('districs')) + ")"
            else:
                text_queue += " - ОЖИДАЕТ"
            text_queue += "\n"
        text_queue += "\n\n"

    return text_queue

def added_to_queue(queue) -> str: 
    return f"Вы записаны в список {queue}"
def already_in_queue(queue) -> str: 
    return f"Вы уже состоите в списке {queue}." # Вы уже состоите в этом списке

ALREADY_IN_OTHER_QUEUE      = "Вы состоите в другой очереди." # Вы есть в другом списке

def remove_from_queue(queue) -> str:
    return f"Вы удалены из списка {queue}."

def added_district(district) -> str:
    return f"Добавлен район {district}."

def remove_district(district) -> str:
    return f"Удален район {district}"

NOT_IN_LIST = "Чтобы выбрать район нужно встать в список."

def chat_add_queue(queue_type, first_name, last_name, username) -> str:
    chat_text = f"{first_name} "
    if last_name:
        chat_text += f"{last_name} "
    chat_text += f"встал в очередь {queue_type}."
    if username:
        chat_text += f" (@{username})"
    
    return chat_text

def chat_leave_queue(queue_type, first_name, last_name, username) -> str:
    chat_text = f"{first_name} "
    if last_name:
        chat_text += f"{last_name} "
    chat_text += f"покинул очередь {queue_type}."
    if username:
        chat_text += f" (@{username})"

    return chat_text

TO_MANY_MESSAGES = "Бот не может отправлять так много сообщений.\nПодождите следующую минуту и <b>повторите действие</b>."