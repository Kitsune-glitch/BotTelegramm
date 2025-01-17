import aiosqlite
import main
# Зададим имя базы данных
DB_NAME = 'quiz_bot.db'
#async def create_database():
 #   conn = sqlite3.connect('quiz_bot.db')
  #  cursor = conn.cursor()
   # cursor.execute('''CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)''')
    #conn.close()
async def create_database():
    async def create_database():
        async with aiosqlite.connect('quiz_bot.db') as db:
            cursor = await db.cursor()
            try:
                await cursor.execute('''SELECT 1 FROM quiz_state LIMIT 1''')
            except aiosqlite.Error:
                try:
                    await cursor.execute(
                        '''CREATE TABLE quiz_state (user_id INTEGER PRIMARY KEY, question_index INTEGER)''')
                except aiosqlite.Error as e:
                    print(f"Error creating table: {e}")

async def  create_table() -> object:
    # Создаем соединение с базой данных (если она не существует, то она будет создана)
    async with aiosqlite.connect('quiz_bot.db') as db:
        # Выполняем SQL-запрос к базе данных
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_state (user_id INTEGER PRIMARY KEY, question_index INTEGER)''')
        # Сохраняем изменения
        await db.commit()
async def update_quiz_index(user_id, index, DB_NAME ):
    # Создаем соединение с базой данных (если она не существует, она будет создана)
    async with aiosqlite.connect(DB_NAME) as db:
        # Вставляем новую запись или заменяем ее, если с данным user_id уже существует
        await db.execute('INSERT OR REPLACE INTO quiz_state (user_id, question_index) VALUES (?, ?)', (user_id, index))
        # Сохраняем изменения
        await db.commit()


async def get_quiz_index(user_id):
    # Подключаемся к базе данных
    async with aiosqlite.connect(DB_NAME) as db:
        # Получаем запись для заданного пользователя
        async with db.execute('SELECT question_index FROM quiz_state WHERE user_id = (?)', (user_id,)) as cursor:
            # Возвращаем результат
            results = await cursor.fetchone()
            if results is not None:
                return results[0]
            else:
                return 0