from aiogram import F, Router, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from bot_handlers.common_functions import check_nickname, main_menu_state
from data.callbacks import CB_CANCEL, CB_CORRECT_ANSWER, CB_START_QUIZ, CB_WRONG_ANSWER
from db_interactions import get_quiz_index, get_resluts, get_user_nickname, update_user_nickname, update_quiz_index, update_quiz_results
from generate_answer import generate_correct_answer, generate_wrong_answer, show_main_menu

from data.questions import quiz_data
from keyboards import generate_change_nickname_keyboard
from utils.utils import get_question, new_quiz

from state.state import UserForm

router = Router()

async def change_nickname_state(message: types.Message, user_id: int, state: FSMContext):
    await state.set_state(UserForm.change_nickname)
    current_nickname = await get_user_nickname(user_id)
    kb = generate_change_nickname_keyboard()
    await message.answer(f'Текущий никнейм: <b>{ current_nickname }</b>. Если хотите изменить, напишите мне новый никнейм.', reply_markup=kb, parse_mode='HTML')

async def quiz_state(message: types.Message, user_id: int, state: FSMContext):
    await state.set_state(UserForm.quiz)
    await message.answer(f"Начинаем квиз!")
    await new_quiz(message, user_id)

async def handle_quiz_answer(callback: types.CallbackQuery, state: FSMContext, is_corrent: bool):
    user_id = callback.from_user.id
    
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )

    if not await check_nickname(message=callback.message, user_id=user_id, state=state):
        return

    result_answer = ''
    current_question_index = await get_quiz_index(callback.from_user.id)
    correct_option = quiz_data[current_question_index]['correct_option']

    if is_corrent:
        result_answer = generate_correct_answer(quiz_data[current_question_index]['options'][correct_option])
        # 1 для верных
        await update_quiz_results(callback.from_user.id, current_question_index, 1)
    else:
        result_answer = generate_wrong_answer(quiz_data[current_question_index]['options'][correct_option])
        # 0 для неверных
        await update_quiz_results(callback.from_user.id, current_question_index, 0)

    await callback.message.answer(result_answer, parse_mode="HTML")

    current_question_index += 1
    await update_quiz_index(callback.from_user.id, current_question_index)

    if current_question_index < len(quiz_data):
        await get_question(callback.message, callback.from_user.id)
    else:
        results = await get_resluts(callback.from_user.id)
        await end_quiz(callback, state, results)

async def end_quiz(callback: types.CallbackQuery, state: FSMContext, results: str):
    await callback.message.answer(f"Это был последний вопрос. Квиз завершен! { results }", parse_mode="HTML")
    await main_menu_state(message=callback.message, user_id=callback.from_user.id, state=state)

async def cancel(callback: types.CallbackQuery, state: FSMContext):
    await main_menu_state(message=callback.message, user_id=callback.from_user.id, state=state)

# ON CANCEL CALLBACK IN ALLOWED STATES
@router.callback_query(StateFilter(
        UserForm.change_nickname,
        UserForm.quiz,
        UserForm.results_menu,
        UserForm.results_top,
    ),
    F.data == CB_CANCEL
)
async def allowed_cancel(callback: types.CallbackQuery, state: FSMContext):
    await cancel(callback, state)

# ON CANCEL CALLBACK IN OTHER STATES
@router.callback_query(F.data == CB_CANCEL)
async def other_states_cancel(callback: types.CallbackQuery):
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )
    await callback.message.answer('Отмена не поддерживается в текущем состоянии диалога')

# ОБРАБОТКА CB_START_QUIZ
@router.callback_query(UserForm.main_menu, F.data == CB_START_QUIZ)
async def cmd_quiz(callback: types.CallbackQuery, state: FSMContext):
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )

    user_id = callback.from_user.id
    has_nickname = await check_nickname(message=callback.message, user_id=user_id, state=state)
    if not has_nickname:
        return
    
    await quiz_state(message=callback.message, user_id=user_id, state=state)

# ОБРАБОТКА ВЕРНОГО ОТВЕТА
@router.callback_query(UserForm.quiz, F.data == CB_CORRECT_ANSWER)
async def right_answer(callback: types.CallbackQuery, state: FSMContext):
    await handle_quiz_answer(callback, state, is_corrent=True)

# ОБРАБОТКА НЕВЕРНОГО ОТВЕТА
@router.callback_query(UserForm.quiz, F.data == CB_WRONG_ANSWER)
async def wrong_answer(callback: types.CallbackQuery, state: FSMContext):
    await handle_quiz_answer(callback, state, is_corrent=False)

@router.message()
async def handle_all_text_messages(message: types.Message):
    await message.answer("Не понял ваше сообщение")

