from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from sql import Database

storage = MemoryStorage()
bot = Bot('5485341881:AAG4G7eF8Joete3ceT6LnwMUFT5Kdt1AnSU', parse_mode='HTML')
dp = Dispatcher(bot, storage=storage)
db = Database('db.db')

admin = 5128725679
tech_support = 'Dragonmoney_support'
payments = -1001540021719
