from aiogram import Router, Bot
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from database.queries import *

from keyboards import keyboards as rp, inline as il

from utils.translation import MESSAGES

from filters.filters import *

from FSM.states import *


rt = Router()


@rt.message(IsPrivateChat(), CommandStart())
async def command_start_handler(message: Message) -> None:
    insert_id(message.chat.id)
    await message.answer(
        f"Hello, <b>{message.from_user.full_name}</b>\nChoose your language:\n\n"
        f"Приветствую тебя, <b>{message.from_user.full_name}</b>\nВыбери свой язык:", reply_markup=rp.languages_buttons())


@rt.message(IsPrivateChat(), lambda message: message.text in ["🇷🇺 РУССКИЙ", "🇬🇧 ENGLISH"])
async def set_chat_language(message: Message):
    if message.text == "🇷🇺 РУССКИЙ":
        insert_language('rus', message.chat.id)
    elif message.text == "🇬🇧 ENGLISH":
        insert_language('eng', message.chat.id)
    language = identify_language(message.chat.id)
    await message.answer(MESSAGES['welcome_user'][language], reply_markup=rp.main_keyboard(language))


@rt.message(IsPrivateChat(), lambda message: message.text in ["About the creator", "О создателе"])
async def list_commands(message: Message):
    language = identify_language(message.chat.id)
    await message.answer(MESSAGES['about'][language])


@rt.message(IsPrivateChat(), lambda message: message.text in [
"Report a bug / Suggest an improvement",
"Сообщить об ошибке / Предложить улучшение"])
async def bug_report(message: Message, state: FSMContext):
    language = identify_language(message.chat.id)
    await state.set_state(BugReport.message)
    await message.answer(MESSAGES['bug_reported'][language])


@rt.message(IsPrivateChat(), BugReport.message)
async def send_newsletter(message: Message, state: FSMContext, bot: Bot) -> None:
    language = identify_language(message.chat.id)
    await message.answer(MESSAGES['waiting'][language])
    try:
        if message.from_user.username:
            await bot.send_message(chat_id=7215866709, text=f"<b>There is a message from @{message.from_user.username}!</b>")
        else:
            await bot.send_message(chat_id=7215866709, text=f"<b>There is a message from @{message.from_user.full_name}!</b>")
        await message.send_copy(chat_id=7215866709, reply_markup=il.admin_answer(message.from_user.id))
        await message.answer(MESSAGES['sending_success'][language])
    except:
        await message.answer(MESSAGES['sending_error'][language])
    await state.clear()


@rt.message(IsPrivateChat(), lambda message: message.text in ["Add the bot to a group!",
"Добавить бота в группу!"])
async def add_me_instructions(message: Message):
    language = identify_language(message.chat.id)
    await message.answer(MESSAGES['how_to_add'][language])


@rt.message(IsPrivateChat(), lambda message: message.text in ["List of the bot commands",
"Список команд бота"])
async def list_commands(message: Message):
    language = identify_language(message.chat.id)
    await message.answer(MESSAGES['list_of_commands'][language])


@rt.message(IsPrivateChat(), lambda message: message.text in ["Change language", "Изменить язык"])
async def switch_languages(message: Message):
    await command_start_handler(message)
