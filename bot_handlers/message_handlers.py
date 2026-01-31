from aiogram import F, Router, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from bot_handlers.common_functions import main_menu_state
from db_interactions import update_user_nickname
from state.state import UserForm

router = Router()

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
    await message.answer(f"Отлично, { username }!")
    await main_menu_state(message=message, user_id=message.from_user.id, state=state)

# ON MESSAGE IN [no_nickname] OR [change_nickname] STATES
@router.message(StateFilter(UserForm.no_nickname, UserForm.change_nickname))
async def no_nickname_message(message: types.Message, state: FSMContext):
    await process_nickname(message, state)

# ON MESSAGES IN ANY OTHER STATE
@router.message()
async def handle_all_text_messages(message: types.Message):
    await message.answer("Не понял ваше сообщение")