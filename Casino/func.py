import random
import time
from loader import bot, db
from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton


async def get_key(user_id):
    if db.get_lang(user_id) == 'ru':
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add('🎮 Играть')
        keyboard.add('🖥 Профиль', '📊 Статистика')
        keyboard.add('⚙️ Настройки')
        if db.get_group(user_id) > 0:
            keyboard.add('🤑 Меню воркера')
        if db.get_group(user_id) > 1:
            keyboard.add('🛠️ Меню админа')
        return keyboard
    elif db.get_lang(user_id) == 'eng':
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add('🎮 Play')
        keyboard.add('🖥 Profile', '📊 Statistics')
        keyboard.add('⚙️ Settings')
        if db.get_group(user_id) > 0:
            keyboard.add('🤑 Меню воркера')
        if db.get_group(user_id) > 1:
            keyboard.add('🛠️ Меню админа')
        return keyboard


async def profile(user_id):
    r = random.randint(350, 400)
    if db.get_lang(user_id) == 'ru':
        with open('img/profile.png', 'rb') as pic:
            await bot.send_photo(user_id, pic, f'<b>🖥 Личный кабинет | Верификация: {db.get_verif(user_id)}</b>\n\n'
                                               f'<b>💰 Баланс:</b> {db.get_balance(user_id)}{db.get_currency(user_id)}\n\n'
                                               f'<b>🟢 Игроков в сети:</b> {r}',
                                 reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                     [InlineKeyboardButton('📥 Пополнить', callback_data='top_up'),
                                      InlineKeyboardButton('📤 Вывести', callback_data='withdraw')],
                                     [InlineKeyboardButton('🤝 Партнерская программа', callback_data='ref_program')]
                                 ]))
    elif db.get_lang(user_id) == 'eng':
        with open('img/profile.png', 'rb') as pic:
            await bot.send_photo(user_id, pic, f'<b>🖥 Personal Area | Verification: {db.get_verif(user_id)}</b>\n\n'
                                               f'<b>💰 Balance:</b> {db.get_balance(user_id)}{db.get_currency(user_id)}\n\n'
                                               f'<b>🟢 Players online:</b> {r}',
                                 reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                     [InlineKeyboardButton('📥 Top Up', callback_data='top_up'),
                                      InlineKeyboardButton('📤 Withdraw', callback_data='withdraw')],
                                     [InlineKeyboardButton('🤝 Affiliate program', callback_data='ref_program')]
                                 ]))


async def timer(c: types.CallbackQuery, user_id):
    i = 0
    while i == 0:
        if db.get_lang(user_id) == 'ru':
            await bot.edit_message_text(chat_id=user_id, message_id=c.message.message_id,
                                        text='<b>⌛️ Ждём результаты.</b>')
            time.sleep(0.5)
            await bot.edit_message_text(chat_id=user_id, message_id=c.message.message_id,
                                        text='<b>⌛️ Ждём результаты..</b>')
            time.sleep(0.5)
            return await bot.edit_message_text(chat_id=user_id, message_id=c.message.message_id,
                                               text='<b>⌛️ Ждём результаты...</b>')
            i = 1
        elif db.get_lang(user_id) == 'eng':
            await bot.edit_message_text(chat_id=user_id, message_id=c.message.message_id,
                                        text='<b>⌛️ Waiting results.</b>')
            time.sleep(0.5)
            await bot.edit_message_text(chat_id=user_id, message_id=c.message.message_id,
                                        text='<b>⌛️ Waiting results..</b>')
            time.sleep(0.5)
            return await bot.edit_message_text(chat_id=user_id, message_id=c.message.message_id,
                                               text='<b>⌛️ Waiting results...</b>')
            i = 1
