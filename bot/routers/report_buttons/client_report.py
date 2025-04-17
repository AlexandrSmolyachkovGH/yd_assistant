from aiogram.types import InlineKeyboardButton

buttons_conf = [
    ("Получить логины", "get_logins"),
    ("Получить статистику", "get_base"),
    ("Получить баланс", "get_balance"),
    ("Справка", "client_report_info"),
    ("Назад", "back_to_report_menu"),
]

client_report_buttons = [[]]

buttons = [
    InlineKeyboardButton(text=f"{elem[0]}", callback_data=f"{elem[1]}") for elem in buttons_conf
]

for btn in buttons:
    if len(client_report_buttons[-1]) < 2:
        client_report_buttons[-1].append(btn)
    else:
        client_report_buttons.append([])
        client_report_buttons[-1].append(btn)
