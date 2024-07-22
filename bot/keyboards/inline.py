from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def languages_inline_buttons():
    languages = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🇷🇺 РУССКИЙ", callback_data="rus")],
            [InlineKeyboardButton(text="🇬🇧 ENGLISH", callback_data="eng")]
        ]
    )
    return languages


delete_rus = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="❌", callback_data="delr")]])
delete_eng = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="❌", callback_data="dele")]])