from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def back_to_main_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="🔙 Назад в главное меню",
                callback_data="back_to_main"
            )]
        ]
    )