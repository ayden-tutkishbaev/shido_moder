# @rt.message(IsGroupChat(), Command(commands=["ban"]))   # TODO: fix
# async def mute_handler(message: Message, bot: Bot, command: CommandObject):
#     chat_id = message.chat.id
#     language = identify_language(chat_id)
#     chat_member = await bot.get_chat_member(message.chat.id, message.from_user.id)
#
#     reply = message.reply_to_message
#     if not reply:
#         if chat_member.status not in ['administrator', 'creator'] and not message.sender_chat:
#             return await message.answer(MESSAGES['admin_rights_prohibited'][language])
#         else:
#             return await message.answer(MESSAGES['reply_to_restrict'][language])
#
#     if chat_member.status not in ['administrator', 'creator'] and not message.sender_chat:
#         return await message.answer(MESSAGES['admin_rights_prohibited'][language])
#
#     if command.args:
#         reason_filter = command.args.split(" ")
#         reason = " ".join(reason_filter)
#     else:
#         reason_filter = []
#         reason = ""
#
#     with suppress(TelegramBadRequest):
#         await bot.ban_chat_member(chat_id=chat_id, user_id=reply.from_user.id)
#         if reason == "":
#             await message.answer(f"❌ <b>{reply.from_user.mention_html(reply.from_user.first_name)}</b> {MESSAGES['banned_no_reason'][language]}!")
#         else:
#             await message.answer(f"❌ <b>{reply.from_user.mention_html(reply.from_user.first_name)}</b> {MESSAGES['banned'][language]} <b>{reason}</b>!")







# @rt.message(IsGroupChat(), Command(commands=["unban"]))  # TODO: fix
# async def unban_handler(message: Message, bot: Bot) -> None:
#     reply = message.reply_to_message
#     language = identify_language(message.chat.id)
#     chat_member = await bot.get_chat_member(message.chat.id, message.from_user.id)
#     if chat_member.status not in ['administrator', 'creator'] and not message.sender_chat:
#         await message.answer(MESSAGES['admin_rights_prohibited'][language])
#     else:
#         if not reply:
#             await message.answer(MESSAGES['reply_to_restrict'][language])
#         else:
#             suspect = await bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id)
#             if suspect.status not in ['kicked']:
#                 await message.answer(f"😳 {reply.from_user.mention_html(reply.from_user.first_name)} {MESSAGES['unban_error'][language]}")
#             else:
#                 with suppress(TelegramBadRequest):
#                     await bot.unban_chat_member(chat_id=message.chat.id, user_id=reply.from_user.id)
#                     await message.answer(
#                         f"🔓 {reply.from_user.mention_html(reply.from_user.first_name)} {MESSAGES['unban'][language]}")


