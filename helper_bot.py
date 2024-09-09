import logging
import time
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.storage import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from Casino import sql

storage = MemoryStorage()
bot = Bot('7425091205:AAG9cbFTGjjJIF-g84kAaPuD8dsTHFhD7FY', parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)
db1 = sqll.Database('Casino/db.db')
logging.basicConfig(level=logging.INFO)
admins = [5128725679]
topnumbs = ['╠ 1','╠ 2','╠ 3','╠ 4','╠ 5','╠ 6','╠ 7','╠ 8','╠ 9','╚ 10']
msgdel = []

async def deletermsg():
    global msgdel

    while True:
        for m in msgdel:
            await bot.delete_message(m[0], m[1])
            await asyncio.sleep(1)
        await asyncio.sleep(5)

@dp.message_handler(commands=['start'], state='*')
async def start(m: types.Message, state=FSMContext):
    msgdel.append([m.chat.id, m.message_id])
    text = f'<b><b>🌿 BitFinex TEAM</b>\n\n<a href="https://t.me/c/1665993286/8426"><b>🔗 Закреп</b></a></b>\n\n<b>/work — статус проекта</b>\n<b>/topc — топ воркеров казино</b>\n<b>/topt — топ воркеров трейд</b>\n<b>/card — карты для прямиков</b>'

    m = await m.answer(text, disable_web_page_preview=True)
    msgdel.append([m.chat.id, m.message_id])

@dp.message_handler(content_types=['new_chat_members'])
async def on_user_joined(m: types.Message):
    await m.delete()
    m = await m.answer(f'<b>👋 Привет, <a href="https://t.me/{m.from_user.username}">{m.from_user.first_name}</a>!</b>\n\n<b>🎰 Казино\n╚ @Dragonmoney_robot\n\n🤝 Пригласи друга\n╚ @Playboymansion_robot</b>', reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                 [InlineKeyboardButton('🔗 Закреп', url='https://t.me/c/1665993286/8426')]
                             ]),disable_web_page_preview=True)
    msgdel.append([m.chat.id, m.message_id])

@dp.message_handler(commands=['top'], state='*')
async def top_casino(m: types.Message, state=FSMContext):
    text = f'<b>🚀 Топ воркеров за всё время:</b>\n\n<b>🎰 Казино</b>\n'
    for c, v in enumerate(db1.get_top()):
        text += f'{topnumbs[c]}. <b><a href="https://t.me/{v[0]}">{v[0]}</a></b> - {v[1]} ₽\n'


    m = await m.answer(text, disable_web_page_preview=True)
    msgdel.append([m.chat.id, m.message_id])

@dp.message_handler(commands=['mute'], is_chat_admin=True)
async def cmd_mute(message: types.Message):
    msgdel.append(message)
    user = message.from_user
    reply = message.reply_to_message
    if reply:
        replyuser = reply.from_user
        args = message.get_args()
        if args:
            try:
                n = ''
                t = ''
                for _ in args:
                    if _.isdigit():
                        n += _
                    else:
                        t += _
                yeah = f"{n}"
                if t == "m":
                    n = int(n) * 60
                    yeah += " минут"
                elif t == "h":
                    n = int(n) * 3600
                    yeah += " часов"
                elif t == "d":
                    n = int(n) * 86400
                    yeah += " дней"
            except ValueError: return await message.reply("Нет аргументов.")
            if replyuser.id == (await bot.get_me()).id:
                return
            if (await bot.get_chat_member(message.chat.id, replyuser.id)).status not in ['owner', 'administrator']:
                m = await bot.send_message(message.chat.id, f"<b>🔰 {replyuser.first_name}</b> получил мут на {yeah}!\n\n"
                                                        f"💢 Выдал: <b>{user.first_name}</b>")
                msgdel.append([m.chat.id, m.message_id])
                await bot.restrict_chat_member(message.chat.id, replyuser.id,
                                   until_date=time.time() + int(n),
                                   can_send_messages=False)

        else:
            m = await message.reply("На сколько?")
            msgdel.append([m.chat.id, m.message_id])
    else:
        m = await message.reply("Ползователь не найден!")
        msgdel.append([m.chat.id, m.message_id])

@dp.message_handler(commands=['unmute'], is_chat_admin=True)
async def cmd_unmute(message: types.Message):
    msgdel.append(message)
    user = message.from_user
    reply = message.reply_to_message
    if reply:
        replyuser = reply.from_user
        if replyuser.id == (await bot.get_me()).id:
            return
        m = await bot.send_message(message.chat.id, f"<b>🔰 {replyuser.first_name}</b> теперь не в муте!\n\n"
                                                f"💢 Снял: <b>{user.first_name}</b>")
        msgdel.append([m.chat.id, m.message_id])
        await bot.restrict_chat_member(message.chat.id, replyuser.id,
                                   can_send_messages=True,
                                   can_send_media_messages=True,
                                   can_send_other_messages=True,
                                   can_add_web_page_previews=True)
    else:
        m = await message.reply("Пользователь не найден")
        msgdel.append([m.chat.id, m.message_id])

@dp.message_handler(commands=['ban'], is_chat_admin=True)
async def cmd_ban(message: types.Message):
    msgdel.append(message)
    user = message.from_user
    reply = message.reply_to_message
    if reply:
        replyuser = reply.from_user
        if replyuser.id == (await bot.get_me()).id:
            return
        if (await bot.get_chat_member(message.chat.id, replyuser.id)).status not in ['owner', 'administrator']:
            m = await bot.send_message(message.chat.id, f"<b>🔰 {replyuser.first_name}</b> получил бан!\n\n"
                                                   f"💢 Выдал: <b>{user.first_name}</b>")
            msgdel.append([m.chat.id, m.message_id])
            await bot.kick_chat_member(message.chat.id, replyuser.id)
    else:
        m = await message.reply("Кого банить то?")
        msgdel.append([m.chat.id, m.message_id])

@dp.message_handler(commands=['unban'], is_chat_admin=True)
async def cmd_unban(message: types.Message):
    msgdel.append(message)
    user = message.from_user
    reply = message.reply_to_message
    if reply:
        replyuser = reply.from_user
        if replyuser.id == (await bot.get_me()).id:
            return
        m = await bot.send_message(message.chat.id, f"<b>🔰 {replyuser.first_name}</b> теперь не в бане!\n\n"
                                                f"💢 Снял: <b>{user.first_name}</b>")
        msgdel.append([m.chat.id, m.message_id])
        await bot.unban_chat_member(message.chat.id, replyuser.id)
    else:
        m = await message.reply("Кому снять бан то?")
        msgdel.append([m.chat.id, m.message_id])

@dp.message_handler(commands=['work'], state='*')
async def work(m: types.Message, state=FSMContext):
    msgdel.append([m.chat.id, m.message_id])
    text = f'<b>🌿 BitFinex TEAM</b>\n\n<b>🎰 Казино\n╠ @Dragonmoney_robot\n╚ Статус: {db1.get_project_status()}</b>'

    m = await m.answer(text, disable_web_page_preview=True)
    msgdel.append([m.chat.id, m.message_id])

@dp.message_handler(commands=['set_status'], state='*')
async def status(m: types.Message, state=FSMContext):
    msgdel.append([m.chat.id, m.message_id])
    if m.from_user.id in admins:
        text = f'<b>⚜️ Новый статус казино: </b> {m.text[13:]}'

        db1.set_project_status(m.text[13:])

        m = await m.answer(text)
        msgdel.append([m.chat.id, m.message_id])

@dp.message_handler(commands=['rules', 'help'], state='*')
async def rules(m: types.Message, state=FSMContext):
    msgdel.append([m.chat.id, m.message_id])
    text = f'<b><b>🌿 BitFinex TEAM</b>\n\n<a href="end_soft"><b>🔗 Закреп</b></a></b>\n\n<b>/work — статус проекта</b>\n<b>/top — топ воркеров</b>\n<b>/card — карты для прямиков</b>'

    await m.answer(text)

    msgdel.append([m.chat.id, m.message_id])

@dp.message_handler(commands=['card'], state='*')
async def card(m: types.Message, state=FSMContext):
    msgdel.append([m.chat.id, m.message_id])
    text = f'<b>💳 Карточки для прямиков:</b>\n\n<b>🇺🇦 UAH: {db1.get_card("UAH") if db1.get_card("UAH") != "" else "❌"}</b>\n<b>🇷🇺 RUB: {db1.get_card("RUB") if db1.get_card("RUB") != "" else "❌"}</b>\n<b>🇪🇺 EUR: {db1.get_card("EUR") if db1.get_card("EUR") != "" else "❌"}</b>'
    await asyncio.sleep(5)

    m = await m.answer(text)
    msgdel.append([m.chat.id, m.message_id])

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    loop = asyncio.get_running_loop()
    nonblocking_task = loop.create_task(deleter())
