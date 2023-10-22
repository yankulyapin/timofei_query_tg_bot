# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =


# МОЖНО ИЗМЕНЯТЬ

# "Название кнопки": "Callback.data"


QUEUES_LIST = ["Авто", "Вело"]
DISTRICS_LIST   =  ["Балатово", "Карпинского", "Парковый", "Казармы", "Мотовилиха", "Грибы", "Крохоля", "Закамск", "Курья", "Гайва" , "Центр", "Гулливер", "Центр верх", "Запруд"]
MAX_QUEUE_TIME: int = 70 * 60 # В секундах
ADMIN_LIST = [5949089515]














# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

# Не изменять
if input("Это тест?(y/n): ") == "y":
    TEST = True
else:
    TEST = False


TEST_BOT_TOKEN  = "6379536272:AAGdsFPNfQBYwhvH4k69u_MjQuSi8-ruFbk"
TEST_CHAT_ID    = "-1001835250790"
TEST_THREAD_ID  = None


BOT_TOKEN   = ""
CHAT_ID     = ""
THREAD_ID   = ""


if TEST:
    BOT_TOKEN   = TEST_BOT_TOKEN
    CHAT_ID     = TEST_CHAT_ID
    THREAD_ID   = None
else:
    BOT_TOKEN   = input("Введите BOT_TOKEN: ")
    CHAT_ID     = input("Введите CHAT_ID: ")
    THREAD_ID   = input("Введите THREAD_ID (если это не форум нажмите enter): ")