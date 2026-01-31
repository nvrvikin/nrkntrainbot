from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot_handlers.common_functions import check_nickname, main_menu_state
from bot_data.phrases import PHRASE_GREET

router = Router()

# ОБРАБОТКА /start
@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer(PHRASE_GREET)
    user_id = message.from_user.id

    if not await check_nickname(message, user_id, state):
        return
    
    await main_menu_state(message, user_id, state)