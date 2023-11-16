from aiogram import types,Dispatcher
from config import bot, ADMIN
import kb
from db.commands import Database

start_text = ("Здравствуйте! Я бот, который соберет и отправит в нужный канал ваш товар."
            "\n\nИспользуйте команду /new для создания нового товара."
            "Просто отправьте мне текст после команды /new, и я начну собирать информацию."
            "Если при отправке информации про ваш товар или номер телефона выйдет ошибка"
            "нажмите на кнопку __cancel__ для очистки анкеты и заполните ее заново"
            "Удачи в управлении вашими товарами!")

async def start(message: types.Message):
    await message.answer(text=start_text, reply_markup=kb.start_markup())

async def find_contact(message:types.Message):
    if message.from_user.id in ADMIN:
        form = Database().sql_select_user_form_by_telegram_id(message.text)[0]
        if form is not None:
            link = f"\n\n@ + {form['username']}"
            link = link if link is not None else ""
            await bot.send_photo(chat_id=message.from_user.id,photo=form['photo'],
                                 caption=f"{form['hash']}\n\n доп инфа: {form['text']}\n\nтел номер: +{form['phone_num_address']}{link}")
        else:
            await message.answer('товара с таким хэшом не найдено')
    else:
        await message.answer("доставать товары по хэшу могут только админы")

def register_handlers_client(dp:Dispatcher):
    dp.register_message_handler(start,commands=['start'])
    dp.register_message_handler(find_contact, lambda word:word.text.startswith("#"))
