from aiogram import F, Router, types
from aiogram.filters import Command

from callbacks import CB_CORRECT_ANSWER, CB_WRONG_ANSWER
from db_interactions import get_quiz_index, get_resluts, get_user_nickname, get_user_state, update_quiz_index, update_quiz_results, update_user_state
from generate_answer import generate_correct_answer, generate_wrong_answer
from state.state import state_changed
from state.states import STATE_MAIN_MENU, STATE_NO_NICKNAME 

from questions import quiz_data
from utils.utils import get_question, new_quiz

router = Router()

# ОБРАБОТКА /start
@router.message(Command("start"))
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    user_nickname = await get_user_nickname(user_id)
    await message.answer("Здравствуйте! Здесь можно несколько раз пройти квиз из 10 вопросов. Вопросы всегда одни и те же.")
    if not user_nickname:
        await update_user_state(user_id, STATE_NO_NICKNAME)
        state_changed(user_id, message)
    if user_nickname:
        await update_user_state(user_id, STATE_MAIN_MENU)
        state_changed(user_id, message)

# ОБРАБОТКА /quiz
@router.message(F.text=="Начать игру")
@router.message(Command("quiz"))
async def cmd_quiz(message: types.Message):
    await message.answer(f"Начинаем квиз!")
    await new_quiz(message)

# ОБРАБОТКА ВЕРНОГО ОТВЕТА
@router.callback_query(F.data == CB_CORRECT_ANSWER)
async def right_answer(callback: types.CallbackQuery):

    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )

    current_question_index = await get_quiz_index(callback.from_user.id)
    correct_option = quiz_data[current_question_index]['correct_option']

    result_answer = generate_correct_answer(quiz_data[current_question_index]['options'][correct_option])
    await callback.message.answer(result_answer, parse_mode="HTML")

    # 1 для верных
    await update_quiz_results(callback.from_user.id, current_question_index, 1)
    # Обновление номера текущего вопроса в базе данных
    current_question_index += 1
    await update_quiz_index(callback.from_user.id, current_question_index)

    if current_question_index < len(quiz_data):
        await get_question(callback.message, callback.from_user.id)
    else:
        results = await get_resluts(callback.from_user.id)
        print(results)
        await callback.message.answer(f"Это был последний вопрос. Квиз завершен! { results }", parse_mode="HTML")

# ОБРАБОТКА НЕВЕРНОГО ОТВЕТА
@router.callback_query(F.data == CB_WRONG_ANSWER)
async def wrong_answer(callback: types.CallbackQuery):
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )

    # Получение текущего вопроса из словаря состояний пользователя
    current_question_index = await get_quiz_index(callback.from_user.id)
    correct_option = quiz_data[current_question_index]['correct_option']

    # Генерация и отправка ответа
    result_answer = generate_wrong_answer(quiz_data[current_question_index]['options'][correct_option])
    await callback.message.answer(result_answer, parse_mode="HTML")

    # 0 для неверных
    await update_quiz_results(callback.from_user.id, current_question_index, 0)
    # Обновление номера текущего вопроса в базе данных
    current_question_index += 1
    await update_quiz_index(callback.from_user.id, current_question_index)

    if current_question_index < len(quiz_data):
        await get_question(callback.message, callback.from_user.id)
    else:
        results = await get_resluts(callback.from_user.id)
        print(results)
        await callback.message.answer(f"Это был последний вопрос. Квиз завершен! { results }", parse_mode="HTML")

@router.message()
async def handle_all_text_messages(message: types.Message):
    user_id = message.from_user.id
    current_state = await get_user_state(user_id)
    
    if current_state == STATE_NO_NICKNAME:
        message.text
        # Обработка установки username
        pass
    else:
        await message.answer("Не понял ваше сообщение")