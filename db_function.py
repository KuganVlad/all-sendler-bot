import sqlite3

# Создание базы данных
def create_db():
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()

    # Создаем таблицы, если они еще не существуют
    cursor.execute('''CREATE TABLE IF NOT EXISTS data (
                            id INTEGER PRIMARY KEY,
                            identifier_name TEXT,
                            identifier_text TEXT,
                            image_path TEXT,
                            video_path TEXT,
                            file_path TEXT,
                            link TEXT
                        )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS admins (
                            id INTEGER PRIMARY KEY,
                            tg_admin_id INTEGER
                        )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            tg_id INTEGER,
                            tg_first_name TEXT,
                            tg_last_name TEXT,
                            tg_username TEXT,
                            registration_date TEXT,
                            registration_time TEXT,
                            messages_viewed INTEGER
                        )''')

    conn.commit()
    conn.close()

# Функция для проверки, является ли пользователь администратором
def is_admin_allowed(user_id):
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM admins WHERE tg_admin_id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return bool(user)

def get_all_users():
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()
    return users

def increase_messages_viewed(user_id):
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET messages_viewed = messages_viewed + 1 WHERE tg_id = ?', (user_id,))
    conn.commit()
    conn.close()
