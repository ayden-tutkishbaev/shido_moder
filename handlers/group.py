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
    insert_id_to_chat_permissions(chat_id)
    chat_member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if chat_member.status not in ['administrator', 'creator'] and not message.sender_chat:
        await message.answer("Error: Access prohibited!")
    else:
        await message.answer(
            f"Hello, members of «<b>{message.chat.title}</b>» group\nChoose your language:\n\n"
            f"Приветствую всех участников чата «<b>{message.chat.title}</b>»\nВыбери свой язык:",
            reply_markup=il.languages_inline_buttons())


@rt.message(IsGroupChat(), Command("links_on"))
async def permissions_menu(message: Message, bot: Bot):
    language = identify_language(message.chat.id)
    chat_member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if chat_member.status not in ['administrator', 'creator'] and not message.sender_chat:
        await message.answer(MESSAGES['admin_rights_prohibited'][language])
    else:
        on_lnks(message.chat.id)
        await message.answer(MESSAGES['links_on'][language])


@rt.message(IsGroupChat(), Command("links_off"))
async def permissions_menu(message: Message, bot: Bot):
    language = identify_language(message.chat.id)
    chat_member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if chat_member.status not in ['administrator', 'creator'] and not message.sender_chat:
        await message.answer(MESSAGES['admin_rights_prohibited'][language])
    else:
        off_lnks(message.chat.id)
        await message.answer(MESSAGES['links_off'][language])


@rt.message(IsGroupChat(), Command("swears_on"))
async def permissions_menu(message: Message, bot: Bot):
    language = identify_language(message.chat.id)
    chat_member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if chat_member.status not in ['administrator', 'creator'] and not message.sender_chat:
        await message.answer(MESSAGES['admin_rights_prohibited'][language])
    else:
        on_swears(message.chat.id)
        await message.answer(MESSAGES['strong_language_on'][language])


@rt.message(IsGroupChat(), Command("swears_off"))
async def permissions_menu(message: Message, bot: Bot):
    language = identify_language(message.chat.id)
    chat_member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if chat_member.status not in ['administrator', 'creator'] and not message.sender_chat:
        await message.answer(MESSAGES['admin_rights_prohibited'][language])
    else:
        off_swears(message.chat.id)
        await message.answer(MESSAGES['strong_language_off'][language])


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
    if chat_member.status not in ['administrator', 'creator'] and not message.sender_chat:
        await message.answer("Error: Access prohibited!")
    else:
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
    await callback.message.answer(f"{MESSAGES['addition_to_a_group'][language]}")
    await callback.message.answer(MESSAGES['welcome_message'][language])


@rt.message(IsGroupChat(), Command(commands=["mute"])) # TODO: fix
async def mute_handler(message: Message, bot: Bot, command: CommandObject):
    chat_id = message.chat.id
    language = identify_language(chat_id)
    chat_member = await bot.get_chat_member(message.chat.id, message.from_user.id)

    reply = message.reply_to_message
    if not reply:
        if chat_member.status not in ['administrator', 'creator'] and not message.sender_chat:
            return await message.answer(MESSAGES['admin_rights_prohibited'][language])
        else:
            return await message.answer(MESSAGES['reply_to_restrict'][language])

    until_date = time_converter(command.args)

    if chat_member.status not in ['administrator', 'creator'] and not message.sender_chat:
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

    if chat_member.status not in ['administrator', 'creator'] and not message.sender_chat:
        await message.answer(MESSAGES['admin_rights_prohibited'][language])
    else:
        if not reply:
            return await message.answer(MESSAGES['reply_to_restrict'][language])
        else:
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


@rt.message(IsGroupChat(), Command(commands=["ban"]))   # TODO: fix
async def mute_handler(message: Message, bot: Bot, command: CommandObject):
    chat_id = message.chat.id
    language = identify_language(chat_id)
    chat_member = await bot.get_chat_member(message.chat.id, message.from_user.id)

    reply = message.reply_to_message
    if not reply:
        if chat_member.status not in ['administrator', 'creator'] and not message.sender_chat:
            return await message.answer(MESSAGES['admin_rights_prohibited'][language])
        else:
            return await message.answer(MESSAGES['reply_to_restrict'][language])

    if chat_member.status not in ['administrator', 'creator'] and not message.sender_chat:
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


@rt.message(IsGroupChat(), Command(commands=["unban"]))
async def unban_handler(message: Message, bot: Bot) -> None:
    reply = message.reply_to_message
    language = identify_language(message.chat.id)
    chat_member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if chat_member.status not in ['administrator', 'creator'] and not message.sender_chat:
        await message.answer(MESSAGES['admin_rights_prohibited'][language])
    else:
        if not reply:
            await message.answer(MESSAGES['reply_to_restrict'][language])
        else:
            suspect = await bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id)
            if suspect.status not in ['kicked']:
                await message.answer(f"😳 {reply.from_user.mention_html(reply.from_user.first_name)} {MESSAGES['unban_error'][language]}")
            else:
                with suppress(TelegramBadRequest):
                    await bot.unban_chat_member(chat_id=message.chat.id, user_id=reply.from_user.id)
                    await message.answer(
                        f"🔓 {reply.from_user.mention_html(reply.from_user.first_name)} {MESSAGES['unban'][language]}")


@rt.message(IsGroupChat(), Command("sleep"))
async def curfew(message: Message, bot: Bot):
    language_code = identify_language(message.chat.id)
    member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    member_permissions = ChatPermissions(
        can_send_messages=False,
        can_send_photos=False,
        can_send_videos=False,
        can_send_documents=False,
        can_send_other_messages=False,
        can_send_audios=False,
        can_send_video_notes=False,
        can_send_voice_notes=False,
        can_invite_users=False,
        can_send_polls=False,
        can_add_web_page_previews=False
    )
    if member.status not in ['administrator', 'creator'] and not message.sender_chat:
        await message.reply(MESSAGES['admin_rights_prohibited'][language_code])
    else:
        with suppress(TelegramBadRequest):
            await bot.set_chat_permissions(chat_id=message.chat.id, permissions=member_permissions)
            await message.answer(MESSAGES['curfew_on'][language_code])


@rt.message(IsGroupChat(), Command("wakeup"))
async def wake_up(message: Message, bot: Bot):
    language_code = identify_language(message.chat.id)
    member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    member_permissions = ChatPermissions(
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
    )
    if member.status not in ['administrator', 'creator'] and not message.sender_chat:
        await message.reply(MESSAGES['admin_rights_prohibited'][language_code])
    else:
        with suppress(TelegramBadRequest):
            await bot.set_chat_permissions(chat_id=message.chat.id, permissions=member_permissions)
            await message.answer(MESSAGES['curfew_off'][language_code])


#########################################################################################################


@rt.edited_message(IsGroupChat())
async def edited_banned_words_handler(message: Message, bot: Bot) -> None:
    text = message.text
    chat_member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    chat_id = message.chat.id
    until_date_banned_words = datetime.datetime.now() + datetime.timedelta(minutes=3)
    until_date_swear_words = datetime.datetime.now() + datetime.timedelta(minutes=2)
    until_date_links = datetime.datetime.now() + datetime.timedelta(minutes=5)
    language = identify_language(chat_id)
    permits = get_chat_permissions(chat_id)
    if chat_member.status not in ['administrator', 'creator'] and not message.sender_chat:
        if banned_words(text, language):
            await message.delete()
            with suppress(TelegramBadRequest):
                await bot.restrict_chat_member(
                    chat_id=message.chat.id,
                    user_id=message.from_user.id,
                    permissions=ChatPermissions(can_send_messages=False),
                    until_date=until_date_banned_words
                )
                await message.answer(f"🤬❌ {message.from_user.mention_html(message.from_user.full_name)}, "
                                     f"{MESSAGES['anti_ban_words'][language]}")
        if for_gamerland(text):
            # if message.chat.id == -1001444716528:
            if message.chat.id == -1002192805825:
                await message.delete()
                with suppress(TelegramBadRequest):
                    await bot.restrict_chat_member(
                        chat_id=message.chat.id,
                        user_id=message.from_user.id,
                        permissions=ChatPermissions(can_send_messages=False),
                        until_date=until_date_banned_words
                    )
                    await message.answer(
                        f"❌ {message.from_user.mention_html(message.from_user.full_name)} <i>был заглушен на 3 минуты! Причина: <b>администраторы запретили упоминание данной личности!</b></i>")
        if triggers(text, language):
            if not permits[0]:
                await message.delete()
                with suppress(TelegramBadRequest):
                    await bot.restrict_chat_member(
                        chat_id=message.chat.id,
                        user_id=message.from_user.id,
                        permissions=ChatPermissions(can_send_messages=False),
                        until_date=until_date_swear_words
                    )
                    await message.answer(f"🤬❌ {message.from_user.mention_html(message.from_user.full_name)}, "
                                        f"{MESSAGES['anti_trigger'][language]}")
        if links_filter(text):
            if not permits[1]:
                await message.delete()
                with suppress(TelegramBadRequest):
                    await bot.restrict_chat_member(
                        chat_id=message.chat.id,
                        user_id=message.from_user.id,
                        permissions=ChatPermissions(can_send_messages=False),
                        until_date=until_date_links
                    )
                    await message.answer(f"📣❌ {message.from_user.mention_html(message.from_user.full_name)} {MESSAGES['anti_links'][language]}")


@rt.message(IsGroupChat())
async def banned_words_handler(message: Message, bot: Bot) -> None:
    chat_member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    language = identify_language(message.chat.id)
    text = message.text
    until_date_banned_words = datetime.datetime.now() + datetime.timedelta(minutes=3)
    until_date_swear_words = datetime.datetime.now() + datetime.timedelta(minutes=2)
    until_date_links = datetime.datetime.now() + datetime.timedelta(minutes=5)
    permits = get_chat_permissions(message.chat.id)
    if chat_member.status not in ['administrator', 'creator'] and not message.sender_chat:
        if banned_words(text, language):
            await message.delete()
            with suppress(TelegramBadRequest):
                await bot.restrict_chat_member(
                    chat_id=message.chat.id,
                    user_id=message.from_user.id,
                    permissions=ChatPermissions(can_send_messages=False),
                    until_date=until_date_banned_words
                )
                await message.answer(f"🤬❌ {message.from_user.mention_html(message.from_user.full_name)}"
                                     f"{MESSAGES['anti_ban_words'][language]}")
        if for_gamerland(text):
            # if message.chat.id == -1001444716528:
            if message.chat.id == -1002192805825:
                await message.delete()
                with suppress(TelegramBadRequest):
                    await bot.restrict_chat_member(
                        chat_id=message.chat.id,
                        user_id=message.from_user.id,
                        permissions=ChatPermissions(can_send_messages=False),
                        until_date=until_date_banned_words
                    )
                    await message.answer(f"❌ {message.from_user.mention_html(message.from_user.full_name)} <i>был заглушен на 3 минуты! Причина: <b>администраторы запретили упоминание данной личности!</b></i>")
        if triggers(text, language):
            if not permits[0]:
                await message.delete()
                with suppress(TelegramBadRequest):
                    await bot.restrict_chat_member(
                        chat_id=message.chat.id,
                        user_id=message.from_user.id,
                        permissions=ChatPermissions(can_send_messages=False),
                        until_date=until_date_swear_words
                    )
                    await message.answer(f"🤬❌ {message.from_user.mention_html(message.from_user.full_name)}, "
                                        f"{MESSAGES['anti_trigger'][language]}")
        if links_filter(text):
            if not permits[1]:
                await message.delete()
                with suppress(TelegramBadRequest):
                    await bot.restrict_chat_member(
                        chat_id=message.chat.id,
                        user_id=message.from_user.id,
                        permissions=ChatPermissions(can_send_messages=False),
                        until_date=until_date_links
                    )
                    await message.answer(f"📣❌ {message.from_user.mention_html(message.from_user.full_name)} {MESSAGES['anti_links'][language]}")