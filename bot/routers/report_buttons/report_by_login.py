from aiogram.types import InlineKeyboardButton


def create_login_report_menu(logins, account: bool = False):
    callback_mask = ["get_simple_report_", "get_account_report_"]
    login_report_buttons = [[]]
    buttons = [
        InlineKeyboardButton(
            text=lgn,
            callback_data=f"{callback_mask[account]}{lgn}",
        ) for lgn in logins
    ]
    for btn in buttons:
        if len(login_report_buttons[-1]) < 2:
            login_report_buttons[-1].append(btn)
        else:
            login_report_buttons.append([])
            login_report_buttons[-1].append(btn)

    login_report_buttons.append([
        InlineKeyboardButton(text="Обновить логины", callback_data="update_logins"),
        InlineKeyboardButton(text="Назад", callback_data="back_to_report_menu"),
    ])

    return login_report_buttons
