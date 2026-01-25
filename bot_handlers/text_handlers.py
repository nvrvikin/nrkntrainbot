from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from data.callbacks import CB_CORRECT_ANSWER, CB_START_QUIZ, CB_WRONG_ANSWER
from db_interactions import get_quiz_index, get_resluts, get_user_nickname, update_user_nickname, get_user_state, update_quiz_index, update_quiz_results, update_user_state
from generate_answer import generate_correct_answer, generate_wrong_answer, show_main_menu
from state.states import STATE_MAIN_MENU, STATE_NO_NICKNAME 

from data.questions import quiz_data
from data.phrases import PHRASE_GREET
from utils.utils import get_question, new_quiz

from state.state import UserForm

router = Router()

def check_nickname(message):
    pass

# ОБРАБОТКА /start
@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_nickname = await get_user_nickname(user_id)
    await message.answer(PHRASE_GREET)
    if not user_nickname:
        await message.answer('Требуется придумать ник до 20 символов для отображения в общих результатах')
        await update_user_state(user_id, STATE_NO_NICKNAME)
        await state.set_state(UserForm.no_nickname)
    if user_nickname:
        await update_user_state(user_id, STATE_MAIN_MENU)
        await state.set_state(UserForm.main_menu)

@router.message(UserForm.no_nickname)
async def process_nickname(message: types.Message, state: FSMContext):
    username = message.text.strip()
    
    # Валидация
    if len(username) > 20:
        await message.answer("Слишком длинный ник! Максимум 20 символов.")
        return
    if len(username) < 3:
        await message.answer("Слишком короткий ник! Минимум 3 символа.")
        return
    
    await update_user_nickname(message.from_user.id, username)
    
    await state.set_state(UserForm.main_menu)
    
    await message.answer(f"Отлично, {username}!")

    await show_main_menu(message)

# ОБРАБОТКА /quiz
@router.message(UserForm.main_menu)
@router.callback_query(F.data == CB_START_QUIZ)
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

    await message.answer("Не понял ваше сообщение")

