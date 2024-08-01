from aiogram.fsm.state import State, StatesGroup


class Sending(StatesGroup):
    message = State()


class EngStoryCreation(StatesGroup):
    title = State()
    text = State()


class RusStoryCreation(StatesGroup):
    title = State()
    text = State()


class BugReport(StatesGroup):
    message = State()


class AnswerMessage(StatesGroup):
    to = State()
    message = State()