import logging
import configparser
import time
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.storage import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from Casino import sql as c_sql

settings = configparser.ConfigParser()
settings.read('settings.ini')
storage = MemoryStorage()
bot = Bot(settings['BOT']['Token'], parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)
db_c = c_sql.Database('Casino/db.db')
logging.basicConfig(level=logging.INFO)


class Answers(StatesGroup):
    answer1 = State()
    answer2 = State()
    answer3 = State()


@dp.message_handler(commands=['start'], state='*')
async def start(m: types.Message, state=FSMContext):
    await state.finish()
    user_id = m.from_user.id
    if user_id == int(settings['MAIN']['Admin']):
        return await m.answer('Admin chat set!')
    reg_date = time.strftime('%d/%m/%Y %H:%M:%S')
    login = '0'
    if m.from_user.username is None:
        login = 'None'
    else:
        login = m.from_user.username

    if not db_c.user_exists(user_id):
        db_c.add_user(user_id, login, m.from_user.first_name, m.from_user.last_name, 0, reg_date)

    if db_c.get_group(user_id) >= 1:
        with open('pic.jpg', 'rb') as pic:
            await bot.send_photo(user_id, pic,
                                 '<b>Твоя заявка уже одобрена✅\nДобро пожаловать!\n\n🎰 Казино\n╠ @end_soft\n╚ Меню воркера - кнопка внизу</b>',
                                 reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                     [InlineKeyboardButton('💬 Чат', url='https://t.me/end_soft')],
                                     [InlineKeyboardButton('💸 Выплаты', url='https://t.me/end_soft')],
                                     [InlineKeyboardButton('📚 Мануалы', url='https://t.me/end_soft')]
                                 ]))

    with open('pic.jpg', 'rb') as pic:
        await bot.send_photo(user_id, pic, f'<b>👋 Привет {m.from_user.first_name}!\n\n'
                                           f'Чтобы работать с нами тебе необходимо подать заявку!</b>',
                             reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                 [InlineKeyboardButton('🚀 Погнали', callback_data='start')]
                             ]))


@dp.callback_query_handler(lambda c: c.data == 'start')
async def rules(c: types.CallbackQuery):
    user_id = c.from_user.id
    await bot.edit_message_caption(user_id, c.message.message_id,
                                   caption='<b>📝 Правила проекта, к прочтению ОБЯЗАТЕЛЬНЫ!\n\n'
                                           '🚫 ЗАПРЕЩЕНО:</b>\n'
                                           '<code>- Оскорбление Администрации\n'
                                           '- Выяснение отношений\n'
                                           '- Реклама/Продажа услуг и т.п. без согласования Администрации\n'
                                           '- Кидать воркеров из своей тимы</code>\n',
                                   reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                       [InlineKeyboardButton('✅ Я ознакомлен', callback_data='accept_rules')]
                                   ]))


@dp.callback_query_handler(lambda c: c.data == 'accept_rules')
async def que1(c: types.CallbackQuery):
    user_id = c.from_user.id
    await bot.delete_message(user_id, c.message.message_id)
    await bot.send_message(user_id, '<b>❔ Вопрос первый\n\n'
                                    'Имеешь опыт работы?</b>')
    await Answers.answer1.set()


@dp.message_handler(content_types='text', state=Answers.answer1)
async def answer1(m: types.Message, state=FSMContext):
    user_id = m.from_user.id
    async with state.proxy() as data:
        data['answer1'] = m.text
    await bot.send_message(user_id, '<b>✍️ Записал\n'
                                    '❔ Вопрос второй\n\n'
                                    'В какой сфере работал?</b>')
    await Answers.answer2.set()


@dp.message_handler(content_types='text', state=Answers.answer2)
async def answer2(m: types.Message, state=FSMContext):
    user_id = m.from_user.id
    async with state.proxy() as data:
        data['answer2'] = m.text
    await bot.send_message(user_id, '<b>✍️ Записал\n'
                                    '❔ Вопрос третий\n\n'
                                    'Откуда узнал про нас?</b>')
    await Answers.answer3.set()


@dp.message_handler(content_types='text', state=Answers.answer3)
async def answer3(m: types.Message, state=FSMContext):
    user_id = m.from_user.id
    async with state.proxy() as data:
        data['answer3'] = m.text
        ans1 = data['answer1']
        ans2 = data['answer2']
        ans3 = data['answer3']
        await bot.send_message(user_id, f'<b>✉️ Твоя анкета готова к отправке!</b>\n\n'
                                        f'<b>Опыт работы:</b> {ans1}\n'
                                        f'<b>В какой сфере работал:</b> {ans2}\n'
                                        f'<b>Откуда узнал:</b> {ans3}',
                               reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                   [InlineKeyboardButton('✉️ Отправить', callback_data=f'send={ans1}|{ans2}|{ans3}')],
                                   [InlineKeyboardButton('✍️ Изменить', callback_data='edit')]
                               ]))
        await state.finish()


@dp.callback_query_handler(lambda c: c.data == 'edit')
async def edit(c: types.CallbackQuery):
    await que1(c)


@dp.callback_query_handler(lambda c: c.data.startswith('send'))
async def send(c: types.CallbackQuery):
    user_id = c.from_user.id
    answers = c.data.replace('send=', '').split('|')
    await bot.edit_message_text('<b>✅ Твоя заявка отправлена и ждёт одобрения администрации!</b>', user_id,
                                c.message.message_id)
    await bot.send_message(settings["MAIN"]["Admin"],
                           f'🔥 Новая заявка от - <a href="tg://user?id={user_id}">{c.from_user.first_name} {c.from_user.last_name}</a>\n\n'
                           f'╠ Опыт работы: {answers[0]}\n'
                           f'╠ В какой сфере работал: {answers[1]}\n'
                           f'╚ Откуда узнал: {answers[2]}', reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton('Принять', callback_data=f'accept_form={user_id}')],
            [InlineKeyboardButton('Отклонить', callback_data=f'decline={user_id}')]
        ]))


@dp.callback_query_handler(lambda c: c.data.startswith('accept_form'))
async def accept_form(c: types.CallbackQuery):
    user_id = c.data.replace('accept_form=', '')
    await bot.delete_message(c.from_user.id, c.message.message_id)
    db_c.set_group(user_id, 1)
    with open('pic.jpg', 'rb') as pic:
        await bot.send_photo(user_id, pic,
                             '<b>Твоя заявка одобрена✅\nДобро пожаловать!\n\n🎰 Казино\n╠ @end_soft\n╚ Меню воркера - кнопка внизу</b>',
                             reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                 [InlineKeyboardButton('💬 Чат', url='https://t.me/end_soft')],
                                 [InlineKeyboardButton('💸 Выплаты', url='https://t.me/end_soft')],
                                 [InlineKeyboardButton('📚 Мануалы', url='https://t.me/end_soft')]
                             ]))


@dp.callback_query_handler(lambda c: c.data.startswith('decline'))
async def decline_form(c: types.CallbackQuery):
    user_id = c.data.replace('decline=', '')
    await bot.delete_message(c.from_user.id, c.message.message_id)
    await bot.send_message(user_id, '<b>Твоя заявка отклонена❌\n\nВозможно ты нарушил правила подачи заявки.</b>', )


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
