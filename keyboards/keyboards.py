from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardBuilder
from utils.translation import *

from database.queries import *


def creator_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Send a message")],
            [KeyboardButton(text="Stories")]
        ], resize_keyboard=True
    )

    return keyboard


def main_keyboard(language):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=MESSAGES['instruction'][language])],
            [KeyboardButton(text=MESSAGES['command_list'][language])],
            [KeyboardButton(text=MESSAGES['report_a_bug'][language])],
            [KeyboardButton(text=MESSAGES['about_creator'][language])],
            [KeyboardButton(text=MESSAGES['change_language'][language])]
        ], resize_keyboard=True
    )

    return keyboard


def languages_buttons():
    languages = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🇷🇺 РУССКИЙ")],
            [KeyboardButton(text="🇬🇧 ENGLISH")]
        ], resize_keyboard=True
    )
    return languages


def lang_stories_buttons():
    languages = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🇷🇺")],
            [KeyboardButton(text="🇬🇧")]
        ], resize_keyboard=True
    )
    return languages


back = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="⬅️")]], resize_keyboard=True)

stories_rus = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="⬅️")], [KeyboardButton(text="Добавить ➕")]], resize_keyboard=True)
stories_eng = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="⬅️")], [KeyboardButton(text="Add ➕")]], resize_keyboard=True)


def russian_stories():
    builder = ReplyKeyboardBuilder()
    stories = get_all_rus_stories_titles()
    [builder.button(text=story_title).adjust(2) for story_title in stories]
    builder.row(KeyboardButton(text="Добавить ➕"))
    builder.row(KeyboardButton(text="⬅️"))
    return builder.as_markup(resize_keyboard=True)


def english_stories():
    builder = ReplyKeyboardBuilder()
    stories = get_all_eng_stories_titles()
    [builder.button(text=story_title).adjust(2) for story_title in stories]
    builder.row(KeyboardButton(text="Add ➕"))
    builder.row(KeyboardButton(text="⬅️"))
    return builder.as_markup(resize_keyboard=True)