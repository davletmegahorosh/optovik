from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import bot
import uuid
import kb
from db.commands import Database

class FSMadmin(StatesGroup):
    check_photo_text = State()
    # text_photo = State()
    phone_num_address = State()
    submit = State()

async def start(message: types.Message, state:FSMContext):
    if message.chat.type == 'private':
            gen_id = str(uuid.uuid1())
            async with state.proxy() as data:
                data['id'] = message.from_user.id
                data['username'] = message.from_user.username
                data['hash'] = '#' + gen_id.replace("-", '')
            await FSMadmin.check_photo_text.set()
            await message.answer('отправьте 1 фото вашего товара и как подпись к нему напишите описание',
                                 reply_markup=kb.cancel())
    else:
        await message.answer('пиши в личке!!!')

async def text(message: types.Message, state: FSMContext):
    if message.photo and message.caption:
        print('norm')
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
            data['text'] = message.caption
        await FSMadmin.next()
        await message.answer(f'напишите ваш номер телефона\n'
                             f'пример: +996 123 456 789\n'
                             f'или: 0 123 456 789\n\n'
                             f'и адрес в одном сообщении')
    elif message.photo and not message.caption:
        await message.answer('добавьте описание вместе с фото')

async def phone_num(message:types.Message, state:FSMContext):
    check_phone = str(message.text).replace(' ','')
    verified_phone = False
    if check_phone.startswith('0') and (check_phone[:9]).isdigit():
        check_phone = check_phone[:9]
        verified_phone = True
    elif check_phone.startswith('+996') and (check_phone[1:12]).isdigit():
        check_phone = check_phone[:12]
        verified_phone = True
    else:
        await message.answer(f'напишите ваш номер телефона\n'
                             f'пример: +996 123 456 789\n'
                             f'или: 0 123 456 789'
                             f'и адесс в одном сообщении')
    if verified_phone and len(message.text.replace(" ","")) > len(check_phone):
        async with state.proxy() as data:
            data['phone_num_address'] = message.text
            await message.answer_photo(data['photo'], caption=f"{data['text']}\n\n"
                                                              f"{data['phone_num_address']}")
        await FSMadmin.next()
        await message.answer('Всё нормально?', reply_markup=kb.yes_no())


async def submit(message: types.Message, state: FSMContext):
    if message.text.lower() == 'да':
        async with state.proxy() as data:
            Database().sql_insert_user_form(data['username'], data['hash'],
                                            data['text'], data['phone_num_address'], data['photo'])
        await bot.send_photo(chat_id=661114436 ,photo=data['photo'], caption=f"{data['hash']}"
                                                                            f"\n\n{data['text']}")
        await state.finish()
        await message.answer('Мы сохранили ваш товар', reply_markup=kb.start_markup())
    elif message.text.lower == 'нет':
        await state.finish()
        await message.answer('удалили все', reply_markup=kb.start_markup())
    else:
        await message.answer('выберите "да" или "нет" ', reply_markup=kb.yes_no())


async def cancel_fsm(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        await message.answer('удалили все', reply_markup=kb.start_markup())


def register_handlers_fsm(dp: Dispatcher):
    dp.register_message_handler(cancel_fsm, Text(equals='cancel', ignore_case=True), state="*")

    dp.register_message_handler(start, commands=['new'])
    dp.register_message_handler(text, state=FSMadmin.check_photo_text,content_types=['photo'])
    dp.register_message_handler(phone_num, state=FSMadmin.phone_num_address)
    dp.register_message_handler(submit, state=FSMadmin.submit)
