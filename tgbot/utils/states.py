from aiogram.dispatcher.filters.state import StatesGroup, State


class NewChannel(StatesGroup):
    URL = State()
    AddBotToAdmin = State()
    GEO = State()
    BaseFormat = State()
    BasePrice = State()
    HoldPrice = State()
    Discount = State()
    Preview = State()
    AddNewChannel = State()
