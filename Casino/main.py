# -*- coding: utf-8 -*-
import logging
import states
import time
import more_less
from datetime import datetime
from converter import conveyor, conveyor2
from AntiSpam import test
from loader import bot, dp, db, admin, payments, tech_support
from func import profile, get_key
from aiogram import types, executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext

logging.basicConfig(level=logging.INFO)


# ******************_START_******************
@dp.message_handler(commands=['start'])
async def start(m: types.Message):
    user_id = m.from_user.id
    if db.user_exists(user_id) is False:
        who_invite = m.text
        if len(who_invite) != 6:
            try:
                ref = int(who_invite[7:])
                boss = ref
                if db.get_group(ref) > 0:
                    await bot.send_message(ref,
                                           f'🐘️ <b>У тебя новый мамонт - <a href="tg://user?id={user_id}">{m.from_user.first_name}</a></b>\n')
            except:
                boss = 0
        else:
            boss = 0
        reg_date = time.strftime('%d/%m/%Y %H:%M:%S')
        login = '0'
        if m.from_user.username is None:
            login = 'None'
        else:
            login = m.from_user.username
        db.add_user(user_id, login, m.from_user.first_name, m.from_user.last_name, boss, reg_date)
        await bot.send_message(user_id, '<b>🌐 Выберите язык (Choose language):</b>',
                               reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                   [InlineKeyboardButton('🇷🇺 Русский', callback_data=f'lang=^{user_id}^ru'),
                                    InlineKeyboardButton('🇬🇧 English', callback_data=f'lang=^{user_id}^eng')]
                               ]))
    else:
        if db.get_lang(user_id) == '0':
            await bot.send_message(user_id, '<b>🌐 Выберите язык (Choose language):</b>',
                                   reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                       [InlineKeyboardButton('🇷🇺 Русский', callback_data=f'lang=^{user_id}^ru'),
                                        InlineKeyboardButton('🇬🇧 English', callback_data=f'lang=^{user_id}^eng')]
                                   ]))
        elif db.get_lang(user_id) == 'ru':
            await bot.send_message(user_id, '<b>Добро пожаловать!</b>', reply_markup=await get_key(user_id))
            await profile(user_id)
        elif db.get_lang(user_id) == 'eng':
            await bot.send_message(user_id, '<b>Welcome!</b>', reply_markup=await get_key(user_id))
            await profile(user_id)


@dp.callback_query_handler(lambda call: call.data.startswith('lang='))
async def lang(c: types.CallbackQuery):
    user_id = c.from_user.id
    new_lang = c.data.replace('lang=', '').split('^')
    if new_lang[2] == 'ru':
        db.set_lang(user_id, 'ru')
    else:
        db.set_lang(user_id, 'eng')
    if db.get_lang(user_id) == 'ru':
        await bot.edit_message_text(chat_id=user_id, message_id=c.message.message_id,
                                    text=f'<b>🎉 Привет, {c.from_user.first_name}!</b>\n\n'
                                         f'<b>Политика и условия пользования данным ботом:</b>\n'
                                         f'<i>1. Играя у нас, вы берёте все риски за свои средства на себя.</i>\n'
                                         f'<i>2. Принимая правила, Вы подтверждаете своё совершеннолетие!</i>\n'
                                         f'<i>3. Ваш аккаунт может быть забанен в подозрении на мошенничество/обман нашей системы!</i>\n'
                                         f'<i>4. Мультиаккаунты запрещены!</i>\n'
                                         f'<i>5. Скрипты, схемы использовать запрещено!</i>\n'
                                         f'<i>6. Для оформления вывода средств, сумма вашего выигрыша должна быть в 5 раз больше суммы пополнения!\n</i>'
                                         f'<i>7. Если будут выявлены вышеперчисленные случаи, Ваш аккаунт будет заморожен до выяснения обстоятельств!\n</i>'
                                         f'Ваша задача - угадать, в каком диапазоне будет располагаться выпадшее число.\n'
                                         f'От 0 до 50, либо от 50 до 100, в таком случае Вы получаете удвоение суммы ставки, либо же если Ваше число будет равно 50, то тогда Вы получаете выигрыш равный 5 Вашим ставкам. Но вероятность выпадения данного числа намного ниже.\n',
                                    reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                        [InlineKeyboardButton('✅ Принять', callback_data='accept')]
                                    ]))
    elif db.get_lang(user_id) == 'eng':
        await bot.edit_message_text(chat_id=user_id, message_id=c.message.message_id,
                                    text=f'<b>🎉 Hi, {c.from_user.first_name}!</b>\n\n'
                                         f'<b>Bot data use policy and terms:</b>\n'
                                         f'<i>1. By playing with us, you take all the risks for your funds.</i>\n'
                                         f'<i>2. By accepting the rules, you confirm that you are of legal age!</i>\n'
                                         f'<i>3. Your account may be banned in suspicion of fraud/cheating our system!</i>\n'
                                         f'<i>4. Multi-accounts are prohibited!</i>\n'
                                         f'<i>5. Scripts, schemes are prohibited!</i>\n'
                                         f'<i>6. To process the withdrawal of funds, the amount of your winnings must be 5 times the amount of replenishment!\n</i>'
                                         f'<i>7. If the above cases are detected, your account will be frozen until the circumstances are clarified!\n</i>'
                                         f'<i>8. If necessary, the administration has the right to ask you for documents confirming your identity and your age.\n\n</i>'
                                         f'Your task is to guess in which range the dropped number will be located\n'
                                         f'From 0 to 50, or from 50 to 100, in which case you get a doubling of the bet amount, or if your number is equal to 50, then you get a win equal to 5 of your bets. But the probability of getting this number is much lower.\n',
                                    reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                        [InlineKeyboardButton('✅ Accept', callback_data='accept')]
                                    ]))


@dp.callback_query_handler(lambda call: call.data == 'accept')
async def accept(c: types.CallbackQuery):
    user_id = c.from_user.id
    await bot.delete_message(chat_id=user_id, message_id=c.message.message_id)
    if db.get_lang(user_id) == 'ru':
        await bot.send_message(user_id, '<b>❗️ Выберите валюту:</b>',
                               reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                    [InlineKeyboardButton('🇷🇺 RUB ₽', callback_data=f'set_currency=^{user_id}^₽'),
                                    InlineKeyboardButton('🇺🇦 UAH ₴', callback_data=f'set_currency=^{user_id}^₴'),
                                    InlineKeyboardButton('🇪🇺 EUR €', callback_data=f'set_currency=^{user_id}^€')]
                               ]))
    elif db.get_lang(user_id) == 'eng':
        await bot.send_message(user_id, '<b>❗️ Select currency:</b>',
                               reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                    [InlineKeyboardButton('🇷🇺 RUB ₽', callback_data=f'set_currency=^{user_id}^₽'),
                                    InlineKeyboardButton('🇺🇦 UAH ₴', callback_data=f'set_currency=^{user_id}^₴'),
                                    InlineKeyboardButton('🇪🇺 EUR €', callback_data=f'set_currency=^{user_id}^€')]
                               ]))


@dp.callback_query_handler(lambda call: call.data == 'cancel', state='*')
async def cancel(c: types.CallbackQuery, state=FSMContext):
    user_id = c.from_user.id
    await bot.delete_message(chat_id=user_id, message_id=c.message.message_id)
    await state.finish()
    await profile(user_id)


@dp.callback_query_handler(lambda call: call.data == 'cancel_admin', state='*')
async def cancel_admin(c: types.CallbackQuery, state=FSMContext):
    user_id = c.from_user.id
    await bot.delete_message(chat_id=user_id, message_id=c.message.message_id)
    await state.finish()
    await bot.send_message(user_id, f'<b>💎️ Админ Панель</b>\n\n'
                                    f'<b>👤 Пользователей в боте -</b> {len(db.get_all())}\n'
                                    f'<b>🤑 Воркеров -</b> {len(db.get_workers())}',
                           reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                               [InlineKeyboardButton('🔎 Найти мамонта', switch_inline_query_current_chat='u=')],
                               [InlineKeyboardButton('✉️ Рассылка', callback_data='post')],
                               [InlineKeyboardButton('💳 Карты', callback_data='cards')]
                           ]))


@dp.callback_query_handler(lambda call: call.data == 'change_cur')
async def change_cur(c: types.CallbackQuery):
    user_id = c.from_user.id
    if db.get_lang(user_id) == 'ru':
        await bot.edit_message_text(chat_id=user_id, message_id=c.message.message_id,
                                    text='<b>👉 Выберите валюту:</b>',
                                    reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                        [InlineKeyboardButton('🇷🇺 RUB ₽',
                                                              callback_data=f'set_currency=^{user_id}^₽'),
                                        InlineKeyboardButton('🇺🇦 UAH ₴',
                                                              callback_data=f'set_currency=^{user_id}^₴'),
                                        InlineKeyboardButton('🇪🇺 EUR €',
                                                              callback_data=f'set_currency=^{user_id}^€')]
                                    ]))
    elif db.get_lang(user_id) == 'eng':
        await bot.edit_message_text(chat_id=user_id, message_id=c.message.message_id, text='<b>❗️ Select currency:</b>',
                                    reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                        [InlineKeyboardButton('🇺🇦 UAH ₴',
                                                              callback_data=f'set_currency=^{user_id}^₴'),
                                        InlineKeyboardButton('🇪🇺 EUR €', callback_data=f'set_currency=^{user_id}^€')]
                                    ]))
    else:
        await bot.edit_message_text(chat_id=user_id, message_id=c.message.message_id, text='<b>❗️ Select currency:</b>',
                                    reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                        [InlineKeyboardButton('🇺🇦 UAH ₴',
                                                              callback_data=f'set_currency=^{user_id}^₴'),
                                        InlineKeyboardButton('🇪🇺 EUR €', callback_data=f'set_currency=^{user_id}^€')]
                                    ]))


@dp.callback_query_handler(lambda call: call.data == 'change_lang')
async def change_cur(c: types.CallbackQuery):
    user_id = c.from_user.id
    if db.get_lang(user_id) == 'eng':
        await bot.edit_message_text(chat_id=user_id, message_id=c.message.message_id, text='<b>🌐 Choose language:</b>',
                                    reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                        [InlineKeyboardButton('🇷🇺 Русский', callback_data='set_lang=ru'),
                                         InlineKeyboardButton('🇬🇧 English', callback_data='set_lang=eng')]
                                    ]))
    elif db.get_lang(user_id) == 'ru':
        await bot.edit_message_text(chat_id=user_id, message_id=c.message.message_id, text='<b>🌐 Выберите язык:</b>',
                                    reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                        [InlineKeyboardButton('🇷🇺 Русский', callback_data='set_lang=ru'),
                                         InlineKeyboardButton('🇬🇧 English', callback_data='set_lang=eng')]
                                    ]))


@dp.callback_query_handler(lambda call: call.data.startswith('set_lang='))
async def set_lang(c: types.CallbackQuery):
    user_id = c.from_user.id
    new_lang = c.data.replace('set_lang=', '').split('^')
    db.set_lang(user_id, new_lang[0])
    await bot.delete_message(chat_id=user_id, message_id=c.message.message_id)
    if db.get_lang(user_id) == 'ru':
        await bot.send_message(user_id, '<b>✅ Язык установлен!</b>', reply_markup=await get_key(user_id))

    elif db.get_lang(user_id) == 'eng':
        await bot.send_message(user_id, '<b>✅ Language set!</b>', reply_markup=await get_key(user_id))
    await profile(user_id)


@dp.callback_query_handler(lambda call: call.data == 'top_up')
async def top_up(c: types.CallbackQuery):
    user_id = c.from_user.id
    if db.get_lang(user_id) == 'ru':
        await bot.edit_message_caption(chat_id=user_id, message_id=c.message.message_id,
                                       caption=f'<b>✍️ Введите сумму пополнения:</b>\n'
                                               f'<i>⚠️ Минимальная сумма пополнения {db.get_min(user_id)}{db.get_currency(user_id)}</i>',
                                       reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                           [InlineKeyboardButton('◀️ Отмена', callback_data='cancel')]
                                       ]))
        await states.TopUp.value.set()

    elif db.get_lang(user_id) == 'eng':
        await bot.edit_message_caption(chat_id=user_id, message_id=c.message.message_id,
                                       caption=f'<b>✍️ Enter replenishment amount:</b>\n'
                                               f'<i>⚠️ Minimum deposit amount {db.get_min(user_id)}{db.get_currency(user_id)}</i>',
                                       reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                           [InlineKeyboardButton('◀️ Cancel', callback_data='cancel')]
                                       ]))
        await states.TopUp.value.set()


@dp.message_handler(content_types='text', state=states.TopUp.value)
async def top_up2(m: types.Message, state=FSMContext):
    user_id = m.from_user.id
    async with state.proxy() as data:
        data['answer'] = m.text
        answers = data['answer']
        if answers.isdigit() and int(answers) != 0 and int(answers) >= db.get_min(user_id):
            topup_card = 0
            if db.get_currency(user_id) == '₽':
                topup_card = db.get_card('RUB')
            elif db.get_currency(user_id) == '₴':
                topup_card = db.get_card('UAH')
            elif db.get_currency(user_id) == '€':
                topup_card = db.get_card('EUR')

            if db.get_lang(user_id) == 'ru':
                with open('img/popolnenieRU.png', 'rb') as pic:
                    await bot.send_photo(user_id, pic, f'<b>📥 Пополнение баланса</b>\n\n'
                                                       f'<b>💰 Сумма:</b> {answers}{db.get_currency(user_id)}\n\n'
                                                       f'<b>💳 Реквизиты:</b>\n'
                                                       f'<code>{topup_card}</code>\n\n'
                                                       f'<b>💬 Комментарий:</b>\n'
                                                       f'<code>DRAGON-MONEY:{m.from_user.id}</code>\n\n'
                                                       f'<i>⚠️Если Вы не можете указать комментарий, отправьте чек/скриншот перевода в Тех. Поддержку.</i>\n'
                                                       f'<i>Средства зачисляются автоматически в течении 5 минут после совершения перевода.</i>',
                                         reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                             [InlineKeyboardButton('🧑‍💻 Тех. Поддержка', url=f't.me/{tech_support}')]
                                         ]))
            elif db.get_lang(user_id) == 'eng':
                with open('img/popolnenieEU.png', 'rb') as pic:
                    await bot.send_photo(user_id, pic, f'<b>📥 Balance replenishment</b>\n\n'
                                                       f'<b>💰 Sum:</b> {answers}{db.get_currency(user_id)}\n\n'
                                                       f'<b>💳 Requisites:</b>\n'
                                                       f'<code>{topup_card}</code>\n\n'
                                                       f'<b>💬 Comment:</b>\n'
                                                       f'<code>DRAGON-MONEY:{m.from_user.id}</code>\n\n'
                                                       f'<i>⚠ ️If you are unable to provide a comment, please send a check/screenshot of the translation to Tech. Support.</i>\n'
                                                       f'<i>Funds are credited automatically within 5 minutes after the transfer.</i>',
                                         reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                             [InlineKeyboardButton('🧑‍💻 Tech. Support', url=f't.me/{tech_support}')]
                                         ]))

            try:
                ref_id = db.get_id(db.get_ref(user_id))
                ref_name = db.get_name(ref_id)
            except:
                ref_id = 0
                ref_name = '-'

            await bot.send_message(admin,
                                   f'<b>💳 Попытка пополнения от</b> <a href="tg://user?id={user_id}">{m.from_user.first_name}</a>\n\n'
                                   f'<b>🤝 Реферал:</b> <a href="tg://user?id={ref_id}">{ref_name}</a>\n'
                                   f'<b>💰 Сумма:</b> {answers}{db.get_currency(user_id)}',
                                   reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                       [InlineKeyboardButton('🔸 85%',
                                                             callback_data=f'payday={answers}^{db.get_currency(user_id)}^{ref_id}^85%'),
                                        InlineKeyboardButton('🔸 80%',
                                                             callback_data=f'payday={answers}^{db.get_currency(user_id)}^{ref_id}^80%')],
                                       [InlineKeyboardButton('🔸 75%',
                                                             callback_data=f'payday={answers}^{db.get_currency(user_id)}^{ref_id}^75%'),
                                        InlineKeyboardButton('🔸 70%',
                                                             callback_data=f'payday={answers}^{db.get_currency(user_id)}^{ref_id}^70%')],
                                        [InlineKeyboardButton('🔸 65%',
                                                             callback_data=f'payday={answers}^{db.get_currency(user_id)}^{ref_id}^65%')],
                                       [InlineKeyboardButton('❌ Закрыть', callback_data='cancel')]
                                   ]))

            if db.get_ref(user_id) == 0 or db.get_group(db.get_ref(user_id)) == 0:
                await state.finish()
            else:
                await bot.send_message(db.get_ref(user_id),
                                       f'<b>💳 Попытка пополнения от</b> <a href="tg://user?id={user_id}">{m.from_user.first_name}</a>\n\n'
                                       f'<b>💰 Сумма:</b> {answers}{db.get_currency(user_id)}\n\n'
                                       f'<b>⚡️ Заряд на залёт</b>', reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                        [InlineKeyboardButton('📥 Пополнить', callback_data=f'accept_top_up=^{user_id}^{answers}')]
                    ]))
                await state.finish()
        else:
            if db.get_lang(user_id) == 'ru':
                await bot.send_message(user_id, '<b>❗️ Сумма должна быть целым числом, повторите попытку!</b>',
                                       reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                           [InlineKeyboardButton('🔙 Отмена', callback_data='cancel')]
                                       ]))
            elif db.get_lang(user_id) == 'eng':
                await bot.send_message(user_id, '<b>❗️ Amount must be an integer, please try again!</b>',
                                       reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                           [InlineKeyboardButton('🔙 Cancel', callback_data='cancel')]
                                       ]))


@dp.callback_query_handler(lambda call: call.data.startswith('accept_top_up='))
async def accept_top_up(c: types.CallbackQuery):
    user_id = c.from_user.id
    value = c.data.replace('accept_top_up=', '').split('^')
    try:
        db.set_balance(value[1], round(db.get_balance(value[1]) + int(value[2])))
        await bot.edit_message_text(chat_id=user_id, message_id=c.message.message_id,
                                    text=f'<b>✅ Баланс успешно пополнен -</b> <a href="tg://user?id={value[1]}">{db.get_name(value[1])}</a>\n'
                                         f'<b>💰 На сумму:</b> {value[2]}{db.get_currency(value[1])}',
                                    reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                        [InlineKeyboardButton(f'◀️ В меню мамонта {db.get_name(value[1])}',
                                                              callback_data=f'i={value[1]}')]
                                    ]))
        if db.get_lang(value[1]) == 'ru':
            await bot.send_message(value[1], f'<b>📥 Ваш баланс пополнен на {value[2]}{db.get_currency(value[1])}!</b>')
        elif db.get_lang(value[1]) == 'eng':
            await bot.send_message(value[1],
                                   f'<b>📥 Your balance has been replenished with {value[2]}{db.get_currency(value[1])}!</b>')
    except:
        await c.answer(text='❌ Ошибка')


@dp.callback_query_handler(lambda call: call.data.startswith('payday='))
async def payday(c: types.CallbackQuery):
    profit = c.data.replace('payday=', '').split('^')
    print(profit)
    try:
        ref = db.get_username(profit[2])
    except:
        ref = 'none'


    if profit[3] == '85%':
        money = float(profit[0]) * 0.85
        await bot.send_message(payments, f'<b>💞 НОВЫЙ ПРОФИТ!  ⏳</b>\n'
                                         f'<b>⚡️ Сервис:</b> Казино\n'
                                         f'<b>💸 Залетело:</b> {profit[0]}{profit[1]}\n'
                                         f'<b>🤝 Доля воркера:</b> {money}{profit[1]} [85%]\n'
                                         f'<b>🥷 Воркер:</b> <a href="https://t.me/{ref}">{ref}</a>',disable_web_page_preview = True)

    elif profit[3] == '75%':
        money = float(profit[0])* 0.75
        await bot.send_message(payments, f'<b>💞 НОВЫЙ ПРОФИТ!  ⏳</b>\n'
                                         f'<b>⚡️ Сервис:</b> Казино\n'
                                         f'<b>💸 Залетело:</b> {profit[0]}{profit[1]}\n'
                                         f'<b>🤝 Доля воркера:</b> {money}{profit[1]} [75%]\n'
                                         f'<b>🥷 Воркер:</b> <a href="https://t.me/{ref}">{ref}</a>',disable_web_page_preview = True)

    elif profit[3] == '70%':
        money = float(profit[0]) * 0.7
        await bot.send_message(payments, f'<b>💞 НОВЫЙ ПРОФИТ!  ⏳</b>\n'
                                         f'<b>⚡️ Сервис:</b> Казино\n'
                                         f'<b>💸 Залетело:</b> {profit[0]}{profit[1]}\n'
                                         f'<b>🤝 Доля воркера:</b> {money}{profit[1]} [70%]\n'
                                         f'<b>🥷 Воркер:</b> <a href="https://t.me/{ref}">{ref}</a>',disable_web_page_preview = True)

    elif profit[3] == '80%':
        money = float(profit[0]) * 0.8
        await bot.send_message(payments, f'<b>💞 НОВЫЙ ПРОФИТ!  ⏳</b>\n'
                                         f'<b>⚡️ Сервис:</b> Казино\n'
                                         f'<b>💸 Залетело:</b> {profit[0]}{profit[1]}\n'
                                         f'<b>🤝 Доля воркера:</b> {money}{profit[1]} [80%]\n'
                                         f'<b>🥷 Воркер:</b> <a href="https://t.me/{ref}">{ref}</a>',disable_web_page_preview = True)
    elif profit[3] == '65%':
        money = float(profit[0]) * 0.65
        await bot.send_message(payments, f'<b>💞 НОВЫЙ ПРОФИТ!  ⏳</b>\n'
                                         f'<b>⚡️ Сервис:</b> Казино\n'
                                         f'<b>💸 Залетело:</b> {profit[0]}{profit[1]}\n'
                                         f'<b>🤝 Доля воркера:</b> {money}{profit[1]} [65%]\n'
                                         f'<b>🥷 Воркер:</b> <a href="https://t.me/{ref}">{ref}</a>',disable_web_page_preview = True)

    if ref == 0:
        return
    current = '0'
    if profit[1] == '₴':
        current = 'UAH'
    elif profit[1] == '€':
        current = 'EUR'
    elif profit[1] == '₽':
        current = 'RUB'
    value = conveyor2(float(profit[0]), current, 'RUB')
    db.set_profit(profit[2], round(db.get_profit(profit[2]) + value))


@dp.callback_query_handler(lambda call: call.data == 'withdraw')
async def withdraw(c: types.CallbackQuery):
    user_id = c.from_user.id
    if db.get_status(user_id) == 3:
        if db.get_lang(user_id) == 'ru':
            return await bot.send_message(user_id, '<b>🚫 На Ваш аккаунт введены ограничения!</b>\n\n'
                                                   '<b>❗️ Для того чтобы снять ограничения Вам необходимо пройти верификацию!</b>')
        elif db.get_lang(user_id) == 'eng':
            return await bot.send_message(user_id, '<b>🚫 Your account has been restricted!</b>\n\n'
                                                   '<b>❗️ In order to remove restrictions, you need to pass verification!</b>')
    if db.get_lang(user_id) == 'ru':
        await bot.edit_message_caption(chat_id=user_id, message_id=c.message.message_id,
                                       caption=f'<b>💰 Ваш баланс:</b> {db.get_balance(user_id)}{db.get_currency(user_id)}\n'
                                               f'<b>✍️ Введите сумму вывода:</b>',
                                       reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                           [InlineKeyboardButton('◀️ Отмена', callback_data='cancel')]
                                       ]))
        await states.Withdraw.value.set()
    elif db.get_lang(user_id) == 'eng':
        await bot.edit_message_caption(chat_id=user_id, message_id=c.message.message_id,
                                       caption=f'<b>💰 Your balance:</b> {db.get_balance(user_id)}{db.get_currency(user_id)}\n'
                                               f'<b>✍️ Enter withdrawal amount:</b>',
                                       reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                           [InlineKeyboardButton('◀️ Cancel', callback_data='cancel')]
                                       ]))
        await states.Withdraw.value.set()


@dp.message_handler(content_types='text', state=states.Withdraw.value)
async def withdraw2(m: types.Message, state=FSMContext):
    user_id = m.from_user.id
    async with state.proxy() as data:
        data['answer'] = m.text
        answers = data['answer']
        if answers.isdigit() and int(answers) != 0 and db.get_balance(user_id) >= int(answers):
            if db.get_lang(user_id) == 'ru':
                await bot.send_message(user_id, f'<b>Вывод на банковсвкую карту</b>\n\n'
                                                f'<i>⚠️ Вывод возможен только на реквизиты, с которых пополнялся Ваш баланс в последний раз!</i>\n\n'
                                                f'<b>❗️ Подтвердить?</b>',
                                       reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                           [InlineKeyboardButton('Да',
                                                                 callback_data=f'accept_withdraw={answers}'),
                                            InlineKeyboardButton('Нет', callback_data='cancel')]
                                       ]))
                await state.finish()
            elif db.get_lang(user_id) == 'eng':
                await bot.send_message(user_id, f'<b>Withdrawal to a bank card</b>\n\n'
                                                f'<i>⚠️ Withdrawal is possible only to the details from which your balance was replenished last time!</i>\n\n'
                                                f'<b>❗️ Confirm?</b>',
                                       reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                           [InlineKeyboardButton('Yes',
                                                                 callback_data=f'accept_withdraw={answers}'),
                                            InlineKeyboardButton('No', callback_data='cancel')]
                                       ]))
                await state.finish()
        else:
            if db.get_lang(user_id) == 'ru':
                await bot.send_message(user_id, '<b>❗️ На Вашем счёту недостаточно средств, повторите попытку!</b>',
                                       reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                           [InlineKeyboardButton('◀️ Отмена', callback_data='cancel')]
                                       ]))
            elif db.get_lang(user_id) == 'eng':
                await bot.send_message(user_id,
                                       '<b>❗️ There are not enough funds on your account, please try again!</b>',
                                       reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                           [InlineKeyboardButton('◀️ Cancel', callback_data='cancel')]
                                       ]))


@dp.callback_query_handler(lambda call: call.data.startswith('accept_withdraw='))
async def withdraw3(c: types.CallbackQuery):
    user_id = c.from_user.id
    item = c.data.replace('accept_withdraw=', '')
    db.set_balance(user_id, round(db.get_balance(user_id) - int(item)))
    await bot.delete_message(chat_id=user_id, message_id=c.message.message_id)
    if db.get_lang(user_id) == 'ru':
        await bot.send_message(user_id, '<b>✅ Заявка на вывод успешно создана!\n\n⌛️ Ожидайте...</b>')
    elif db.get_lang(user_id) == 'eng':
        await bot.send_message(user_id, '<b>✅ Withdrawal request successfully created!\n\n⌛️ Expect...</b>')
    if db.get_ref(user_id) == 0:
        return await bot.send_message(admin,
                                      f'<b>🐘 Мамонт <a href="tg://user?id={user_id}">{db.get_name(user_id)}</a> создал запрос на вывод!</b>\n\n'
                                      f'<b>💰 Сумма вывода:</b> {item}{db.get_currency(user_id)}',
                                      reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                          [InlineKeyboardButton('✅ Вывести',
                                                                callback_data=f'accept_withdraw2=^{user_id}^{item}'),
                                           InlineKeyboardButton('❌ Отказ',
                                                                callback_data=f'decline_withdraw=^{user_id}^{item}')]
                                      ]))
    if db.get_group(db.get_ref(user_id)) > 0:
        await bot.send_message(db.get_ref(user_id),
                               f'<b>🐘 Мамонт <a href="tg://user?id={user_id}">{db.get_name(user_id)}</a> создал запрос на вывод!</b>\n\n'
                               f'<b>💰 Сумма вывода:</b> {item}{db.get_currency(user_id)}',
                               reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                   [InlineKeyboardButton('✅ Вывести',
                                                         callback_data=f'accept_withdraw2=^{user_id}^{item}'),
                                    InlineKeyboardButton('❌ Отказ',
                                                         callback_data=f'decline_withdraw=^{user_id}^{item}')]
                               ]))


@dp.callback_query_handler(lambda call: call.data.startswith('accept_withdraw2='))
async def accept_withdraw(c: types.CallbackQuery):
    user_id = c.from_user.id
    item = c.data.replace('accept_withdraw2=', '').split('^')
    await bot.edit_message_text(chat_id=user_id, message_id=c.message.message_id,
                                text=f'<b>🐘 Мамонт <a href="tg://user?id={item[1]}">{db.get_name(item[1])}</a> создал запрос на вывод!</b>\n\n'
                                     f'<b>💰 Сумма вывода:</b> {item[2]}{db.get_currency(item[1])}\n'
                                     f'<b>➖ Выведено ➖</b>')
    if db.get_lang(item[1]) == 'ru':
        await bot.send_message(item[1],
                               '<b>✅ Заявка на вывод одобрена!\n\nСредства поступят на Ваш счёт в течении 15 минут.</b>')
    elif db.get_lang(item[1]) == 'eng':
        await bot.send_message(item[1],
                               '<b>✅ Withdrawal request approved!\n\nFunds will be credited to your account within 15 minutes.</b>')


@dp.callback_query_handler(lambda call: call.data.startswith('decline_withdraw='))
async def accept_withdraw(c: types.CallbackQuery):
    user_id = c.from_user.id
    item = c.data.replace('accept_withdraw2=', '').split('^')
    db.set_balance(item[1], round(db.get_balance(item[1]) + int(item[2])))
    await bot.edit_message_text(chat_id=user_id, message_id=c.message.message_id,
                                text=f'<b>🐘 Мамонт <a href="tg://user?id={item[1]}">{db.get_name(item[1])}</a> создал запрос на вывод!</b>\n\n'
                                     f'<b>💰 Сумма вывода:</b> {item[2]}{db.get_currency(item[1])}\n'
                                     f'<b>➖ Отказано ➖</b>')
    if db.get_lang(item[1]) == 'ru':
        await bot.send_message(item[1],
                               '<b>⚠️ Заявка на вывод отклонена!\n\nПросим вас обратиться в Тех. Поддержку!</b>',
                               reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                   [InlineKeyboardButton('🧑‍💻 Тех. Поддержка', url=f't.me/{tech_support}')]
                               ]))
    elif db.get_lang(item[1]) == 'eng':
        await bot.send_message(item[1],
                               '<b>⚠️ Withdrawal request rejected!\n\nPlease contact Tech. Support!</b>',
                               reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                   [InlineKeyboardButton('🧑‍💻 Tech. Support', url=f't.me/{tech_support}')]
                               ]))


@dp.callback_query_handler(lambda call: call.data.startswith('set_currency='))
async def set_currency(c: types.CallbackQuery):
    user_id = c.from_user.id
    element = c.data.replace('set_currency=', '').split('^')
    if element[2] == '₽':
        db.set_min(element[1], 1500)
    elif element[2] == '₴':
        db.set_min(element[1], 500)
    elif element[2] == 'Br':
        db.set_min(element[1], 50)
    else:
        db.set_min(element[1], 30)
    conveyor(user_id, element, db.get_balance(user_id))
    await bot.delete_message(chat_id=user_id, message_id=c.message.message_id)
    if db.get_lang(user_id) == 'ru':
        await bot.send_message(user_id, '<b>✅ Валюта установлена!</b>', reply_markup=await get_key(user_id))

    elif db.get_lang(user_id) == 'eng':
        await bot.send_message(user_id, '<b>✅ Currency set!</b>', reply_markup=await get_key(user_id))
    await profile(user_id)


@dp.callback_query_handler(lambda call: call.data == 'ref_program')
async def ref_program(c: types.CallbackQuery):
    user_id = c.from_user.id
    bot_me = await bot.get_me()
    if db.get_lang(user_id) == 'ru':
        await bot.edit_message_caption(chat_id=user_id, message_id=c.message.message_id,
                                       caption=f'<b>🤝 Реферальная программа</b>\n\n'
                                               f'<b>👤 За каждого реферала который пополнит баланс, Вы получаете 3% от суммы его пополнения.</b>\n\n'
                                               f'<b>🔗 Ваша пригласительная ссылка:</b>\n'
                                               f'https://t.me/{bot_me.username}?start={user_id}\n\n'
                                               f'<b>👥 Вы пригласили -</b> {len(db.get_refs(user_id))} чел.',
                                       reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                           [InlineKeyboardButton('◀️ Назад', callback_data='cancel')]
                                       ]))
    elif db.get_lang(user_id) == 'eng':
        await bot.edit_message_caption(chat_id=user_id, message_id=c.message.message_id,
                                       caption=f'<b>🤝 Affiliate program</b>\n\n'
                                               f'<b>👤 For each referral who replenishes the balance, you receive 3% of the amount of its replenishment.</b>\n\n'
                                               f'<b>🔗 Your invite link:</b>\n'
                                               f'https://t.me/{bot_me.username}?start={user_id}\n\n'
                                               f'<b>👥 You invited -</b> {len(db.get_refs(user_id))} peo.',
                                       reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                           [InlineKeyboardButton('◀️ Back', callback_data='cancel')]
                                       ]))


@dp.callback_query_handler(lambda call: call.data == 'post')
async def post(c: types.CallbackQuery):
    user_id = c.from_user.id
    await states.Post.text.set()
    await bot.edit_message_text(chat_id=user_id, message_id=c.message.message_id,
                                text='<b>✍️ Введите текст для рассылки:</b>',
                                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                    [InlineKeyboardButton('◀️ Назад', callback_data='cancel_admin')]
                                ]))


@dp.message_handler(content_types='text', state=states.Post.text)
async def post2(m: types.Message, state=FSMContext):
    user_id = m.from_user.id
    async with state.proxy() as data:
        data['answers'] = m.text
        global text
        text = data['answers']
        await bot.send_message(user_id, f'<b>✉️ Начать рассылку?</b>\n\n'
                                        f'<b>Текст:</b>\n'
                                        f'{text}', reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton('✅ Да', callback_data=f'start_post'),
             InlineKeyboardButton('❌ Нет', callback_data='cancel_admin')]
        ]))
        await state.finish()


@dp.callback_query_handler(lambda call: call.data == 'start_post')
async def start_post(c: types.CallbackQuery):
    user_id = c.from_user.id
    users = db.get_all()
    success = 0
    error = 0
    for user in users:
        try:
            await bot.send_message(user[0], text)
            success += 1
        except:
            error += 1
            pass
    await bot.send_message(user_id, f'<b>✉️ Рассылка завершена!</b>\n'
                                    f'<b>✅ Успешно:</b> {success}\n'
                                    f'<b>❌ Заблокировано:</b> {error}')


@dp.callback_query_handler(lambda c: c.data.startswith('set_balance='))
async def set_balance(c: types.CallbackQuery):
    user_id = c.from_user.id
    if db.get_group(user_id) < 1:
        return
    global element
    element = c.data.replace('set_balance=', '')
    if db.user_exists(element) is None or (db.get_group(user_id) == 1 and db.get_ref(element) != user_id):
        return
    if c.inline_message_id is not None:
        await states.ChangeBalance.balance.set()
        await bot.edit_message_text(f'<b>✍️ Введите сумму, которая будет установлена на баланс мамонта:</b>',
                                    inline_message_id=c.inline_message_id,
                                    reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                        [InlineKeyboardButton('◀️ Назад', callback_data=f'i={element}')]
                                    ]))
    else:
        await states.ChangeBalance.balance.set()
        await bot.edit_message_text(f'<b>✍️ Введите сумму, которая будет установлена на баланс мамонта:</b>',
                                    chat_id=c.message.chat.id,
                                    message_id=c.message.message_id,
                                    reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                        [InlineKeyboardButton('◀️ Назад', callback_data=f'i={element}')]
                                    ]))


@dp.message_handler(content_types='text', state=states.ChangeBalance.balance)
async def set_balance2(m: types.Message, state=FSMContext):
    user_id = m.from_user.id
    async with state.proxy() as data:
        data['answers'] = m.text
        balance = data['answers']
        if not balance.isdigit():
            return await bot.send_message(user_id, '<b>❌ Вы ввели некорректное число!</b>')
        try:
            db.set_balance(element, round(int(balance)))
            await bot.send_message(user_id, '<b>✅ Вы успешно изменили баланс мамонта!</b>')
        except:
            await bot.send_message(user_id, 'Ошибка')
            await state.finish()


@dp.callback_query_handler(lambda c: c.data.startswith('set_min_dep='))
async def set_balance(c: types.CallbackQuery):
    user_id = c.from_user.id
    if db.get_group(user_id) < 1:
        return
    global element66
    element66 = c.data.replace('set_min_dep=', '')
    if db.user_exists(element66) is None or (db.get_group(user_id) == 1 and db.get_ref(element66) != user_id):
        return
    if c.inline_message_id is not None:
        await states.ChangeMinDep.dep.set()
        await bot.edit_message_text(f'<b>✍️ Введите сумму, которая будет установлена на минимальный депозит:</b>',
                                    inline_message_id=c.inline_message_id,
                                    reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                        [InlineKeyboardButton('◀️ Назад', callback_data=f'i={element66}')]
                                    ]))
    else:
        await states.ChangeMinDep.dep.set()
        await bot.edit_message_text(f'<b>✍️ Введите сумму, которая будет установлена на минимальный депозит:</b>',
                                    chat_id=c.message.chat.id,
                                    message_id=c.message.message_id,
                                    reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                        [InlineKeyboardButton('◀️ Назад', callback_data=f'i={element66}')]
                                    ]))


@dp.message_handler(content_types='text', state=states.ChangeMinDep.dep)
async def set_balance2(m: types.Message, state=FSMContext):
    user_id = m.from_user.id
    async with state.proxy() as data:
        data['answers'] = m.text
        dep = data['answers']
        if not dep.isdigit():
            return await bot.send_message(user_id, '<b>❌ Вы ввели некорректное число!</b>')
        try:
            db.set_min(element66, int(dep))
            await bot.send_message(user_id, '<b>✅ Вы успешно изменили минимальную сумму депозита!</b>')
            await state.finish()
        except:
            await bot.send_message(user_id, 'Ошибка')
            await state.finish()


@dp.callback_query_handler(lambda call: call.data.startswith('set_status='))
async def set_status(c: types.CallbackQuery):
    user_id = c.from_user.id
    element3 = c.data.replace('set_status=', '')
    new_status = 0
    if db.get_status(element3) == 0:
        new_status = 1
        db.set_status(element3, new_status)
        await c.answer(text='❕ Статус был изменён на "Проигрыш"')
    elif db.get_status(element3) == 1:
        new_status = 2
        db.set_status(element3, new_status)
        await c.answer(text='❕ Статус был изменён на "Рандом"')
    elif db.get_status(element3) == 2:
        new_status = 3
        db.set_status(element3, new_status)
        await c.answer(text='❕ Статус был изменён на "Верификация"')
    elif db.get_status(element3) == 3:
        new_status = 0
        db.set_status(element3, new_status)
        await c.answer(text='❕ Статус был изменён на "Победа"')
    keyboard = [
        [InlineKeyboardButton('✉️ Отправить сообщение', callback_data=f'send_message={element3}')],
        [InlineKeyboardButton('💰 Изменить баланс', callback_data=f'set_balance={element3}'),
         InlineKeyboardButton('🔖 Изменить статус', callback_data=f'set_status={element3}')],
        [InlineKeyboardButton('📥 Изменить мин. сумму депозита', callback_data=f'set_min_dep={element3}')],
        [InlineKeyboardButton('🔃 Обновить', callback_data=f'i={element3}')],
    ]
    group = 'Мамонт'
    if db.get_group(element3) == 1:
        group = 'Воркер'
    elif db.get_group(element3) == 2:
        group = 'Администратор'

    status = 'Победа'
    if db.get_status(element3) == 1:
        status = 'Проигрыш'
    elif db.get_status(element3) == 2:
        status = 'Рандом'
    elif db.get_status(element3) == 3:
        status = 'Верификация'
    ref = f''
    if db.get_ref(element3) != 0:
        ref_db = db.get_ref(element3)
        if ref_db is not None:
            ref = f'<b>🤝 Приглашён:</b> <a href="tg://user?id={db.get_id(ref_db)}">{db.get_name(ref_db)}</a>'
    if db.get_group(user_id) == 1:
        try:
            if c.inline_message_id is not None:
                await bot.edit_message_text(
                    f'<b>👤 Имя:</b> <a href="tg://user?id={db.get_id(element3)}">{db.get_name(element3)}</a>\n'
                    f'<b>💰 Баланс:</b> {db.get_balance(element3)}{db.get_currency(element3)}\n'
                    f'<b>📥 Мин. сумма депозита:</b> {db.get_min(element3)}{db.get_currency(element3)}\n'
                    f'<b>👥 Рефералов:</b> {len(db.get_refs(element3))}\n'
                    f'<b>🔖 Статус:</b> {status}\n',
                    reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard),
                    inline_message_id=c.inline_message_id)
            else:
                await bot.edit_message_text(
                    f'<b>👤 Имя:</b> <a href="tg://user?id={db.get_id(element3)}">{db.get_name(element3)}</a>\n'
                    f'<b>💰 Баланс:</b> {db.get_balance(element3)}{db.get_currency(element3)}\n'
                    f'<b>📥 Мин. сумма депозита:</b> {db.get_min(element3)}{db.get_currency(element3)}\n'
                    f'<b>👥 Рефералов:</b> {len(db.get_refs(element3))}\n'
                    f'<b>🔖 Статус:</b> {status}\n',
                    reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard),
                    chat_id=c.message.chat.id,
                    message_id=c.message.message_id)
        except Exception as e:
            await c.answer(text='❕ Обновлений профиля не было найдено')
    elif db.get_group(user_id) == 2:
        keyboard.append(
            [InlineKeyboardButton('👤 Изменить группу', callback_data=f'set_group={db.get_id(element3)}'),
             InlineKeyboardButton('✅ Верифицировать', callback_data=f'verification={db.get_id(element3)}')])
        try:
            if c.inline_message_id is not None:
                return await bot.edit_message_text(
                    f'<b>👤 Имя:</b> <a href="tg://user?id={db.get_id(element3)}">{db.get_name(element3)}</a>\n'
                    f'<b>🔒 Верификация:</b> {db.get_verif(element3)}\n'
                    f'<b>💰 Баланс:</b> {db.get_balance(element3)}{db.get_currency(element3)}\n'
                    f'<b>📥 Мин. сумма депозита:</b> {db.get_min(element3)}{db.get_currency(element3)}\n'
                    f'<b>👥 Рефералов:</b> {len(db.get_refs(element3))}\n'
                    f'<b>🔖 Статус:</b> {status}\n'
                    f'<b>💸 Профитов:</b> {db.get_profit(element3)}₽\n'
                    f'<b>🆔 Группа:</b> {group}\n'
                    f'{ref if db.get_ref(element3) != 0 else f""}',
                    reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard),
                    inline_message_id=c.inline_message_id)
            else:
                await bot.edit_message_text(
                    f'<b>👤 Имя:</b> <a href="tg://user?id={db.get_id(element3)}">{db.get_name(element3)}</a>\n'
                    f'<b>🔒 Верификация:</b> {db.get_verif(element3)}\n'
                    f'<b>💰 Баланс:</b> {db.get_balance(element3)}{db.get_currency(element3)}\n'
                    f'<b>📥 Мин. сумма депозита:</b> {db.get_min(element3)}{db.get_currency(element3)}\n'
                    f'<b>👥 Рефералов:</b> {len(db.get_refs(element3))}\n'
                    f'<b>🔖 Статус:</b> {status}\n'
                    f'<b>💸 Профитов:</b> {db.get_profit(element3)}₽\n'
                    f'<b>🆔 Группа:</b> {group}\n'
                    f'{ref if db.get_ref(element3) != 0 else f""}',
                    reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard),
                    chat_id=c.message.chat.id,
                    message_id=c.message.message_id)
        except Exception as e:
            await c.answer(text='❕ Обновлений профиля не было найдено')


@dp.callback_query_handler(lambda call: call.data.startswith('set_group='))
async def set_status(c: types.CallbackQuery):
    user_id = c.from_user.id
    element3 = c.data.replace('set_group=', '')
    group_id = db.get_group(element3)
    new_group = 0
    if group_id == 0:
        new_group = 1
    elif group_id == 1:
        new_group = 0
    db.set_group(element3, new_group)
    keyboard = [
        [InlineKeyboardButton('✉️ Отправить сообщение', callback_data=f'send_message={element3}')],
        [InlineKeyboardButton('💰 Изменить баланс', callback_data=f'set_balance={element3}'),
         InlineKeyboardButton('🔖 Изменить статус', callback_data=f'set_status={element3}')],
        [InlineKeyboardButton('📥 Изменить мин. сумму депозита', callback_data=f'set_min_dep={element3}')],
        [InlineKeyboardButton('🔃 Обновить', callback_data=f'i={element3}')],
    ]
    group = 'Мамонт'
    if db.get_group(element3) == 1:
        group = 'Воркер'
    elif db.get_group(element3) == 2:
        group = 'Администратор'

    status = 'Победа'
    if db.get_status(element3) == 1:
        status = 'Проигрыш'
    elif db.get_status(element3) == 2:
        status = 'Рандом'
    elif db.get_status(element3) == 3:
        status = 'Верификация'
    ref = f''
    if db.get_ref(element3) != 0:
        ref_db = db.get_ref(element3)
        if ref_db is not None:
            ref = f'<b>🤝 Приглашён:</b> <a href="tg://user?id={db.get_id(ref_db)}">{db.get_name(ref_db)}</a>'
    if db.get_group(user_id) == 1:
        try:
            if c.inline_message_id is not None:
                await bot.edit_message_text(
                    f'<b>👤 Имя:</b> <a href="tg://user?id={db.get_id(element3)}">{db.get_name(element3)}</a>\n'
                    f'<b>💰 Баланс:</b> {db.get_balance(element3)}{db.get_currency(element3)}\n'
                    f'<b>📥 Мин. сумма депозита:</b> {db.get_min(element3)}{db.get_currency(element3)}\n'
                    f'<b>👥 Рефералов:</b> {len(db.get_refs(element3))}\n'
                    f'<b>🔖 Статус:</b> {status}\n',
                    reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard),
                    inline_message_id=c.inline_message_id)
            else:
                await bot.edit_message_text(
                    f'<b>👤 Имя:</b> <a href="tg://user?id={db.get_id(element3)}">{db.get_name(element3)}</a>\n'
                    f'<b>💰 Баланс:</b> {db.get_balance(element3)}{db.get_currency(element3)}\n'
                    f'<b>📥 Мин. сумма депозита:</b> {db.get_min(element3)}{db.get_currency(element3)}\n'
                    f'<b>👥 Рефералов:</b> {len(db.get_refs(element3))}\n'
                    f'<b>🔖 Статус:</b> {status}\n',
                    reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard),
                    chat_id=c.message.chat.id,
                    message_id=c.message.message_id)
        except Exception as e:
            await c.answer(text='❕ Обновлений профиля не было найдено')
    elif db.get_group(user_id) == 2:
        keyboard.append(
            [InlineKeyboardButton('👤 Изменить группу', callback_data=f'set_group={db.get_id(element3)}'),
             InlineKeyboardButton('✅ Верифицировать', callback_data=f'verification={db.get_id(element3)}')])
        try:
            if c.inline_message_id is not None:
                return await bot.edit_message_text(
                    f'<b>👤 Имя:</b> <a href="tg://user?id={db.get_id(element3)}">{db.get_name(element3)}</a>\n'
                    f'<b>🔒 Верификация:</b> {db.get_verif(element3)}\n'
                    f'<b>💰 Баланс:</b> {db.get_balance(element3)}{db.get_currency(element3)}\n'
                    f'<b>📥 Мин. сумма депозита:</b> {db.get_min(element3)}{db.get_currency(element3)}\n'
                    f'<b>👥 Рефералов:</b> {len(db.get_refs(element3))}\n'
                    f'<b>🔖 Статус:</b> {status}\n'
                    f'<b>💸 Профитов:</b> {db.get_profit(element3)}₽\n'
                    f'<b>🆔 Группа:</b> {group}\n'
                    f'{ref if db.get_ref(element3) != 0 else f""}',
                    reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard),
                    inline_message_id=c.inline_message_id)
            else:
                await bot.edit_message_text(
                    f'<b>👤 Имя:</b> <a href="tg://user?id={db.get_id(element3)}">{db.get_name(element3)}</a>\n'
                    f'<b>🔒 Верификация:</b> {db.get_verif(element3)}\n'
                    f'<b>💰 Баланс:</b> {db.get_balance(element3)}{db.get_currency(element3)}\n'
                    f'<b>📥 Мин. сумма депозита:</b> {db.get_min(element3)}{db.get_currency(element3)}\n'
                    f'<b>👥 Рефералов:</b> {len(db.get_refs(element3))}\n'
                    f'<b>🔖 Статус:</b> {status}\n'
                    f'<b>💸 Профитов:</b> {db.get_profit(element3)}₽\n'
                    f'<b>🆔 Группа:</b> {group}\n'
                    f'{ref if db.get_ref(element3) != 0 else f""}',
                    reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard),
                    chat_id=c.message.chat.id,
                    message_id=c.message.message_id)
        except Exception as e:
            await c.answer(text='❕ Обновлений профиля не было найдено')


@dp.callback_query_handler(lambda call: call.data.startswith('send_message='))
async def send_message(c: types.CallbackQuery):
    user_id = c.from_user.id
    if db.get_group(user_id) < 1:
        return
    global text_element
    text_element = c.data.replace('send_message=', '')
    if db.user_exists(text_element) is None or (db.get_group(user_id) == 1 and db.get_ref(text_element) != user_id):
        return
    if c.inline_message_id is not None:
        await states.WorkPost.text.set()
        await bot.edit_message_text(
            f'<b>✍️ Введите сообщение, которое будет отправлено <a href="tg://user?id={text_element}">{db.get_name(text_element)}</a>:</b>',
            inline_message_id=c.inline_message_id,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton('◀️ Назад', callback_data=f'i={text_element}')]
            ]))
    else:
        await states.WorkPost.text.set()
        await bot.edit_message_text(
            f'<b>✍️ Введите сообщение, которое будет отправлено <a href="tg://user?id={text_element}">{db.get_name(text_element)}</a>:</b>',
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton('◀️ Назад', callback_data=f'i={text_element}')]
            ]))


@dp.message_handler(content_types='text', state=states.WorkPost.text)
async def set_balance2(m: types.Message, state=FSMContext):
    user_id = m.from_user.id
    async with state.proxy() as data:
        data['answers'] = m.text
        text = data['answers']
        try:
            await bot.send_message(text_element, text)
            await bot.send_message(user_id, '<b>✅ Сообщение успешно доставлено!</b>')
            await bot.send_message(admin, f'<b>Было отправлено смс!</b>\n\n'
                                          f'От <a href="tg://user?={user_id}">{m.from_user.first_name}</a> к <a href="tg://user?id={db.get_id(text_element)}">{db.get_name(text_element)}</a>\n'
                                          f'{text}')
            await state.finish()
        except:
            await bot.send_message(user_id, 'Ошибка')
            await state.finish()
@dp.callback_query_handler(lambda call: call.data == 'cards')
async def cards(c: types.CallbackQuery):
    user_id = c.from_user.id
    await bot.edit_message_text(chat_id=user_id, message_id=c.message.message_id, text=f'<b>💳 Карты:</b>\n\n'
                                                                                       f'<b>🇺🇦 UAH:</b> {db.get_card("UAH")}\n'
                                                                                       f'<b>🇷🇺 RUB:</b> {db.get_card("RUB")}\n'
                                                                                       f'<b>🇪🇺 EUR:</b> {db.get_card("EUR")}',
                                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                    [InlineKeyboardButton('🇺🇦 Сменить UAH', callback_data='change_card=UAH'),
                                     InlineKeyboardButton('🇷🇺 Сменить RUB', callback_data='change_card=RUB')],
                                    [InlineKeyboardButton('🇪🇺 Сменить EUR', callback_data='change_card=EUR')],
                                    [InlineKeyboardButton('◀️ Назад', callback_data='cancel_admin')]
                                ]))


@dp.callback_query_handler(lambda call: call.data.startswith('change_card='))
async def change_card(c: types.CallbackQuery):
    user_id = c.from_user.id
    global card
    card = c.data.replace('change_card=', '')
    await states.ChangeCard.card.set()
    await bot.edit_message_text(chat_id=user_id, message_id=c.message.message_id,
                                text='Введи новую карту:\n\n<code>Пополнение с помощью Тех. Поддержки</code>',
                                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                    [InlineKeyboardButton('◀️ Назад', callback_data='cancel_admin')]
                                ]))


@dp.message_handler(content_types='text', state=states.ChangeCard.card)
async def change_card2(m: types.Message, state=FSMContext):
    user_id = m.from_user.id
    async with state.proxy() as data:
        data['answers'] = m.text
        new_card = data['answers']
        db.set_card(card, new_card)
        await bot.send_message(user_id, 'успешно')
        await state.finish()


@dp.callback_query_handler(lambda c: c.data == 'info')
async def info(c: types.CallbackQuery):
    user_id = c.from_user.id
    await bot.edit_message_caption(chat_id=user_id, message_id=c.message.message_id, caption='<a href="t.me/scmxx"><b>🥷ТС</b></a>\n'
                                                                                             '<a href="https://t.me/+BL_MyR7sBkU3M2My"><b>💸 Канал выплат</b></a>\n'
                                                                                             '<a href="https://t.me/+Yb6gr4QwZc5iZjcy"><b>📚 Канал с мануалами</b></a>\n'
                                                                                             '<a href="https://t.me/+QE3662zQu7tjZjJi"><b>🚀 Чат воркеров</b></a>\n'
                                                                                             '<a href="https://telegra.ph/Pravila-PLAYBOY-MANSION-09-04"><b>🔰 Правила проекта</b></a>',
                                   reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                       [InlineKeyboardButton('◀️ Назад', callback_data='back_work')]
                                   ]))


@dp.callback_query_handler(lambda c: c.data == 'back_work')
async def back_work(c: types.CallbackQuery):
    user_id = c.from_user.id
    bot_me = await bot.get_me()
    group = 'Мамонт'
    if db.get_group(user_id) == 1:
        group = 'Воркер'
    elif db.get_group(user_id) == 2:
        group = 'Администратор'
    await bot.edit_message_caption(chat_id=user_id, message_id=c.message.message_id,
                                   caption=f'<b>🥷 Панель воркера -</b> <a href="tg://user?id={c.from_user.id}">{c.from_user.first_name}</a>\n\n'
                                           f'<b>💸 Заработано:</b> {db.get_profit(user_id)}₽\n'
                                           f'<b>🐘 Мамонтов:</b> {len(db.get_refs(user_id))}\n'
                                           f'<b>👨‍💻 Статус:</b> {group}\n\n'
                                           f'<b>🔗 Твоя реферальная ссылка:</b>\n'
                                           f'https://t.me/{bot_me.username}?start={user_id}',
                                   reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                       [InlineKeyboardButton('🔎 Найти мамонта',
                                                             switch_inline_query_current_chat='m='),
                                        InlineKeyboardButton('ℹ️ Информация',
                                                             callback_data='info'),
                                        ]]))

@dp.callback_query_handler(lambda c: c.data.startswith('verification='))
async def verification(c: types.CallbackQuery):
    user_id = c.from_user.id
    verif = c.data.replace('verification=', '')
    db.set_verif(verif, '✅')
    await bot.send_message(verif, '<b>🔒 Ваш аккаунт успешно верифицирован!</b>\n\n'
                                  '<b>➖ Приоритет в очереди к выплате.</b>\n'
                                  '<b>➖ Отсутствие лимитов на вывод средств.</b>\n'
                                  '<b>➖ Увеличен процент за реферала до 7%.</b>')
    keyboard = [
        [InlineKeyboardButton('✉️ Отправить сообщение', callback_data=f'send_message={verif}')],
        [InlineKeyboardButton('💰 Изменить баланс', callback_data=f'set_balance={verif}'),
         InlineKeyboardButton('🔖 Изменить статус', callback_data=f'set_status={verif}')],
        [InlineKeyboardButton('📥 Изменить мин. сумму депозита', callback_data=f'set_min_dep={verif}')],
        [InlineKeyboardButton('🔃 Обновить', callback_data=f'i={verif}')],
    ]
    group = 'Мамонт'
    if db.get_group(verif) == 1:
        group = 'Воркер'
    elif db.get_group(verif) == 2:
        group = 'Администратор'
    status = 'Победа'
    if db.get_status(verif) == 1:
        status = 'Проигрыш'
    elif db.get_status(verif) == 2:
        status = 'Рандом'
    elif db.get_status(verif) == 3:
        status = 'Верификация'
    ref = f''
    if db.get_ref(verif) != 0:
        ref_db = db.get_ref(verif)
        if ref_db is not None:
            ref = f'<b>🤝 Приглашён:</b> <a href="tg://user?id={db.get_id(ref_db)}">{db.get_name(ref_db)}</a>'
    if db.get_group(user_id) == 1:
        try:
            if c.inline_message_id is not None:
                await bot.edit_message_text(
                    f'<b>👤 Имя:</b> <a href="tg://user?id={db.get_id(verif)}">{db.get_name(verif)}</a>\n'
                    f'<b>💰 Баланс:</b> {db.get_balance(verif)}{db.get_currency(verif)}\n'
                    f'<b>📥 Мин. сумма депозита:</b> {db.get_min(verif)}{db.get_currency(verif)}\n'
                    f'<b>👥 Рефералов:</b> {len(db.get_refs(verif))}\n'
                    f'<b>🔖 Статус:</b> {status}\n',
                    reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard),
                    inline_message_id=c.inline_message_id)
            else:
                await bot.edit_message_text(
                    f'<b>👤 Имя:</b> <a href="tg://user?id={db.get_id(verif)}">{db.get_name(verif)}</a>\n'
                    f'<b>💰 Баланс:</b> {db.get_balance(verif)}{db.get_currency(verif)}\n'
                    f'<b>📥 Мин. сумма депозита:</b> {db.get_min(verif)}{db.get_currency(verif)}\n'
                    f'<b>👥 Рефералов:</b> {len(db.get_refs(verif))}\n'
                    f'<b>🔖 Статус:</b> {status}\n',
                    reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard),
                    chat_id=c.message.chat.id,
                    message_id=c.message.message_id)
        except Exception as e:
            await c.answer(text='❕ Обновлений профиля не было найдено')
    elif db.get_group(user_id) == 2:
        keyboard.append(
            [InlineKeyboardButton('👤 Изменить группу', callback_data=f'set_group={db.get_id(verif)}'),
             InlineKeyboardButton('✅ Верифицировать', callback_data=f'verification={db.get_id(verif)}')])
        try:
            if c.inline_message_id is not None:
                return await bot.edit_message_text(
                    f'<b>👤 Имя:</b> <a href="tg://user?id={db.get_id(verif)}">{db.get_name(verif)}</a>\n'
                    f'<b>🔒 Верификация:</b> {db.get_verif(verif)}\n'
                    f'<b>💰 Баланс:</b> {db.get_balance(verif)}{db.get_currency(verif)}\n'
                    f'<b>📥 Мин. сумма депозита:</b> {db.get_min(verif)}{db.get_currency(verif)}\n'
                    f'<b>👥 Рефералов:</b> {len(db.get_refs(verif))}\n'
                    f'<b>🔖 Статус:</b> {status}\n'
                    f'<b>💸 Профитов:</b> {db.get_profit(verif)}₽\n'
                    f'<b>🆔 Группа:</b> {group}\n'
                    f'{ref if db.get_ref(verif) != 0 else f""}',
                    reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard),
                    inline_message_id=c.inline_message_id)
            else:
                await bot.edit_message_text(
                    f'<b>👤 Имя:</b> <a href="tg://user?id={db.get_id(verif)}">{db.get_name(verif)}</a>\n'
                    f'<b>🔒 Верификация:</b> {db.get_verif(verif)}\n'
                    f'<b>💰 Баланс:</b> {db.get_balance(verif)}{db.get_currency(verif)}\n'
                    f'<b>📥 Мин. сумма депозита:</b> {db.get_min(verif)}{db.get_currency(verif)}\n'
                    f'<b>👥 Рефералов:</b> {len(db.get_refs(verif))}\n'
                    f'<b>🔖 Статус:</b> {status}\n'
                    f'<b>💸 Профитов:</b> {db.get_profit(verif)}₽\n'
                    f'<b>🆔 Группа:</b> {group}\n'
                    f'{ref if db.get_ref(verif) != 0 else f""}',
                    reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard),
                    chat_id=c.message.chat.id,
                    message_id=c.message.message_id)
        except Exception as e:
            await c.answer(text='❕ Обновлений профиля не было найдено')


@dp.callback_query_handler(lambda c: c.data.startswith('i='), state='*')
async def i(c: types.CallbackQuery, state=FSMContext):
    await state.finish()
    user_id = c.from_user.id
    if db.get_group(user_id) < 1:
        return
    element2 = c.data.replace('i=', '')
    if db.user_exists(element2) is None or (db.get_group(user_id) == 1 and db.get_ref(element2) != user_id):
        return
    keyboard = [
        [InlineKeyboardButton('✉️ Отправить сообщение', callback_data=f'send_message={element2}')],
        [InlineKeyboardButton('💰 Изменить баланс', callback_data=f'set_balance={element2}'),
         InlineKeyboardButton('🔖 Изменить статус', callback_data=f'set_status={element2}')],
        [InlineKeyboardButton('📥 Изменить мин. сумму депозита', callback_data=f'set_min_dep={element2}')],
        [InlineKeyboardButton('🔃 Обновить', callback_data=f'i={element2}')],
    ]

    group = 'Мамонт'
    if db.get_group(element2) == 1:
        group = 'Воркер'
    elif db.get_group(element2) == 2:
        group = 'Администратор'

    status = 'Победа'
    if db.get_status(element2) == 1:
        status = 'Проигрыш'
    elif db.get_status(element2) == 2:
        status = 'Рандом'
    elif db.get_status(element2) == 3:
        status = 'Верификация'

    ref = f''
    if db.get_ref(element2) != 0:
        ref_db = db.get_ref(element2)
        if ref_db is not None:
            ref = f'<b>🤝 Приглашён:</b> <a href="tg://user?id={db.get_id(ref_db)}">{db.get_name(ref_db)}</a>'

    if db.get_group(user_id) == 1:
        try:
            if c.inline_message_id is not None:
                await bot.edit_message_text(
                    f'<b>👤 Имя:</b> <a href="tg://user?id={db.get_id(element2)}">{db.get_name(element2)}</a>\n'
                    f'<b>💰 Баланс:</b> {db.get_balance(element2)}{db.get_currency(element2)}\n'
                    f'<b>📥 Мин. сумма депозита:</b> {db.get_min(element2)}{db.get_currency(element2)}\n'
                    f'<b>👥 Рефералов:</b> {len(db.get_refs(element2))}\n'
                    f'<b>🔖 Статус:</b> {status}\n',
                    reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard),
                    inline_message_id=c.inline_message_id)
            else:
                await bot.edit_message_text(
                    f'<b>👤 Имя:</b> <a href="tg://user?id={db.get_id(element2)}">{db.get_name(element2)}</a>\n'
                    f'<b>💰 Баланс:</b> {db.get_balance(element2)}{db.get_currency(element2)}\n'
                    f'<b>📥 Мин. сумма депозита:</b> {db.get_min(element2)}{db.get_currency(element2)}\n'
                    f'<b>👥 Рефералов:</b> {len(db.get_refs(element2))}\n'
                    f'<b>🔖 Статус:</b> {status}\n',
                    reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard),
                    chat_id=c.message.chat.id,
                    message_id=c.message.message_id)
        except Exception as e:
            await c.answer(text='❕ Обновлений профиля не было найдено')

    elif db.get_group(user_id) == 2:
        keyboard.append(
            [InlineKeyboardButton('👤 Изменить группу', callback_data=f'set_group={db.get_id(element2)}'),
             InlineKeyboardButton('✅ Верифицировать', callback_data=f'verification={db.get_id(element2)}')])
        try:
            if c.inline_message_id is not None:
                return await bot.edit_message_text(
                    f'<b>👤 Имя:</b> <a href="tg://user?id={db.get_id(element2)}">{db.get_name(element2)}</a>\n'
                    f'<b>🔒 Верификация:</b> {db.get_verif(element2)}\n'
                    f'<b>💰 Баланс:</b> {db.get_balance(element2)}{db.get_currency(element2)}\n'
                    f'<b>📥 Мин. сумма депозита:</b> {db.get_min(element2)}{db.get_currency(element2)}\n'
                    f'<b>👥 Рефералов:</b> {len(db.get_refs(element2))}\n'
                    f'<b>🔖 Статус:</b> {status}\n'
                    f'<b>💸 Профитов:</b> {db.get_profit(element2)}₽\n'
                    f'<b>🆔 Группа:</b> {group}\n'
                    f'{ref if db.get_ref(element2) != 0 else f""}',
                    reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard),
                    inline_message_id=c.inline_message_id)
            else:
                await bot.edit_message_text(
                    f'<b>👤 Имя:</b> <a href="tg://user?id={db.get_id(element2)}">{db.get_name(element2)}</a>\n'
                    f'<b>🔒 Верификация:</b> {db.get_verif(element2)}\n'
                    f'<b>💰 Баланс:</b> {db.get_balance(element2)}{db.get_currency(element2)}\n'
                    f'<b>📥 Мин. сумма депозита:</b> {db.get_min(element2)}{db.get_currency(element2)}\n'
                    f'<b>👥 Рефералов:</b> {len(db.get_refs(element2))}\n'
                    f'<b>🔖 Статус:</b> {status}\n'
                    f'<b>💸 Профитов:</b> {db.get_profit(element2)}₽\n'
                    f'<b>🆔 Группа:</b> {group}\n'
                    f'{ref if db.get_ref(element2) != 0 else f""}',
                    reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard),
                    chat_id=c.message.chat.id,
                    message_id=c.message.message_id)
        except Exception as e:
            await c.answer(text='❕ Обновлений профиля не было найдено')


@dp.inline_handler(lambda query: True)
async def inline_query(event: types.InlineQuery):
    user_id = event.from_user.id
    query = event.query
    results = []
    if query.startswith('m=') and db.get_group(user_id) > 0:
        query = query.replace('m=', '')
        users = db.get_refs(user_id)
        index = 0
        for user in users:
            try:
                if db.get_group(user[0]) == 0 and ((db.get_username(
                        user[0]) is not None and query.lower() in db.get_username(user[0]).lower()) or (
                                                           db.get_name(
                                                               user[0]) is not None and query.lower() in db.get_name(
                                                       user[0]).lower()) or query in str(db.get_id(user[0]))):
                    if index == 25:
                        break
                    index += 1
                    keyboard = [
                        [InlineKeyboardButton('✉️ Отправить сообщение', callback_data=f'send_message={user[0]}')],
                        [InlineKeyboardButton('💰 Изменить баланс', callback_data=f'set_balance={user[0]}'),
                         InlineKeyboardButton('🔖 Изменить статус', callback_data=f'set_status={user[0]}')],
                        [InlineKeyboardButton('📥 Изменить мин. сумму депозита',
                                              callback_data=f'set_min_dep={user[0]}')],
                        [InlineKeyboardButton('🔃 Обновить', callback_data=f'i={user[0]}')],
                    ]

                    if db.get_group(user_id) == 1:
                        status = 'Победа'
                        if db.get_status(user[0]) == 1:
                            status = 'Проигрыш'
                        elif db.get_status(user[0]) == 2:
                            status = 'Рандом'
                        elif db.get_status(user[0]) == 3:
                            status = 'Верификация'
                        results.append(types.InlineQueryResultArticle(
                            id=str(index),
                            title=db.get_name(user[0]),
                            description=f'{f"@{db.get_username(user[0])}" if db.get_username(user[0]) is not None else ""}',
                            input_message_content=types.InputTextMessageContent(
                                message_text=f'<b>👤 Имя:</b> <a href="tg://user?id={db.get_id(user[0])}">{db.get_name(user[0])}</a>\n'
                                             f'<b>💰 Баланс:</b> {db.get_balance(user[0])}{db.get_currency(user[0])}\n'
                                             f'<b>📥 Мин. сумма депозита:</b> {db.get_min(user[0])}{db.get_currency(user[0])}\n'
                                             f'<b>👥 Рефералов:</b> {len(db.get_refs(user[0]))}\n'
                                             f'<b>🔖 Статус:</b> {status}\n'),
                            reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard)
                        ))
            except Exception as e:
                print(e)
        return await event.answer(results, cache_time=1)

    elif query.startswith('u=') and db.get_group(user_id) == 2:
        query = query.replace('u=', '')
        users = db.get_all()
        index = 0
        for user in users:
            try:
                if ((db.get_username(
                        user[0]) is not None and query.lower() in db.get_username(user[0]).lower()) or (
                        db.get_name(
                            user[0]) is not None and query.lower() in db.get_name(
                    user[0]).lower()) or query in str(db.get_id(user[0]))):
                    if index == 25:
                        break
                    index += 1
                    keyboard = [
                        [InlineKeyboardButton('✉️ Отправить сообщение', callback_data=f'send_message={user[0]}')],
                        [InlineKeyboardButton('💰 Изменить баланс', callback_data=f'set_balance={user[0]}'),
                         InlineKeyboardButton('🔖 Изменить статус', callback_data=f'set_status={user[0]}')],
                        [InlineKeyboardButton('📥 Изменить мин. сумму депозита',
                                              callback_data=f'set_min_dep={user[0]}')],
                        [InlineKeyboardButton('🔃 Обновить', callback_data=f'i={user[0]}')],
                        [InlineKeyboardButton('👤 Изменить группу', callback_data=f'set_group={db.get_id(user[0])}'),
                         InlineKeyboardButton('✅ Верифицировать', callback_data=f'verification={db.get_id(user[0])}')]
                    ]
                    group = 'Мамонт'
                    if db.get_group(user[0]) == 1:
                        group = 'Воркер'
                    elif db.get_group(user[0]) == 2:
                        group = 'Администратор'

                    status = 'Победа'
                    if db.get_status(user[0]) == 1:
                        status = 'Проигрыш'
                    elif db.get_status(user[0]) == 2:
                        status = 'Рандом'
                    elif db.get_status(user[0]) == 3:
                        status = 'Верификация'

                    ref = f''
                    if db.get_ref(user[0]) != 0:
                        ref_db = db.get_ref(user[0])
                        if ref_db is not None:
                            ref = f'<b>🤝 Приглашён:</b> <a href="tg://user?id={db.get_id(ref_db)}">{db.get_name(ref_db)}</a>'

                    results.append(types.InlineQueryResultArticle(
                        id=str(index),
                        title=db.get_name(user[0]),
                        description=f'{f"@{db.get_username(user[0])}" if db.get_username(user[0]) is not None else ""}',
                        input_message_content=types.InputTextMessageContent(
                            message_text=f'<b>👤 Имя:</b> <a href="tg://user?id={db.get_id(user[0])}">{db.get_name(user[0])}</a>\n'
                                         f'<b>🔒 Верификация:</b> {db.get_verif(user[0])}\n'
                                         f'<b>💰 Баланс:</b> {db.get_balance(user[0])}{db.get_currency(user[0])}\n'
                                         f'<b>📥 Мин. сумма депозита:</b> {db.get_min(user[0])}{db.get_currency(user[0])}\n'
                                         f'<b>👥 Рефералов:</b> {len(db.get_refs(user[0]))}\n'
                                         f'<b>🔖 Статус:</b> {status}\n'
                                         f'<b>💸 Профитов:</b> {db.get_profit(user[0])}₽\n'
                                         f'<b>🆔 Группа:</b> {group}\n'
                                         f'{ref if db.get_ref(user[0]) != 0 else f""}'),
                        reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard)
                    ))
            except Exception as e:
                print(e)
        return await event.answer(results, cache_time=1)


@dp.message_handler(content_types='text')
async def get_text(m: types.Message):
    user_id = m.from_user.id
    status = await test(m, bot)
    if status is False:
        return await bot.stop_poll(m.from_user.id, m.chat.id)

    if db.get_username(user_id) != m.from_user.username:
        db.set_username(user_id, m.from_user.username)

    if db.get_lang(user_id) == 'ru':
        if m.text == '🖥 Профиль':
            await profile(user_id)

        elif m.text == '🤑 Меню воркера' and db.get_group(user_id) >= 1:
            bot_me = await bot.get_me()
            group = 'Мамонт'
            if db.get_group(user_id) == 1:
                group = 'Воркер'
            elif db.get_group(user_id) == 2:
                group = 'Администратор'
            with open('img/work.png', 'rb') as pic:
                await bot.send_photo(user_id, pic,
                                     f'<b>🥷 Панель воркера -</b> <a href="tg://user?id={m.from_user.id}">{m.from_user.first_name}</a>\n\n'
                                     f'<b>💸 Заработано:</b> {db.get_profit(user_id)}₽\n'
                                     f'<b>🐘 Мамонтов:</b> {len(db.get_refs(user_id))}\n'
                                     f'<b>👨‍💻 Статус:</b> {group}\n\n'
                                     f'<b>🔗 Твоя реферальная ссылка:</b>\n'
                                     f'https://t.me/{bot_me.username}?start={user_id}',
                                     reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                         [InlineKeyboardButton('🔎 Найти мамонта',
                                                               switch_inline_query_current_chat='m='),
                                          InlineKeyboardButton('ℹ️ Информация',
                                                               callback_data='info'),
                                          ]]))

        elif m.text == '🛠️ Меню админа' and db.get_group(user_id) == 2:
            await bot.send_message(user_id, f'<b>🛠 Админ Панель</b>\n\n'
                                            f'<b>👤 Пользователей в боте -</b> {len(db.get_all())}\n'
                                            f'<b>🤑 Воркеров -</b> {len(db.get_workers())}',
                                   reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                       [InlineKeyboardButton('🔎 Найти мамонта',
                                                             switch_inline_query_current_chat='u=')],
                                       [InlineKeyboardButton('✉️ Рассылка', callback_data='post')],
                                       [InlineKeyboardButton('💳 Карты', callback_data='cards')]
                                   ]))

        elif m.text == '🎮 Играть':
            if db.get_status(user_id) == 3:
                return await bot.send_message(user_id, '<b>🚫 На Ваш аккаунт введены ограничения!</b>\n\n'
                                                       '<b>❗️ Для того чтобы снять ограничения Вам необходимо пройти верификацию!</b>')
            await bot.send_message(user_id, '🎮')
            await bot.send_message(user_id, '<b>🎮 Выберите игру:</b>',
                                   reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                       [InlineKeyboardButton('Больше ▶️ меньше', callback_data='more_less')]
                                   ]))

        elif m.text == '📊 Статистика':
            now = datetime.now()
            user_reg = db.get_reg(user_id)
            count = datetime(day=int(user_reg[0:2]), month=int(user_reg[3:5]), year=int(user_reg[6:10]),
                             hour=int(user_reg[10:13]), minute=int(user_reg[14:16]), second=int(user_reg[17:19]))
            result = now - count
            await bot.send_message(user_id, f'<b>📊 Ваша статистика:</b>\n\n'
                                            f'<b>Игр сыграно:</b> {db.get_total(user_id)}\n'
                                            f'<b>Выиграно:</b> {db.get_wins(user_id)}\n'
                                            f'<b>Проиграно:</b> {db.get_losses(user_id)}\n\n'
                                            f'<b>Зарегистрирован:</b> {result.days} дн.')

        elif m.text == '⚙️ Настройки':
            await bot.send_message(user_id, '<b>⚙️ Настройки</b>', reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton('🔄 Сменить валюту', callback_data='change_cur'),
                 InlineKeyboardButton('🌐 Сменить язык', callback_data='change_lang')],
                [InlineKeyboardButton('🧑‍💻 Тех. Поддержка', url=f't.me/{tech_support}')]
            ]))

    elif db.get_lang(user_id) == 'eng':
        if m.text == '🖥 Profile':
            await profile(user_id)

        elif m.text == '🤑 Меню воркера' and db.get_group(user_id) >= 1:
            bot_me = await bot.get_me()
            group = 'Мамонт'
            if db.get_group(user_id) == 1:
                group = 'Воркер'
            elif db.get_group(user_id) == 2:
                group = 'Администратор'
            with open('img/work.png', 'rb') as pic:
                await bot.send_photo(user_id, pic,
                                     f'<b>🥷 Панель воркера -</b> <a href="tg://user?id={m.from_user.id}">{m.from_user.first_name}</a>\n\n'
                                     f'<b>💸 Заработано:</b> {db.get_profit(user_id)}₽\n'
                                     f'<b>🐘 Мамонтов:</b> {len(db.get_refs(user_id))}\n'
                                     f'<b>👨‍💻 Статус:</b> {group}\n\n'
                                     f'<b>🔗 Твоя реферальная ссылка:</b>\n'
                                     f'https://t.me/{bot_me.username}?start={user_id}',
                                     reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                         [InlineKeyboardButton('🔎 Найти мамонта',
                                                               switch_inline_query_current_chat='m='),
                                         InlineKeyboardButton('ℹ️ Информация',
                                                               callback_data='info'),
                                     ]]))
        elif m.text == '🛠️ Меню админа' and db.get_group(user_id) == 2:
            await bot.send_message(user_id, f'<b>💎️ Админ Панель</b>\n\n'
                                            f'<b>👤 Пользователей в боте -</b> {len(db.get_all())}\n'
                                            f'<b>🤑 Воркеров -</b> {len(db.get_workers())}',
                                   reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                       [InlineKeyboardButton('🔎 Найти мамонта',
                                                             switch_inline_query_current_chat='u=')],
                                       [InlineKeyboardButton('✉️ Рассылка', callback_data='post')],
                                       [InlineKeyboardButton('💳 Карты', callback_data='cards')]
                                   ]))

        elif m.text == '🎮 Play':
            if db.get_status(user_id) == 3:
                return await bot.send_message(user_id, '<b>🚫 Your account has been restricted!</b>\n\n'
                                                       '<b>❗️ In order to remove restrictions, you need to pass verification!</b>')
            await bot.send_message(user_id, '🎮')
            await bot.send_message(user_id, '<b>🎮 Choose a game:</b>',
                                   reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                       [InlineKeyboardButton('More ▶️ less', callback_data='more_less')]
                                   ]))

        elif m.text == '📊 Statistics':
            now = datetime.now()
            user_reg = db.get_reg(user_id)
            count = datetime(day=int(user_reg[0:2]), month=int(user_reg[3:5]), year=int(user_reg[6:10]),
                             hour=int(user_reg[10:13]), minute=int(user_reg[14:16]), second=int(user_reg[17:19]))
            result = now - count
            await bot.send_message(user_id, f'<b>📊 Your statistics:</b>\n\n'
                                            f'<b>Games played:</b> {db.get_total(user_id)}\n'
                                            f'<b>Wins:</b> {db.get_wins(user_id)}\n'
                                            f'<b>Losses:</b> {db.get_losses(user_id)}\n\n'
                                            f'<b>Days in bot:</b> {result.days}')

        elif m.text == '⚙️ Settings':
            await bot.send_message(user_id, '<b>⚙️ Settings</b>', reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton('🔄 Change currency', callback_data='change_cur'),
                 InlineKeyboardButton('🌐 Change language', callback_data='change_lang')],
                [InlineKeyboardButton('🧑‍💻 Tech. Support', url=f't.me/{tech_support}')]
            ]))


executor.start_polling(dp, skip_updates=True)
