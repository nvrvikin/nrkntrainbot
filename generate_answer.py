from random import randint
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

async def show_main_menu(message):
    kb = generate_main_menu_keyboard()
    await message.answer(f"<b>На ваш выбор:</b>", parse_mode="HTML", reply_markup=kb)