from database import connect_to_database

# Создание базы данных
def create_db():
    conn = connect_to_database()
    cursor = conn.cursor()

    # Создаем таблицы, если они еще не существуют
    cursor.execute('''CREATE TABLE IF NOT EXISTS data (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        identifier_name VARCHAR(255),
                        identifier_text TEXT,
                        image_path VARCHAR(255),
                        video_path VARCHAR(255),
                        file_path VARCHAR(255),
                        link VARCHAR(255)
                    )''')
    conn.commit()
    conn.close()

# Создание таблицы admins
def create_admins_table():
    conn = connect_to_database()
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS admins (
                            id INT PRIMARY KEY AUTO_INCREMENT,
                            tg_admin_id INT
                        )''')

    conn.commit()
    conn.close()

# Создание таблицы users
def create_users_table():
    conn = connect_to_database()
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INT PRIMARY KEY AUTO_INCREMENT,
                            tg_id INT,
                            tg_first_name VARCHAR(255),
                            tg_last_name VARCHAR(255),
                            tg_username VARCHAR(255),
                            registration_date DATE,
                            registration_time TIME,
                            messages_viewed INT
                        )''')

    conn.commit()
    conn.close()

# Функция для проверки, является ли пользователь администратором
def is_admin_allowed(user_id):
    conn = connect_to_database()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM admins WHERE tg_admin_id = %s', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return bool(user)

def get_all_users():
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()
    return users

def increase_messages_viewed(user_id):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET messages_viewed = messages_viewed + 1 WHERE tg_id = %s', (user_id,))
    conn.commit()
    conn.close()
