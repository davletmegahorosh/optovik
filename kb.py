from aiogram.types import  ReplyKeyboardMarkup, KeyboardButton
types_list = ["муж одежда" ,"жен одежда" ,"ботинки" ,"игрушки"]

def start_markup():
    new = KeyboardButton('/new')
    start_markup = ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard = True,
        row_width=3
    ).add(new)
    return start_markup
def cancel():
    cancel_but = KeyboardButton('cancel')
    cancel_markup = ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard = True,
        row_width=3
    ).add(cancel_but)
    return cancel_markup

def yes_no():
    yes = KeyboardButton('да')
    no = KeyboardButton('нет')
    yes_no = ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard = True,
        row_width=3
    ).add(yes, no)
    return yes_no


