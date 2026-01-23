from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

from callbacks import CB_CORRECT_ANSWER, CB_WRONG_ANSWER, CB_START_QUIZ, CB_CHANGE_NICKNAME

# Клавиатура с вариантами ответа на вопрос
def generate_options_keyboard(answer_options, right_answer):
    builder = InlineKeyboardBuilder()

    for option in answer_options:
        builder.add(types.InlineKeyboardButton(
            text=option,
            callback_data=CB_CORRECT_ANSWER if option == right_answer else CB_WRONG_ANSWER)
        )

    builder.adjust(1)
    return builder.as_markup()

def generate_main_menu_keyboard():
    builder = InlineKeyboardBuilder()

    builder.add(types.InlineKeyboardButton(
        text='Начать игру',
        callback_data=CB_START_QUIZ
    ))

    builder.add(types.InlineKeyboardButton(
        text='Изменить никнейм',
        callback_data=CB_CHANGE_NICKNAME
    ))

    builder.add(types.InlineKeyboardButton(
        text='Посмотреть результаты',
        callback_data=CB_CHANGE_NICKNAME
    ))

    return builder.as_markup()