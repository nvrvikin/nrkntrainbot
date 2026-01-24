# Управление состоянием
from db_interactions import get_user_state
from state.states import STATE_CHANGE_NICKNAME, STATE_MAIN_MENU, STATE_NO_NICKNAME, STATE_QUIZ, STATE_RESULTS_GLOBAL, STATE_RESULTS_MENU

from aiogram.fsm.state import State, StatesGroup


class UserForm(StatesGroup):
    no_nickname = State()
    main_menu = State()
    quiz = State()
    results_menu = State()
    results_top = State()