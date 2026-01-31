from db_interactions import get_quiz_index, update_quiz_index
from keyboards import generate_options_keyboard
from bot_data.questions import quiz_data

# Начало квиза
async def new_quiz(message, user_id):
    current_question_index = 0
    await update_quiz_index(user_id, current_question_index)
    await get_question(message, user_id)

# Получение вопроса по пользователю и его индексу текущего вопроса
async def get_question(message, user_id):
    # Получение текущего вопроса из словаря состояний пользователя
    current_question_index = await get_quiz_index(user_id)
    correct_index = quiz_data[current_question_index]['correct_option']
    opts = quiz_data[current_question_index]['options']
    kb = generate_options_keyboard(opts, opts[correct_index])
    await message.answer(f"<b>{ quiz_data[current_question_index]['question'] }</b>", parse_mode="HTML", reply_markup=kb)

