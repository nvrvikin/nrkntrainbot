import aiosqlite

from bot_data.constatns import DB_NAME
from generate_answer import generate_results_list, generate_top_results_list

# Init tables
async def create_table():
    """
    Creates quiz_user, quiz_state and quiz_results tables if they do not exist
    """
    async with aiosqlite.connect(DB_NAME) as db:
        # Create tables
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_users (user_id INTEGER PRIMARY KEY, nickname STRING)''')
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_state (user_id INTEGER PRIMARY KEY, question_index INTEGER)''')
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_results (user_id INTEGER NOT NULL, question_index INTEGER NOT NULL, answer_index INTEGER NOT NULL, PRIMARY KEY (user_id, question_index))''')
        
        # Save changes
        await db.commit()

# Getting index of a current question for a user
async def get_quiz_index(user_id: int):
     """
     Returns a current question index for a user by user_id
     
     :param user_id: Chat user ID
     :type user_id: int
     """
     async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT question_index FROM quiz_state WHERE user_id = (?)', (user_id, )) as cursor:
            results = await cursor.fetchone()
            if results is not None:
                return results[0]
            else:
                return 0
            
# Реадктируем или создаём в базе запись с текущим индексом вопроса
async def update_quiz_index(user_id: int, index: int):
    """
    Updates or inserts 
    
    :param user_id: Description
    :type user_id: int
    :param index: Description
    :type index: int
    """
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('INSERT OR REPLACE INTO quiz_state (user_id, question_index) VALUES (?, ?)', (user_id, index))
        await db.commit()
            
# Сохранение результата ответа на вопрос
async def update_quiz_results(user_id: int, question_index: int, answer_index: int):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('INSERT OR REPLACE INTO quiz_results (user_id, question_index, answer_index) VALUES (?, ?, ?)', (user_id, question_index, answer_index))
        await db.commit()

# Запрос и форматирование результатов пользователя
async def get_resluts(user_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT * FROM quiz_results WHERE user_id = (?)', (user_id, )) as cursor:
            results = await cursor.fetchall()
            if results is not None:
                return generate_results_list(results)
            else:
                return 0
            
# Запрос и форматирование результатов пользователя
async def get_top_results():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT * FROM quiz_results') as cursor:
            results = await cursor.fetchall()
            if results is not None:
                # Passing get_user_nickname function to avoid cycle importing
                return await generate_top_results_list(results, get_user_nickname)
            else:
                return 0
            
# Getting user nickname
async def get_user_nickname(user_id: int):
    """
    Returns a nickname by user_id
    
    :param user_id: Chat user ID
    :type user_id: int
    """
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT nickname FROM quiz_users WHERE user_id = (?)', (user_id, )) as cursor:
            results = await cursor.fetchone()
            if results is not None:
                return results[0]
            else:
                return 0
        
# Updating user nickname
async def update_user_nickname(user_id: int, nickname: str):
    """
    Updates or insterts a nickname of the corresponding user
    by user_id into the database
    
    :param user_id: Chat user ID
    :type user_id: int
    :param nickname: A nickname user sent
    :type nickname: str
    """
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('INSERT OR REPLACE INTO quiz_users (user_id, nickname) VALUES (?, ?)', (user_id, nickname))
        await db.commit()

