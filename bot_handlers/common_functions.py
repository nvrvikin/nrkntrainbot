from aiogram.fsm.context import FSMContext
from aiogram import F, types

from bot_handlers.callback_handlers import no_nickname_state
from db_interactions import get_user_nickname
from generate_answer import show_main_menu
from state.state import UserForm

async def check_nickname(message: types.Message, user_id: int, state: FSMContext):
    if not await get_user_nickname(user_id):
        await no_nickname_state(message, state)
        return False
    return True

async def no_nickname_state(message: types.Message, state: FSMContext):
    await state.set_state(UserForm.no_nickname)
    await message.answer('Требуется придумать ник от 3 до 20 символов для отображения в общих результатах')

async def main_menu_state(message: types.Message, user_id: int, state: FSMContext):
    nickname = await get_user_nickname(user_id)
    print(nickname)
    await state.set_state(UserForm.main_menu)
    await show_main_menu(message, nickname)