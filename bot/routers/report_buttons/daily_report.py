from aiogram.types import InlineKeyboardButton

buttons_conf = [
    ("Получить логины", "get_logins"),
    ("Конфигурация рассылки", "get_base"),
    ("Справка", "daily_report_info"),
    ("Назад", "back_to_report_menu"),
]

daily_report_buttons = [[]]

buttons = [
    InlineKeyboardButton(text=f"{elem[0]}", callback_data=f"{elem[1]}") for elem in buttons_conf
]

for btn in buttons:
    if len(daily_report_buttons[-1]) < 2:
        daily_report_buttons[-1].append(btn)
    else:
        daily_report_buttons.append([])
        daily_report_buttons[-1].append(btn)
