import random

from aiogram import F, Router, Bot, types
from aiogram.filters import CommandStart, Command, CommandObject, ChatMemberUpdatedFilter, IS_MEMBER, IS_NOT_MEMBER
from aiogram.types import Message, ChatPermissions, ChatMemberUpdated, CallbackQuery

import configs
from bot.utils import *
from database.queries import *
from translation import *

from contextlib import suppress

from aiogram.exceptions import TelegramBadRequest
from bot.keyboards import inline as il

from bot.keyboards import keyboards as rp

rt = Router()


@rt.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    chat_id = message.chat.id
    insert_id(chat_id)
    await message.answer(
        f"Hello, <b>{message.from_user.full_name}</b>\nChoose your language:\n\n"
        f"Приветствую тебя, <b>{message.from_user.full_name}</b>\nВыбери свой язык:", reply_markup=rp.languages_buttons())


@rt.message(lambda message: message.text in ["🇷🇺 РУССКИЙ", "🇬🇧 ENGLISH"])
async def set_message(message: Message):
    if message.text == "🇷🇺 РУССКИЙ":
        insert_language("rus", message.chat.id)
    if message.text == "🇬🇧 ENGLISH":
        insert_language("eng", message.chat.id)
    language = identify_language(message.chat.id)
    await message.delete()
    await message.answer(MESSAGES['welcome_user'][language], reply_markup=rp.main_keyboard(language))


@rt.my_chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def on_user_joined(event: ChatMemberUpdated):
    new_member = event.new_chat_member
    await event.answer(f"Добро пожаловать, {new_member.user.full_name}!")


@rt.message(lambda message: message.text in ["Шидо расскажи историю", "Shido tell a story"])
async def dushnila_shido(message: Message):
    language = identify_language(message.chat.id)
    await message.answer(MESSAGES['dushnila'][language])


@rt.message(lambda message: message.text in ["Шидо, расскажи историю", "Shido, tell a story"])
async def shido_tells_a_story(message: Message):
    language = identify_language(message.chat.id)
    if language == "eng":
        story = get_eng_story(random.choice(get_all_eng_stories_ids()))
        await message.answer(f"<b>{story[0]}</b>\n\n{story[1]}")
    elif language == "rus":
        story = get_rus_story(random.choice(get_all_rus_stories_ids()))
        await message.answer(f"<b>{story[0]}</b>\n\n{story[1]}")


@rt.message(Command(commands=['language']))
async def set_bot_language(message: Message, bot: Bot) -> None:
    chat_id = message.chat.id
    insert_id(chat_id)
    chat_member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if chat_member.status in ['administrator', 'creator']:
        await message.answer(f"Hello, members of <b>{message.chat.title}</b> chat!\nChoose a language on which I will be operated.\n:)",
                             reply_markup=il.languages_inline_buttons())
    else:
        await message.answer("Access prohibited!")


@rt.callback_query(lambda callback: callback.data in ["rus", "eng", "uzb"])
async def set_message(callback: CallbackQuery, bot: Bot):
    chat_member = await bot.get_chat_member(callback.message.chat.id, callback.message.from_user.id)
    if chat_member.status in ['administrator', 'creator']:
        chat_id = callback.message.chat.id
        language = callback.data
        insert_language(language, chat_id)
        chat_id = callback.message.chat.id
        language = identify_language(chat_id)
        await callback.message.delete()
        await callback.message.answer(MESSAGES['welcome_message'][language])
    else:
        await callback.answer("Access prohibited")


@rt.message(Command(commands=["mute"]))
async def mute_handler(message: Message, bot: Bot, command: CommandObject):
    chat_id = message.chat.id
    language = identify_language(chat_id)

    reply = message.reply_to_message
    if not reply:
        return await message.answer(f"Not found")

    until_date = time_converter(command.args)
    mention = reply.from_user.mention_html(reply.from_user.first_name)

    chat_member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if chat_member.status not in ['administrator', 'creator']:
        return await message.answer(MESSAGES['admin_rights_prohibited'][language])

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
            await message.answer(f"<b>{mention}</b> {MESSAGES['muted_no_reason'][language]}!")
        else:
            await message.answer(f"<b>{mention}</b> {MESSAGES['muted'][language]} <b>{reason}</b>!")



#########################################################################################################
@rt.message(Command(commands=["unmute"]))
async def mute_handler(message: Message, bot: Bot):
    chat_id = message.chat.id
    language = identify_language(chat_id)

    reply = message.reply_to_message
    if not reply:
        return await message.answer(f"Not found")

    mention = reply.from_user.mention_html(reply.from_user.first_name)

    chat_member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if chat_member.status not in ['administrator', 'creator']:
        return await message.answer(MESSAGES['admin_rights_prohibited'][language])

    with suppress(TelegramBadRequest):
        await bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=reply.from_user.id,
            permissions=ChatPermissions(
                can_send_messages=True,
                can_send_photos=True,
                can_send_videos=True,
                can_send_documents=True,
                can_send_other_messages=True,
                can_send_audios=True,
                can_send_video_notes=True,
                can_send_voice_notes=True,
                can_invite_users=True,
                can_send_polls=True,
                can_add_web_page_previews=True
            ),
            until_date=None
        )
        await message.answer(f"<b>{mention}</b> {MESSAGES['unmute'][language]}")


@rt.message(Command(commands=["ban"]))
async def mute_handler(message: Message, bot: Bot, command: CommandObject):
    chat_id = message.chat.id
    language = identify_language(chat_id)

    reply = message.reply_to_message
    if not reply:
        return await message.answer(f"Not found")

    mention = reply.from_user.mention_html(reply.from_user.first_name)

    chat_member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if chat_member.status not in ['administrator', 'creator']:
        return await message.answer(MESSAGES['admin_rights_prohibited'][language])

    if command.args:
        reason_filter = command.args.split(" ")
        reason = " ".join(reason_filter)
    else:
        reason_filter = []
        reason = ""

    with suppress(TelegramBadRequest):
        await bot.ban_chat_member(chat_id=chat_id, user_id=reply.from_user.id)
        if reason == "":
            await message.answer(f"<b>{mention}</b> {MESSAGES['banned_no_reason'][language]}!")
        else:
            await message.answer(f"<b>{mention}</b> {MESSAGES['banned'][language]} <b>{reason}</b>!")


@rt.message(Command(commands=["unban"]))
async def unban_handler(message: Message, bot: Bot) -> None:
    reply = message.reply_to_message
    mention = reply.from_user.mention_html(reply.from_user.first_name)
    language = identify_language(message.chat.id)
    chat_member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    suspect = await bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id)
    if chat_member.status in ['administrator', 'creator']:
        if not reply:
            await message.answer(f"Not found")
        elif suspect.status not in ['kicked']:
            await message.answer(f"{mention} {MESSAGES['unban_error'][language]}")
        else:
            with suppress(TelegramBadRequest):
                await bot.unban_chat_member(chat_id=message.chat.id, user_id=reply.from_user.id)
                await message.answer(f"{mention} {MESSAGES['unban'][language]}")
    else:
        await message.answer(MESSAGES['admin_rights_prohibited'][language])






#########################################################################################################


@rt.edited_message()
async def edited_banned_words_handler(message: Message, bot: Bot) -> None:
    text = message.text
    chat_member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    chat_id = message.chat.id
    until_date_words = datetime.datetime.now() + datetime.timedelta(minutes=2)
    until_date_links = datetime.datetime.now() + datetime.timedelta(minutes=5)
    language = identify_language(chat_id)
    if chat_member.status not in ['administrator', 'creator']:
        if triggers(text, language):
            await message.delete()
            with suppress(TelegramBadRequest):
                await bot.restrict_chat_member(
                    chat_id=message.chat.id,
                    user_id=message.from_user.id,
                    permissions=ChatPermissions(can_send_messages=False),
                    until_date=until_date_words
                )
                await message.answer(f"{message.from_user.mention_html(message.from_user.first_name)}, "
                                    f"{MESSAGES['anti_trigger'][language]}")

        if links_filter(text):
            await message.delete()
            with suppress(TelegramBadRequest):
                await bot.restrict_chat_member(
                    chat_id=message.chat.id,
                    user_id=message.from_user.id,
                    permissions=ChatPermissions(can_send_messages=False),
                    until_date=until_date_links
                )
                await message.answer(MESSAGES['anti_links'][language])


@rt.message()
async def banned_words_handler(message: Message, bot: Bot) -> None:
    chat_member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    language = identify_language(message.chat.id)
    text = message.text
    until_date_words = datetime.datetime.now() + datetime.timedelta(minutes=2)
    until_date_links = datetime.datetime.now() + datetime.timedelta(minutes=5)
    if chat_member.status not in ['administrator', 'creator']:
        if triggers(text, language):
            await message.delete()
            with suppress(TelegramBadRequest):
                await bot.restrict_chat_member(
                    chat_id=message.chat.id,
                    user_id=message.from_user.id,
                    permissions=ChatPermissions(can_send_messages=False),
                    until_date=until_date_words
                )
                await message.answer(f"{message.from_user.mention_html(message.from_user.first_name)}, "
                                    f"{MESSAGES['anti_trigger'][language]}")
        if links_filter(text):
            await message.delete()
            with suppress(TelegramBadRequest):
                await bot.restrict_chat_member(
                    chat_id=message.chat.id,
                    user_id=message.from_user.id,
                    permissions=ChatPermissions(can_send_messages=False),
                    until_date=until_date_links
                )
                await message.answer(MESSAGES['anti_links'][language])