import aiosqlite

from data.constatns import DB_NAME
from generate_answer import generate_results_list, generate_top_results_list

# Инициализация таблиц
async def create_table():
    async with aiosqlite.connect(DB_NAME) as db:
        # Создаем таблицы
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_users (user_id INTEGER PRIMARY KEY, nickname STRING)''')
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_state (user_id INTEGER PRIMARY KEY, question_index INTEGER)''')
        await db.execute('''CREATE TABLE IF NOT EXISTS user_state (user_id INTEGER PRIMARY KEY, user_state STRING)''')
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_results (user_id INTEGER NOT NULL, question_index INTEGER NOT NULL, answer_index INTEGER NOT NULL, PRIMARY KEY (user_id, question_index))''')
        # Сохраняем изменения
        await db.commit()

# Получение индекса текущего вопроса по пользователю
async def get_quiz_index(user_id):
     async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT question_index FROM quiz_state WHERE user_id = (?)', (user_id, )) as cursor:
            results = await cursor.fetchone()
            if results is not None:
                return results[0]
            else:
                return 0
            
# Реадктируем или создаём в базе запись с текущим индексом вопроса
async def update_quiz_index(user_id, index):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('INSERT OR REPLACE INTO quiz_state (user_id, question_index) VALUES (?, ?)', (user_id, index))
        await db.commit()
            
# Сохранение результата ответа на вопрос
async def update_quiz_results(user_id, question_index, answer_index):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('INSERT OR REPLACE INTO quiz_results (user_id, question_index, answer_index) VALUES (?, ?, ?)', (user_id, question_index, answer_index))
        await db.commit()

# Запрос и форматирование результатов пользователя
async def get_resluts(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        # Получаем запись для заданного пользователя
        async with db.execute('SELECT * FROM quiz_results WHERE user_id = (?)', (user_id, )) as cursor:
            # Возвращаем результат
            results = await cursor.fetchall()
            if results is not None:
                return generate_results_list(results)
            else:
                return 0
            
# Запрос и форматирование результатов пользователя
async def get_top_results():
    async with aiosqlite.connect(DB_NAME) as db:
        # Получаем запись для заданного пользователя
        async with db.execute('SELECT * FROM quiz_results') as cursor:
            # Возвращаем результат
            results = await cursor.fetchall()
            if results is not None:
                return await generate_top_results_list(results, get_user_nickname)
            else:
                return 0
            
# Получение состояния пользователя
async def get_user_state(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT user_state FROM user_state WHERE user_id = (?)', (user_id, )) as cursor:
            results = await cursor.fetchone()
            if results is not None:
                return results[0]
            else:
                return 0
        
# Обновление состояния пользователя
async def update_user_state(user_id, user_state):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('INSERT OR REPLACE INTO user_state (user_id, user_state) VALUES (?, ?)', (user_id, user_state))
        await db.commit()

# Получение никнейма пользователя
async def get_user_nickname(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT nickname FROM quiz_users WHERE user_id = (?)', (user_id, )) as cursor:
            results = await cursor.fetchone()
            if results is not None:
                return results[0]
            else:
                return 0
        
# Обновление никнейма пользователя
async def update_user_nickname(user_id, nickname):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('INSERT OR REPLACE INTO quiz_users (user_id, nickname) VALUES (?, ?)', (user_id, nickname))
        await db.commit()

