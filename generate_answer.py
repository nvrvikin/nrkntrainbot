from random import randint
from aiogram import types
from data.constatns import CORRECT_PHRASES, WRONG_PHRASES, PRE_WRONG_PHRASE, EMOJI_CORRECT, EMOJI_WRONG
from keyboards import generate_main_menu_keyboard


def generate_correct_answer(correct_answer):
    rand_answer = randint(0, len(CORRECT_PHRASES) - 1)
    return f"{ EMOJI_CORRECT } <i>{ CORRECT_PHRASES[rand_answer] }</i>\n<u>{ correct_answer }</u>"

def generate_wrong_answer(correct_answer):
    rand_answer = randint(0, len(WRONG_PHRASES) - 1)
    return f"{ EMOJI_WRONG } <i>{ WRONG_PHRASES[rand_answer] }</i>\n{ PRE_WRONG_PHRASE } <u>{ correct_answer }</u>"

def generate_results_list(results):
    if not len(results):
        return 'Нет результатов, пройдите тест ещё раз.'
    response = '\n\n<b>Твой результат:</b>\n'
    for r in results:
        # Пробелы, чтобы выглядело ровнее
        human_count = r[1] + 1
        digit = f'{ human_count }  ' if human_count < 10 else f'{ human_count }'
        # Обозначаем эмодзи в зависимости от ответа
        response += f'{ digit } - { EMOJI_CORRECT if r[2] > 0 else EMOJI_WRONG }\n'
    return response

async def generate_top_results_list(results, get_user_nickname):
    if not len(results):
        return 'Нет топа. Похоже, ещё никто не прошёл квиз.'
    
    user_scores = {}

    for r in results:
        if r[0] not in user_scores:
            user_scores[r[0]] = r[2]
        else:
            user_scores[r[0]] += r[2]
            pass
    
    sorted_users = sorted(user_scores.items(), key=lambda x: x[1], reverse=True)

    results_list = ''

    for u in sorted_users:
        nickname = await get_user_nickname(u[0])
        if nickname:
            results_list += f'<i>{ nickname }</i>: {u[1]}\n'

    response = '\n\n<b>Топ результатов:</b>\n\n'
    return f'{response}{results_list}'

async def show_main_menu(message: types.Message, nickname: str):
    kb = generate_main_menu_keyboard()
    await message.answer(f"<b>{ nickname }</b>, На ваш выбор:", parse_mode="HTML", reply_markup=kb)