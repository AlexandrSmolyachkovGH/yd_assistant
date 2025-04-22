from aiogram.types import InlineKeyboardButton

buttons_conf = [
    ("Ежедневные авто-отчеты", "daily_report"),
    ("Для тестов", "client_report"),
    ("Отчет в срезе Аккаунта", "login_report_menu_account"),
    ("Отчет в срезе Кампаний", "login_report_menu"),
]

main_buttons = [
    [
        InlineKeyboardButton(text=f"{elem[0]}", callback_data=f"{elem[1]}"),
    ] for elem in buttons_conf
]
main_buttons.append([
    InlineKeyboardButton(text="Назад", callback_data="back_to_main_menu"),
    InlineKeyboardButton(text="Об отчетах", callback_data="about_reports"),
])
