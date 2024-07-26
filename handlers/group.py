import random

from aiogram import Router, Bot
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.types import ChatPermissions, CallbackQuery

from utils.utils import *
from database.queries import *
from utils.translation import *

from contextlib import suppress

from aiogram.exceptions import TelegramBadRequest
from keyboards import inline as il

from filters.filters import *

rt = Router()


@rt.message(IsGroupChat(), CommandStart())
async def command_start_handler(message: Message, bot: Bot) -> None:
    chat_id = message.chat.id
    insert_id(chat_id)
    chat_member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if chat_member.status in ['administrator', 'creator']:
        await message.answer(
            f"Hello, members of «<b>{message.chat.title}</b>» group\nChoose your language:\n\n"
            f"Приветствую всех участников чата «<b>{message.chat.title}</b>»\nВыбери свой язык:", reply_markup=il.languages_inline_buttons())
    else:
        await message.answer("Error: Access prohibited!")


@rt.message(IsGroupChat(), lambda message: message.text in ["Шидо расскажи историю", "Shido tell a story"])
async def dushnila_shido(message: Message):
    language = identify_language(message.chat.id)
    await message.answer(MESSAGES['dushnila'][language])


@rt.message(IsGroupChat(), lambda message: message.text in ["Шидо, расскажи историю", "Shido, tell a story"])
async def shido_tells_a_story(message: Message):
    language = identify_language(message.chat.id)
    if language == "eng":
        story = get_eng_story(random.choice(get_all_eng_stories_ids()))
        await message.answer(f"<b>{story[0]}</b>\n\n{story[1]}")
    elif language == "rus":
        story = get_rus_story(random.choice(get_all_rus_stories_ids()))
        await message.answer(f"<b>{story[0]}</b>\n\n{story[1]}")


@rt.message(IsGroupChat(), Command(commands=['language']))
async def set_bot_language(message: Message, bot: Bot) -> None:
    chat_id = message.chat.id
    insert_id(chat_id)
    chat_member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if chat_member.status not in ['administrator', 'creator']:
        await message.answer("Access prohibited")
    await message.answer(
        f"Hello, members of <b>{message.chat.title}</b> chat!\nChoose a language on which I will be operated.\n:)",
        reply_markup=il.languages_inline_buttons())


@rt.callback_query(CallGroupChat(), lambda callback: callback.data in ["rus", "eng"])
async def set_message(callback: CallbackQuery, bot: Bot):
    chat_id = callback.message.chat.id
    language = callback.data
    insert_language(language, chat_id)
    chat_id = callback.message.chat.id
    language = identify_language(chat_id)
    await callback.message.delete()
    await callback.message.answer_photo(caption=f"{MESSAGES['addition_to_a_group'][language]}", photo="AgACAgIAAxkBAAIBXmaiTfZIW5U0M7snAAELcJ0NgnDEFQACfuAxG6JcGUlTBQABnZ2SdzcBAAMCAAN5AAM1BA")
    await callback.message.answer(MESSAGES['welcome_message'][language])


@rt.message(IsGroupChat(), Command(commands=["mute"])) # TODO: fix
async def mute_handler(message: Message, bot: Bot, command: CommandObject):
    chat_id = message.chat.id
    language = identify_language(chat_id)
    chat_member = await bot.get_chat_member(message.chat.id, message.from_user.id)

    reply = message.reply_to_message
    if not reply:
        if chat_member.status not in ['administrator', 'creator']:
            return await message.answer(MESSAGES['admin_rights_prohibited'][language])
        else:
            return await message.answer(MESSAGES['reply_to_restrict'][language])

    until_date = time_converter(command.args)

    if chat_member.status not in ['administrator', 'creator']:
        return await message.answer(MESSAGES['admin_rights_prohibited'][language])

    if command.args:
        reason_filter = command.args.split(" ")
        reason = " ".join(reason_filter[1:])
    else:
        reason_filter = []
        reason = ""

    with suppress(TelegramBadRequest):
        await bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=reply.from_user.id,
            permissions=ChatPermissions(can_send_messages=False),
            until_date=until_date
        )
        if reason == "":
            await message.answer(f"🚫 <b>{reply.from_user.mention_html(reply.from_user.first_name)}</b> {MESSAGES['muted_no_reason'][language]}!")
        else:
            await message.answer(f"🚫 <b>{reply.from_user.mention_html(reply.from_user.first_name)}</b> {MESSAGES['muted'][language]} <b>{reason}</b>!")


#########################################################################################################
@rt.message(IsGroupChat(), Command(commands=["unmute"]))
async def mute_handler(message: Message, bot: Bot):
    chat_id = message.chat.id
    language = identify_language(chat_id)
    chat_member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    reply = message.reply_to_message

    if not reply:
        if chat_member.status in ['administrator', 'creator']:
            return await message.answer(MESSAGES['reply_to_restrict'][language])
        else:
            return await message.answer(MESSAGES['admin_rights_prohibited'][language])
    else:
        if chat_member.status in ['administrator', 'creator']:
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
                await message.answer(
                    f"😌 <b>{reply.from_user.mention_html(reply.from_user.first_name)}</b> {MESSAGES['unmute'][language]}")
        else:
            return await message.answer(MESSAGES['admin_rights_prohibited'][language])


@rt.message(IsGroupChat(), Command(commands=["ban"]))   # TODO: fix
async def mute_handler(message: Message, bot: Bot, command: CommandObject):
    chat_id = message.chat.id
    language = identify_language(chat_id)
    chat_member = await bot.get_chat_member(message.chat.id, message.from_user.id)

    reply = message.reply_to_message
    if not reply:
        if chat_member.status not in ['administrator', 'creator']:
            return await message.answer(MESSAGES['admin_rights_prohibited'][language])
        else:
            return await message.answer(MESSAGES['reply_to_restrict'][language])

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
            await message.answer(f"❌ <b>{reply.from_user.mention_html(reply.from_user.first_name)}</b> {MESSAGES['banned_no_reason'][language]}!")
        else:
            await message.answer(f"❌ <b>{reply.from_user.mention_html(reply.from_user.first_name)}</b> {MESSAGES['banned'][language]} <b>{reason}</b>!")


@rt.message(IsGroupChat(), Command(commands=["unban"]))  # TODO: fix
async def unban_handler(message: Message, bot: Bot) -> None:
    reply = message.reply_to_message
    language = identify_language(message.chat.id)
    chat_member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if not reply:
        if chat_member.status not in ['administrator', 'creator']:
            await message.answer(MESSAGES['admin_rights_prohibited'][language])
        else:
            await message.answer(MESSAGES['reply_to_restrict'][language])
    else:
        suspect = await bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id)
        if chat_member.status in ['administrator', 'creator']:
            if suspect.status not in ['kicked']:
                await message.answer(f"😳 {reply.from_user.mention_html(reply.from_user.first_name)} {MESSAGES['unban_error'][language]}")
            else:
                with suppress(TelegramBadRequest):
                    await bot.unban_chat_member(chat_id=message.chat.id, user_id=reply.from_user.id)
                    await message.answer(f"🔓 {reply.from_user.mention_html(reply.from_user.first_name)} {MESSAGES['unban'][language]}")
        else:
            await message.answer(MESSAGES['admin_rights_prohibited'][language])






#########################################################################################################


@rt.edited_message(IsGroupChat())
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
                await message.answer(f"🤬❌ {message.from_user.mention_html(message.from_user.first_name)}, "
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
                await message.answer(f"📣❌ {message.from_user.mention_html(message.from_user.first_name)}, "
                                     f"{MESSAGES['anti_links'][language]}")


@rt.message(IsGroupChat())
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
                await message.answer(f"🤬❌ {message.from_user.mention_html(message.from_user.first_name)}, "
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
                await message.answer(f"📣❌ {message.from_user.mention_html(message.from_user.first_name)}, "
                                     f"{MESSAGES['anti_links'][language]}")