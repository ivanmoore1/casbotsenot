import states
import random
from loader import db, dp, bot
from func import timer
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext


@dp.callback_query_handler(lambda call: call.data == 'more_less')
async def game_more_less(c: types.CallbackQuery):
    user_id = c.from_user.id
    if db.get_lang(user_id) == 'ru':
        await bot.edit_message_text(chat_id=user_id, message_id=c.message.message_id,
                                    text='<b>📝 Правила игры в "Больше ▶️ меньше":</b>\n\n'
                                         '<b>• Ваша задача - угадать, в каком диапазоне будет располагаться выпадшее число.</b>\n\n'
                                         '<b>• Если число выпадет в диапазоне от 0 до 50 или от 50 до 100 - тогда вы получите х2 к вашей ставке.</b>\n\n'
                                         '<b>• Если выпадет число равное 50 - тогда вы получите х5 к вашей ставке.</b>',
                                    reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                        [InlineKeyboardButton('🎮 Начать игру', callback_data='start_more_less')],
                                        [InlineKeyboardButton('◀️ В главное меню', callback_data='cancel')]
                                    ]))
    elif db.get_lang(user_id) == 'eng':
        await bot.edit_message_text(chat_id=user_id, message_id=c.message.message_id,
                                    text='<b>📝 Rules of the game "More ▶️ less":</b>\n\n'
                                         '<b>• Your task is to guess in which range the drawn number will be located.</b>\n\n'
                                         '<b>• If the number falls in the range from 0 to 50 or from 50 to 100 - then you will get x2 to your bet.</b>\n\n'
                                         '<b>• If a number equal to 50 falls out - then you will get x5 to your bet.</b>',
                                    reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                        [InlineKeyboardButton('🎮 Start the game', callback_data='start_more_less')],
                                        [InlineKeyboardButton('◀️ To main menu', callback_data='cancel')]
                                    ]))


@dp.callback_query_handler(lambda call: call.data == 'start_more_less')
async def game_more_less2(c: types.CallbackQuery):
    user_id = c.from_user.id
    await states.MoreLess.bet.set()
    if db.get_lang(user_id) == 'ru':
        await bot.edit_message_text(chat_id=user_id, message_id=c.message.message_id,
                                    text=f'<b>"Больше ▶️ меньше"</b>\n\n'
                                         f'<b>💰 Ваш баланс:</b> {db.get_balance(user_id)}{db.get_currency(user_id)}\n'
                                         f'<b>✍️ Введите сумму ставки:</b>',
                                    reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                        [InlineKeyboardButton('❌ Закончить игру', callback_data='cancel')]
                                    ]))
    elif db.get_lang(user_id) == 'eng':
        await bot.edit_message_text(chat_id=user_id, message_id=c.message.message_id,
                                    text=f'<b>"More ▶️ less"</b>\n\n'
                                         f'<b>💰 Your balance:</b> {db.get_balance(user_id)}{db.get_currency(user_id)}\n'
                                         f'<b>✍️ Enter bet amount:</b>',
                                    reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                        [InlineKeyboardButton('❌ Finish the game', callback_data='cancel')]
                                    ]))


@dp.message_handler(content_types='text', state=states.MoreLess.bet)
async def game_more_less3(m: types.Message, state=FSMContext):
    user_id = m.from_user.id
    async with state.proxy() as data:
        data['answers'] = m.text
        bet = data['answers']
        if bet.isdigit() and db.get_balance(user_id) >= float(bet) != 0:
            if db.get_lang(user_id) == 'ru':
                await bot.send_message(user_id, f'<b>🎲 Сейчас выпадет случайное число от 0 до 100</b>\n\n'
                                                f'<b>💰 Сумма ставки:</b> {bet}{db.get_currency(user_id)}\n\n'
                                                f'<b>❕ Выберите исход события:</b>',
                                       reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                           [InlineKeyboardButton('« 50', callback_data=f'bet=^<50^{bet}'),
                                            InlineKeyboardButton('= 50', callback_data=f'bet=^=50^{bet}'),
                                            InlineKeyboardButton('» 50', callback_data=f'bet=^>50^{bet}')]
                                       ]))
                await state.finish()
            elif db.get_lang(user_id) == 'eng':
                await bot.send_message(user_id, f'<b>🎲 Now a random number will be drawn from 0 to 100</b>\n\n'
                                                f'<b>💰 Stake amount:</b> {bet}{db.get_currency(user_id)}\n\n'
                                                f'<b>❕ Select event outcome:</b>',
                                       reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                           [InlineKeyboardButton('« 50', callback_data=f'bet=^<50^{bet}'),
                                            InlineKeyboardButton('= 50', callback_data=f'bet=^=50^{bet}'),
                                            InlineKeyboardButton('» 50', callback_data=f'bet=^>50^{bet}')]
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


@dp.callback_query_handler(lambda call: call.data.startswith('bet='))
async def game_more_less4(c: types.CallbackQuery):
    user_id = c.from_user.id
    bet = c.data.replace('bet=', '').split('^')
    status = db.get_status(user_id)
    ref = db.get_ref(user_id)
    if ref == 0:
        ref = ''
    if bet[1] == '<50':
        if status == 0:
            num = random.choice(range(0, 49))
            if num < 50:
                await timer(c, user_id)
                balance = db.get_balance(user_id) + float(bet[2])
                db.set_balance(user_id, float(balance))
                db.set_total(user_id, round(db.get_total(user_id) + 1))
                db.set_wins(user_id, round(db.get_wins(user_id) + 1))
                if db.get_lang(user_id) == 'ru':
                    await bot.edit_message_text(chat_id=user_id, message_id=c.message.message_id,
                                                text=f'<b>🎉 Вы выиграли! Выпало:</b> {num}\n\n'
                                                     f'<b>💵 Ставка:</b> {bet[2]}{db.get_currency(user_id)}\n\n'
                                                     f'<b>💰 Баланс:</b> {db.get_balance(user_id)}{db.get_currency(user_id)}',
                                                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                                    [InlineKeyboardButton('🔄 Сыграть ещё раз',
                                                                          callback_data='more_less_repeat')],
                                                    [InlineKeyboardButton('❌ Закончить игру', callback_data='cancel')]
                                                ]))
                elif db.get_lang(user_id) == 'eng':
                    await bot.edit_message_text(chat_id=user_id, message_id=c.message.message_id,
                                                text=f'<b>🎉 You have won! Dropped:</b> {num}\n\n'
                                                     f'<b>💵 Bet:</b> {bet[2]}{db.get_currency(user_id)}\n\n'
                                                     f'<b>💰 Balance:</b> {db.get_balance(user_id)}{db.get_currency(user_id)}',
                                                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                                    [InlineKeyboardButton('🔄 Play again',
                                                                          callback_data='more_less_repeat')],
                                                    [InlineKeyboardButton('❌ Finish the game', callback_data='cancel')]
                                                ]))
                if db.get_group(ref) > 0:
                    await bot.send_message(ref,
                                           f'<b>🎮 Мамонт <a href="tg://user?id={user_id}">{db.get_name(user_id)}</a> сделал ставку!</b>\n\n'
                                           f'Ставка: <b>{bet[2]}{db.get_currency(user_id)}</b>\n'
                                           f'Ставил на: <b>« 50</b>\n'
                                           f'Итог: <b>Выиграл</b>\n'
                                           f'Баланс: <b>{db.get_balance(user_id)}{db.get_currency(user_id)}</b>')
        elif status == 1:
            num = random.choice(range(51, 100))
            if num > 50:
                await timer(c, user_id)
                balance = db.get_balance(user_id) - float(bet[2])
                db.set_balance(user_id, float(balance))
                db.set_total(user_id, round(db.get_total(user_id) + 1))
                db.set_losses(user_id, round(db.get_losses(user_id) + 1))
                if db.get_lang(user_id) == 'ru':
                    await bot.edit_message_text(chat_id=user_id, message_id=c.message.message_id,
                                                text=f'<b>💣 Вы проиграли! Выпало:</b> {num}\n\n'
                                                     f'<b>💵 Ставка:</b> {bet[2]}{db.get_currency(user_id)}\n\n'
                                                     f'<b>💰 Баланс:</b> {db.get_balance(user_id)}{db.get_currency(user_id)}',
                                                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                                    [InlineKeyboardButton('🔄 Сыграть ещё раз',
                                                                          callback_data='more_less_repeat')],
                                                    [InlineKeyboardButton('❌ Закончить игру', callback_data='cancel')]
                                                ]))
                elif db.get_lang(user_id) == 'eng':
                    await bot.edit_message_text(chat_id=user_id, message_id=c.message.message_id,
                                                text=f'<b>💣 You lost! Dropped:</b> {num}\n\n'
                                                     f'<b>💵 Bet:</b> {bet[2]}{db.get_currency(user_id)}\n\n'
                                                     f'<b>💰 Balance:</b> {db.get_balance(user_id)}{db.get_currency(user_id)}',
                                                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                                    [InlineKeyboardButton('🔄 Play again',
                                                                          callback_data='more_less_repeat')],
                                                    [InlineKeyboardButton('❌ Finish the game', callback_data='cancel')]
                                                ]))
                if db.get_group(ref) > 0:
                    await bot.send_message(ref,
                                           f'<b>🎮 Мамонт <a href="tg://user?id={user_id}">{db.get_name(user_id)}</a> сделал ставку!</b>\n\n'
                                           f'Ставка: <b>{bet[2]}{db.get_currency(user_id)}</b>\n'
                                           f'Ставил на: <b>« 50</b>\n'
                                           f'Итог: <b>Проиграл</b>\n'
                                           f'Баланс: <b>{db.get_balance(user_id)}{db.get_currency(user_id)}</b>')
        elif status == 2:
            num = random.choice(range(0, 100))
            if num < 50:
                await timer(c, user_id)
                balance = db.get_balance(user_id) + float(bet[2])
                db.set_balance(user_id, float(balance))
                db.set_total(user_id, round(db.get_total(user_id) + 1))
                db.set_wins(user_id, round(db.get_wins(user_id) + 1))
                if db.get_lang(user_id) == 'ru':
                    await bot.edit_message_text(chat_id=user_id, message_id=c.message.message_id,
                                                text=f'<b>🎉 Вы выиграли! Выпало:</b> {num}\n\n'
                                                     f'<b>💵 Ставка:</b> {bet[2]}{db.get_currency(user_id)}\n\n'
                                                     f'<b>💰 Баланс:</b> {db.get_balance(user_id)}{db.get_currency(user_id)}',
                                                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                                    [InlineKeyboardButton('🔄 Сыграть ещё раз',
                                                                          callback_data='more_less_repeat')],
                                                    [InlineKeyboardButton('❌ Закончить игру', callback_data='cancel')]
                                                ]))
                elif db.get_lang(user_id) == 'eng':
                    await bot.edit_message_text(chat_id=user_id, message_id=c.message.message_id,
                                                text=f'<b>🎉 You have won! Dropped:</b> {num}\n\n'
                                                     f'<b>💵 Bet:</b> {bet[2]}{db.get_currency(user_id)}\n\n'
                                                     f'<b>💰 Balance:</b> {db.get_balance(user_id)}{db.get_currency(user_id)}',
                                                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                                    [InlineKeyboardButton('🔄 Play again',
                                                                          callback_data='more_less_repeat')],
                                                    [InlineKeyboardButton('❌ Finish the game', callback_data='cancel')]
                                                ]))
                if db.get_group(ref) > 0:
                    await bot.send_message(ref,
                                           f'<b>🎮 Мамонт <a href="tg://user?id={user_id}">{db.get_name(user_id)}</a> сделал ставку!</b>\n\n'
                                           f'Ставка: <b>{bet[2]}{db.get_currency(user_id)}</b>\n'
                                           f'Ставил на: <b>« 50</b>\n'
                                           f'Итог: <b>Выиграл</b>\n'
                                           f'Баланс: <b>{db.get_balance(user_id)}{db.get_currency(user_id)}</b>')
            else:
                await timer(c, user_id)
                balance = db.get_balance(user_id) - float(bet[2])
                db.set_balance(user_id, float(balance))
                db.set_total(user_id, round(db.get_total(user_id) + 1))
                db.set_losses(user_id, round(db.get_losses(user_id) + 1))
                if db.get_lang(user_id) == 'ru':
                    await bot.edit_message_text(chat_id=user_id, message_id=c.message.message_id,
                                                text=f'<b>💣 Вы проиграли! Выпало:</b> {num}\n\n'
                                                     f'<b>💵 Ставка:</b> {bet[2]}{db.get_currency(user_id)}\n\n'
                                                     f'<b>💰 Баланс:</b> {db.get_balance(user_id)}{db.get_currency(user_id)}',
                                                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                                    [InlineKeyboardButton('🔄 Сыграть ещё раз',
                                                                          callback_data='more_less_repeat')],
                                                    [InlineKeyboardButton('❌ Закончить игру', callback_data='cancel')]
                                                ]))
                elif db.get_lang(user_id) == 'eng':
                    await bot.edit_message_text(chat_id=user_id, message_id=c.message.message_id,
                                                text=f'<b>💣 You lost! Dropped:</b> {num}\n\n'
                                                     f'<b>💵 Bet:</b> {bet[2]}{db.get_currency(user_id)}\n\n'
                                                     f'<b>💰 Balance:</b> {db.get_balance(user_id)}{db.get_currency(user_id)}',
                                                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                                    [InlineKeyboardButton('🔄 Play again',
                                                                          callback_data='more_less_repeat')],
                                                    [InlineKeyboardButton('❌ Finish the game', callback_data='cancel')]
                                                ]))
                if db.get_group(ref) > 0:
                    await bot.send_message(ref,
                                           f'<b>🎮 Мамонт <a href="tg://user?id={user_id}">{db.get_name(user_id)}</a> сделал ставку!</b>\n\n'
                                           f'Ставка: <b>{bet[2]}{db.get_currency(user_id)}</b>\n'
                                           f'Ставил на: <b>« 50</b>\n'
                                           f'Итог: <b>Проиграл</b>\n'
                                           f'Баланс: <b>{db.get_balance(user_id)}{db.get_currency(user_id)}</b>')

    elif bet[1] == '=50':
        if status == 0:
            num = 50
            if num == 50:
                await timer(c, user_id)
                balance = (float(bet[2]) * 5) + db.get_balance(user_id)
                db.set_balance(user_id, float(balance))
                db.set_total(user_id, round(db.get_total(user_id) + 1))
                db.set_wins(user_id, round(db.get_wins(user_id) + 1))
                if db.get_lang(user_id) == 'ru':
                    await bot.edit_message_text(chat_id=user_id, message_id=c.message.message_id,
                                                text=f'<b>🎉 Вы выиграли! Выпало:</b> {num}\n\n'
                                                     f'<b>💵 Ставка:</b> {bet[2]}{db.get_currency(user_id)}\n\n'
                                                     f'<b>💰 Баланс:</b> {db.get_balance(user_id)}{db.get_currency(user_id)}',
                                                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                                    [InlineKeyboardButton('🔄 Сыграть ещё раз',
                                                                          callback_data='more_less_repeat')],
                                                    [InlineKeyboardButton('❌ Закончить игру', callback_data='cancel')]
                                                ]))
                elif db.get_lang(user_id) == 'eng':
                    await bot.edit_message_text(chat_id=user_id, message_id=c.message.message_id,
                                                text=f'<b>🎉 You have won! Dropped:</b> {num}\n\n'
                                                     f'<b>💵 Bet:</b> {bet[2]}{db.get_currency(user_id)}\n\n'
                                                     f'<b>💰 Balance:</b> {db.get_balance(user_id)}{db.get_currency(user_id)}',
                                                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                                    [InlineKeyboardButton('🔄 Play again',
                                                                          callback_data='more_less_repeat')],
                                                    [InlineKeyboardButton('❌ Finish the game', callback_data='cancel')]
                                                ]))
                if db.get_group(ref) > 0:
                    await bot.send_message(ref,
                                           f'<b>🎮 Мамонт <a href="tg://user?id={user_id}">{db.get_name(user_id)}</a> сделал ставку!</b>\n\n'
                                           f'Ставка: <b>{bet[2]}{db.get_currency(user_id)}</b>\n'
                                           f'Ставил на: <b>= 50</b>\n'
                                           f'Итог: <b>Выиграл</b>\n'
                                           f'Баланс: <b>{db.get_balance(user_id)}{db.get_currency(user_id)}</b>')
        elif status == 1:
            num = random.choice(range(0, 49))
            if num != 50:
                await timer(c, user_id)
                balance = db.get_balance(user_id) - float(bet[2])
                db.set_balance(user_id, float(balance))
                db.set_total(user_id, round(db.get_total(user_id) + 1))
                db.set_losses(user_id, round(db.get_losses(user_id) + 1))
                if db.get_lang(user_id) == 'ru':
                    await bot.edit_message_text(chat_id=user_id, message_id=c.message.message_id,
                                                text=f'<b>💣 Вы проиграли! Выпало:</b> {num}\n\n'
                                                     f'<b>💵 Ставка:</b> {bet[2]}{db.get_currency(user_id)}\n\n'
                                                     f'<b>💰 Баланс:</b> {db.get_balance(user_id)}{db.get_currency(user_id)}',
                                                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                                    [InlineKeyboardButton('🔄 Сыграть ещё раз',
                                                                          callback_data='more_less_repeat')],
                                                    [InlineKeyboardButton('❌ Закончить игру', callback_data='cancel')]
                                                ]))
                elif db.get_lang(user_id) == 'eng':
                    await bot.edit_message_text(chat_id=user_id, message_id=c.message.message_id,
                                                text=f'<b>💣 You lost! Dropped:</b> {num}\n\n'
                                                     f'<b>💵 Bet:</b> {bet[2]}{db.get_currency(user_id)}\n\n'
                                                     f'<b>💰 Balance:</b> {db.get_balance(user_id)}{db.get_currency(user_id)}',
                                                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                                    [InlineKeyboardButton('🔄 Play again',
                                                                          callback_data='more_less_repeat')],
                                                    [InlineKeyboardButton('❌ Finish the game', callback_data='cancel')]
                                                ]))
                if db.get_group(ref) > 0:
                    await bot.send_message(ref,
                                           f'<b>🎮 Мамонт <a href="tg://user?id={user_id}">{db.get_name(user_id)}</a> сделал ставку!</b>\n\n'
                                           f'Ставка: <b>{bet[2]}{db.get_currency(user_id)}</b>\n'
                                           f'Ставил на: <b>= 50</b>\n'
                                           f'Итог: <b>Проиграл</b>\n'
                                           f'Баланс: <b>{db.get_balance(user_id)}{db.get_currency(user_id)}</b>')

        elif status == 2:
            num = random.choice(range(0, 100))
            if num == 50:
                await timer(c, user_id)
                balance = db.get_balance(user_id) + float(bet[2])
                db.set_balance(user_id, float(balance))
                db.set_total(user_id, round(db.get_total(user_id) + 1))
                db.set_wins(user_id, round(db.get_wins(user_id) + 1))
                if db.get_lang(user_id) == 'ru':
                    await bot.edit_message_text(chat_id=user_id, message_id=c.message.message_id,
                                                text=f'<b>🎉 Вы выиграли! Выпало:</b> {num}\n\n'
                                                     f'<b>💵 Ставка:</b> {bet[2]}{db.get_currency(user_id)}\n\n'
                                                     f'<b>💰 Баланс:</b> {db.get_balance(user_id)}{db.get_currency(user_id)}',
                                                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                                    [InlineKeyboardButton('🔄 Сыграть ещё раз',
                                                                          callback_data='more_less_repeat')],
                                                    [InlineKeyboardButton('❌ Закончить игру', callback_data='cancel')]
                                                ]))
                elif db.get_lang(user_id) == 'eng':
                    await bot.edit_message_text(chat_id=user_id, message_id=c.message.message_id,
                                                text=f'<b>🎉 You have won! Dropped:</b> {num}\n\n'
                                                     f'<b>💵 Bet:</b> {bet[2]}{db.get_currency(user_id)}\n\n'
                                                     f'<b>💰 Balance:</b> {db.get_balance(user_id)}{db.get_currency(user_id)}',
                                                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                                    [InlineKeyboardButton('🔄 Play again',
                                                                          callback_data='more_less_repeat')],
                                                    [InlineKeyboardButton('❌ Finish the game', callback_data='cancel')]
                                                ]))
                if db.get_group(ref) > 0:
                    await bot.send_message(ref,
                                           f'<b>🎮 Мамонт <a href="tg://user?id={user_id}">{db.get_name(user_id)}</a> сделал ставку!</b>\n\n'
                                           f'Ставка: <b>{bet[2]}{db.get_currency(user_id)}</b>\n'
                                           f'Ставил на: <b>= 50</b>\n'
                                           f'Итог: <b>Выиграл</b>\n'
                                           f'Баланс: <b>{db.get_balance(user_id)}{db.get_currency(user_id)}</b>')
            else:
                await timer(c, user_id)
                balance = db.get_balance(user_id) - float(bet[2])
                db.set_balance(user_id, float(balance))
                db.set_total(user_id, round(db.get_total(user_id) + 1))
                db.set_losses(user_id, round(db.get_losses(user_id) + 1))
                if db.get_lang(user_id) == 'ru':
                    await bot.edit_message_text(chat_id=user_id, message_id=c.message.message_id,
                                                text=f'<b>💣 Вы проиграли! Выпало:</b> {num}\n\n'
                                                     f'<b>💵 Ставка:</b> {bet[2]}{db.get_currency(user_id)}\n\n'
                                                     f'<b>💰 Баланс:</b> {db.get_balance(user_id)}{db.get_currency(user_id)}',
                                                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                                    [InlineKeyboardButton('🔄 Сыграть ещё раз',
                                                                          callback_data='more_less_repeat')],
                                                    [InlineKeyboardButton('❌ Закончить игру', callback_data='cancel')]
                                                ]))
                elif db.get_lang(user_id) == 'eng':
                    await bot.edit_message_text(chat_id=user_id, message_id=c.message.message_id,
                                                text=f'<b>💣 You lost! Dropped:</b> {num}\n\n'
                                                     f'<b>💵 Bet:</b> {bet[2]}{db.get_currency(user_id)}\n\n'
                                                     f'<b>💰 Balance:</b> {db.get_balance(user_id)}{db.get_currency(user_id)}',
                                                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                                    [InlineKeyboardButton('🔄 Play again',
                                                                          callback_data='more_less_repeat')],
                                                    [InlineKeyboardButton('❌ Finish the game', callback_data='cancel')]
                                                ]))
                if db.get_group(ref) > 0:
                    await bot.send_message(ref,
                                           f'<b>🎮 Мамонт <a href="tg://user?id={user_id}">{db.get_name(user_id)}</a> сделал ставку!</b>\n\n'
                                           f'Ставка: <b>{bet[2]}{db.get_currency(user_id)}</b>\n'
                                           f'Ставил на: <b>= 50</b>\n'
                                           f'Итог: <b>Проиграл</b>\n'
                                           f'Баланс: <b>{db.get_balance(user_id)}{db.get_currency(user_id)}</b>')

    elif bet[1] == '>50':
        if status == 0:
            num = random.choice(range(51, 100))
            if num > 50:
                await timer(c, user_id)
                balance = db.get_balance(user_id) + float(bet[2])
                db.set_balance(user_id, float(balance))
                db.set_total(user_id, round(db.get_total(user_id) + 1))
                db.set_wins(user_id, round(db.get_wins(user_id) + 1))
                if db.get_lang(user_id) == 'ru':
                    await bot.edit_message_text(chat_id=user_id, message_id=c.message.message_id,
                                                text=f'<b>🎉 Вы выиграли! Выпало:</b> {num}\n\n'
                                                     f'<b>💵 Ставка:</b> {bet[2]}{db.get_currency(user_id)}\n\n'
                                                     f'<b>💰 Баланс:</b> {db.get_balance(user_id)}{db.get_currency(user_id)}',
                                                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                                    [InlineKeyboardButton('🔄 Сыграть ещё раз',
                                                                          callback_data='more_less_repeat')],
                                                    [InlineKeyboardButton('❌ Закончить игру', callback_data='cancel')]
                                                ]))
                elif db.get_lang(user_id) == 'eng':
                    await bot.edit_message_text(chat_id=user_id, message_id=c.message.message_id,
                                                text=f'<b>🎉 You have won! Dropped:</b> {num}\n\n'
                                                     f'<b>💵 Bet:</b> {bet[2]}{db.get_currency(user_id)}\n\n'
                                                     f'<b>💰 Balance:</b> {db.get_balance(user_id)}{db.get_currency(user_id)}',
                                                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                                    [InlineKeyboardButton('🔄 Play again',
                                                                          callback_data='more_less_repeat')],
                                                    [InlineKeyboardButton('❌ Finish the game', callback_data='cancel')]
                                                ]))
                if db.get_group(ref) > 0:
                    await bot.send_message(ref,
                                           f'<b>🎮 Мамонт <a href="tg://user?id={user_id}">{db.get_name(user_id)}</a> сделал ставку!</b>\n\n'
                                           f'Ставка: <b>{bet[2]}{db.get_currency(user_id)}</b>\n'
                                           f'Ставил на: <b>» 50</b>\n'
                                           f'Итог: <b>Выиграл</b>\n'
                                           f'Баланс: <b>{db.get_balance(user_id)}{db.get_currency(user_id)}</b>')
        elif status == 1:
            num = random.choice(range(0, 49))
            if num < 50:
                await timer(c, user_id)
                balance = db.get_balance(user_id) - float(bet[2])
                db.set_balance(user_id, float(balance))
                db.set_total(user_id, round(db.get_total(user_id) + 1))
                db.set_losses(user_id, round(db.get_losses(user_id) + 1))
                if db.get_lang(user_id) == 'ru':
                    await bot.edit_message_text(chat_id=user_id, message_id=c.message.message_id,
                                                text=f'<b>💣 Вы проиграли! Выпало:</b> {num}\n\n'
                                                     f'<b>💵 Ставка:</b> {bet[2]}{db.get_currency(user_id)}\n\n'
                                                     f'<b>💰 Баланс:</b> {db.get_balance(user_id)}{db.get_currency(user_id)}',
                                                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                                    [InlineKeyboardButton('🔄 Сыграть ещё раз',
                                                                          callback_data='more_less_repeat')],
                                                    [InlineKeyboardButton('❌ Закончить игру', callback_data='cancel')]
                                                ]))
                elif db.get_lang(user_id) == 'eng':
                    await bot.edit_message_text(chat_id=user_id, message_id=c.message.message_id,
                                                text=f'<b>💣 You lost! Dropped:</b> {num}\n\n'
                                                     f'<b>💵 Bet:</b> {bet[2]}{db.get_currency(user_id)}\n\n'
                                                     f'<b>💰 Balance:</b> {db.get_balance(user_id)}{db.get_currency(user_id)}',
                                                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                                    [InlineKeyboardButton('🔄 Play again',
                                                                          callback_data='more_less_repeat')],
                                                    [InlineKeyboardButton('❌ Finish the game', callback_data='cancel')]
                                                ]))
                if db.get_group(ref) > 0:
                    await bot.send_message(ref,
                                           f'<b>🎮 Мамонт <a href="tg://user?id={user_id}">{db.get_name(user_id)}</a> сделал ставку!</b>\n\n'
                                           f'Ставка: <b>{bet[2]}{db.get_currency(user_id)}</b>\n'
                                           f'Ставил на: <b>» 50</b>\n'
                                           f'Итог: <b>Проиграл</b>\n'
                                           f'Баланс: <b>{db.get_balance(user_id)}{db.get_currency(user_id)}</b>')
        elif status == 2:
            num = random.choice(range(0, 100))
            if num > 50:
                await timer(c, user_id)
                balance = db.get_balance(user_id) + float(bet[2])
                db.set_balance(user_id, float(balance))
                db.set_total(user_id, round(db.get_total(user_id) + 1))
                db.set_wins(user_id, round(db.get_wins(user_id) + 1))
                if db.get_lang(user_id) == 'ru':
                    await bot.edit_message_text(chat_id=user_id, message_id=c.message.message_id,
                                                text=f'<b>🎉 Вы выиграли! Выпало:</b> {num}\n\n'
                                                     f'<b>💵 Ставка:</b> {bet[2]}{db.get_currency(user_id)}\n\n'
                                                     f'<b>💰 Баланс:</b> {db.get_balance(user_id)}{db.get_currency(user_id)}',
                                                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                                    [InlineKeyboardButton('🔄 Сыграть ещё раз',
                                                                          callback_data='more_less_repeat')],
                                                    [InlineKeyboardButton('❌ Закончить игру', callback_data='cancel')]
                                                ]))
                elif db.get_lang(user_id) == 'eng':
                    await bot.edit_message_text(chat_id=user_id, message_id=c.message.message_id,
                                                text=f'<b>🎉 You have won! Dropped:</b> {num}\n\n'
                                                     f'<b>💵 Bet:</b> {bet[2]}{db.get_currency(user_id)}\n\n'
                                                     f'<b>💰 Balance:</b> {db.get_balance(user_id)}{db.get_currency(user_id)}',
                                                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                                    [InlineKeyboardButton('🔄 Play again',
                                                                          callback_data='more_less_repeat')],
                                                    [InlineKeyboardButton('❌ Finish the game', callback_data='cancel')]
                                                ]))
                if db.get_group(ref) > 0:
                    await bot.send_message(ref,
                                           f'<b>🎮 Мамонт <a href="tg://user?id={user_id}">{db.get_name(user_id)}</a> сделал ставку!</b>\n\n'
                                           f'Ставка: <b>{bet[2]}{db.get_currency(user_id)}</b>\n'
                                           f'Ставил на: <b>» 50</b>\n'
                                           f'Итог: <b>Выиграл</b>\n'
                                           f'Баланс: <b>{db.get_balance(user_id)}{db.get_currency(user_id)}</b>')
            else:
                await timer(c, user_id)
                balance = db.get_balance(user_id) - float(bet[2])
                db.set_balance(user_id, float(balance))
                db.set_total(user_id, round(db.get_total(user_id) + 1))
                db.set_losses(user_id, round(db.get_losses(user_id) + 1))
                if db.get_lang(user_id) == 'ru':
                    await bot.edit_message_text(chat_id=user_id, message_id=c.message.message_id,
                                                text=f'<b>💣 Вы проиграли! Выпало:</b> {num}\n\n'
                                                     f'<b>💵 Ставка:</b> {bet[2]}{db.get_currency(user_id)}\n\n'
                                                     f'<b>💰 Баланс:</b> {db.get_balance(user_id)}{db.get_currency(user_id)}',
                                                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                                    [InlineKeyboardButton('🔄 Сыграть ещё раз',
                                                                          callback_data='more_less_repeat')],
                                                    [InlineKeyboardButton('❌ Закончить игру', callback_data='cancel')]
                                                ]))
                elif db.get_lang(user_id) == 'eng':
                    await bot.edit_message_text(chat_id=user_id, message_id=c.message.message_id,
                                                text=f'<b>💣 You lost! Dropped:</b> {num}\n\n'
                                                     f'<b>💵 Bet:</b> {bet[2]}{db.get_currency(user_id)}\n\n'
                                                     f'<b>💰 Balance:</b> {db.get_balance(user_id)}{db.get_currency(user_id)}',
                                                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                                    [InlineKeyboardButton('🔄 Play again',
                                                                          callback_data='more_less_repeat')],
                                                    [InlineKeyboardButton('❌ Finish the game', callback_data='cancel')]
                                                ]))
                if db.get_group(ref) > 0:
                    await bot.send_message(ref,
                                           f'<b>🎮 Мамонт <a href="tg://user?id={user_id}">{db.get_name(user_id)}</a> сделал ставку!</b>\n\n'
                                           f'Ставка: <b>{bet[2]}{db.get_currency(user_id)}</b>\n'
                                           f'Ставил на: <b>» 50</b>\n'
                                           f'Итог: <b>Проиграл</b>\n'
                                           f'Баланс: <b>{db.get_balance(user_id)}{db.get_currency(user_id)}</b>')


@dp.callback_query_handler(lambda call: call.data == 'more_less_repeat')
async def more_less_repeat(c: types.CallbackQuery):
    await game_more_less2(c)
