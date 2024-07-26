from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from filters.filters import Admin

from FSM.states import *
from aiogram.fsm.context import FSMContext
from database.queries import *

from keyboards import keyboards as rp, inline as il

rt = Router()


@rt.message(Admin(), Command("creator"))
async def admin_panel(message: Message):
    await message.answer("ADMIN PANEL", reply_markup=rp.creator_keyboard())


@rt.message(Admin(), F.text == "⬅️")
async def admin_main_menu(message: Message):
    await message.answer("ADMIN PANEL", reply_markup=rp.creator_keyboard())


@rt.message(Admin(), F.text == "Send a message")
async def admin_message(message: Message, state: FSMContext):
    await state.set_state(Sending.message)
    await message.answer("Leave a message to everyone: ")


@rt.message(Admin(), Sending.message)
async def send_newsletter(message: Message, state: FSMContext) -> None:
    all_chats = get_all_chats()
    await message.answer("Your message is being processed...")
    for chat in all_chats:
        try:
            await message.send_copy(chat_id=chat)
        except:
            await message.answer("An error occurred!")
    await message.answer("The message has been sent to all successfully!")
    await state.clear()


@rt.message(Admin(), F.text == "Stories")
async def story_creation(message: Message) -> None:
    await message.answer("Language: ", reply_markup=rp.lang_stories_buttons())


@rt.message(Admin(), F.text == "🇬🇧")
async def story_eng(message: Message):
    await message.answer("All stories: ", reply_markup=rp.english_stories())


@rt.message(Admin(), F.text == "🇷🇺")
async def story_rus(message: Message):
    await message.answer("All stories: ", reply_markup=rp.russian_stories())


@rt.message(Admin(), F.text == "Add ➕")
async def add_eng_story(message: Message, state: FSMContext):
    await state.set_state(EngStoryCreation.title)
    await message.answer("START\nHeadline of the story?")


@rt.message(Admin(), EngStoryCreation.title)
async def add_rus_story(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(EngStoryCreation.text)
    await message.answer("Text of the story?")


@rt.message(Admin(), EngStoryCreation.text)
async def add_rus_story(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    data = await state.get_data()
    insert_eng_story(data['title'], data['text'])
    await state.clear()
    await message.answer("Completed and added!", reply_markup=rp.english_stories())


@rt.message(Admin(), F.text == "Добавить ➕")
async def add_eng_story(message: Message, state: FSMContext):
    await state.set_state(RusStoryCreation.title)
    await message.answer("START\nHeadline of the story?")


@rt.message(Admin(), RusStoryCreation.title)
async def add_rus_story(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(RusStoryCreation.text)
    await message.answer("Text of the story?")


@rt.message(Admin(), RusStoryCreation.text)
async def add_rus_story(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    data = await state.get_data()
    insert_rus_story(data['title'], data['text'])
    await state.clear()
    await message.answer("Completed and added!", reply_markup=rp.russian_stories())


@rt.message(Admin(), lambda message: message.text in get_all_eng_stories_titles())
async def delete_eng_story_func(message: Message):
    story = get_eng_story_del(message.text)
    await message.answer(f"<b>DESCRIPTION</b>\n\n{story[1]}")
    await message.answer(story[0], reply_markup=il.delete_eng)


@rt.message(Admin(), lambda message: message.text in get_all_rus_stories_titles())
async def delete_rus_story_func(message: Message):
    story = get_rus_story_del(message.text)
    await message.answer(f"<b>DESCRIPTION</b>\n\n{story[1]}")
    await message.answer(story[0], reply_markup=il.delete_rus)


@rt.callback_query(Admin(), F.data == "dele")
async def delete_story_en(callback: CallbackQuery):
    delete_eng_story(callback.message.text)
    await callback.message.delete()
    await callback.message.answer("Successfully deleted!", reply_markup=rp.english_stories())


@rt.callback_query(Admin(), F.data == "delr")
async def delete_story_ru(callback: CallbackQuery):
    delete_rus_story(callback.message.text)
    await callback.message.delete()
    await callback.message.answer("Successfully deleted!", reply_markup=rp.russian_stories())





