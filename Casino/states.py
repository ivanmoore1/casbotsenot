from aiogram.dispatcher.filters.state import State, StatesGroup


class TopUp(StatesGroup):
    value = State()


class Withdraw(StatesGroup):
    value = State()


class Post(StatesGroup):
    text = State()


class ChangeBalance(StatesGroup):
    balance = State()


class WorkPost(StatesGroup):
    text = State()


class ChangeCard(StatesGroup):
    card = State()


class MoreLess(StatesGroup):
    bet = State()


class ChangeMinDep(StatesGroup):
    dep = State()
