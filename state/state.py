# Управление состоянием
from db_interactions import get_user_state
from state.states import STATE_CHANGE_NICKNAME, STATE_MAIN_MENU, STATE_NO_NICKNAME, STATE_QUIZ, STATE_RESULTS_GLOBAL, STATE_RESULTS_MENU

async def state_changed(user_id, message):
    current_state = get_user_state(user_id)
    if not current_state:
        pass
    if current_state == STATE_NO_NICKNAME:
        message.answer('Представьтесь. Сообщите имя, которое будет отображаться в таблице результатов (не более 20 символов).')
        pass
    if current_state == STATE_CHANGE_NICKNAME:
        pass
    if current_state == STATE_QUIZ:
        pass
    if current_state == STATE_MAIN_MENU:
        pass
    if current_state == STATE_RESULTS_MENU:
        pass
    if current_state == STATE_RESULTS_GLOBAL:
        pass
    pass

# Получение клаиватуры по состоянию
async def get_state_keyboard(user_id):
    state = get_user_state(user_id)