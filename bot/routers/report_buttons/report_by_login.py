from aiogram.types import InlineKeyboardButton


def create_login_report_meny(logins):
    login_report_buttons = [[]]
    buttons = [
        InlineKeyboardButton(text=f"{elem}", callback_data=f"{elem}") for elem in logins
    ]
    for btn in buttons:
        if len(login_report_buttons[-1]) < 2:
            login_report_buttons[-1].append(btn)
        else:
            login_report_buttons.append([])
            login_report_buttons[-1].append(btn)

    return login_report_buttons
