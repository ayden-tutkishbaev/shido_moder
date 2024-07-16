from aiogram import F, Router, Bot
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message, ChatPermissions

import configs
from bot.utils import *
from database.queries import *

from contextlib import suppress

from aiogram.exceptions import TelegramBadRequest


rt = Router()


@rt.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    full_name = message.from_user.full_name
    telegram_id = message.from_user.id
    insert_data_to_creation(full_name=full_name, telegram_id=telegram_id)
    await message.answer(f"Hello, <b>{message.from_user.full_name}</b>!"
                         f"\nBe careful since the data about you is being saved.")


@rt.message(Command(commands=["mute"]))
async def mute_handler(message: Message, bot: Bot, command: CommandObject):
    reply = message.reply_to_message
    if not reply:
        return await message.answer(f"Not found")

    until_date = time_converter(command.args)
    mention = reply.from_user.mention_html(reply.from_user.first_name)

    chat_member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if chat_member.status not in ['administrator', 'creator']:
        return await message.answer("Команда доступна только администраторам группы!")

    reason_filter = command.args.split(" ")
    reason = " ".join(reason_filter[1:])

    with suppress(TelegramBadRequest):
        await bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=reply.from_user.id,
            permissions=ChatPermissions(can_send_messages=False),
            until_date=until_date
        )
        print(until_date)
        if reason == "":
            await message.answer(f"<b>{mention}</b> <i>заткнут по</i><b> неизвестной причине</b>!")
        else:
            await message.answer(f"<b>{mention}</b> <i>заткнут по причине</i>: <b>{reason}</b>!")


@rt.edited_message()
async def edited_banned_words_handler(message: Message, bot: Bot) -> None:
    text = message.text.lower()
    chat_member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if chat_member.status not in ['administrator', 'creator']:
        if triggers(text):
            await message.delete()
            await message.answer(f"{message.from_user.mention_html(message.from_user.first_name)}, ругаться здесь нельзя!")


@rt.message()
async def banned_words_handler(message: Message, bot: Bot) -> None:
    text = message.text.lower()
    chat_member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if chat_member.status not in ['administrator', 'creator']:
        if triggers(text):
            await message.delete()
            await message.answer(f"{message.from_user.mention_html(message.from_user.first_name)}, ругаться здесь нельзя!")