from aiogram.types import InlineKeyboardButton

buttons_conf = [
    ("Ежедневные авто-отчеты", "daily_report"),
    ("Сформировать отчет по клиенту", "client_report"),
    ("Назад", "back_to_main_menu"),
]

main_buttons = [
    [
        InlineKeyboardButton(text=f"{elem[0]}", callback_data=f"{elem[1]}"),
    ] for elem in buttons_conf
]
