import aiogram.utils.exceptions
from db_function import is_admin_allowed, create_db, get_all_users, increase_messages_viewed, \
    create_admins_table, create_users_table
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram import executor
import configparser
import schedule
import datetime
from database import connect_to_database

import asyncio

class SendMessage(StatesGroup):
    MESSAGE = State()

config = configparser.ConfigParser()
config.read("config.ini")
TOKEN = config['Telegram']['bot_token']

# Создаем объекты бота и диспетчера
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Define the task you want to perform
async def your_task():
    # Получаем список всех пользователей
    users = get_all_users()
    # Отправляем сообщение каждому пользователю, кроме администратора
    for user in users:
        user_id = user[1]  # Предполагается, что user_id находится на первой позиции

        conn = connect_to_database()
        cursor = conn.cursor()
        if user[7] == 1:
            cursor.execute('SELECT * FROM data WHERE identifier_name = "first_send"')
            data_rows = cursor.fetchall()
        elif user[7] == 2:
            cursor.execute('SELECT * FROM data WHERE identifier_name = "two_send"')
            data_rows = cursor.fetchall()
        elif user[7] == 3:
            cursor.execute('SELECT * FROM data WHERE identifier_name = "three_send"')
            data_rows = cursor.fetchall()
        elif user[7] == 4:
            cursor.execute('SELECT * FROM data WHERE identifier_name = "four_send"')
            data_rows = cursor.fetchall()
        elif user[7] == 5:
            cursor.execute('SELECT * FROM data WHERE identifier_name = "five_send"')
            data_rows = cursor.fetchall()
        elif user[7] == 6:
            cursor.execute('SELECT * FROM data WHERE identifier_name = "six_send"')
            data_rows = cursor.fetchall()
        else:
            break
        conn.close()
        try:
            for row in data_rows:
                identifier_text = row[2]
                image_path = row[3]
                video_path = row[4]
                file_path = row[5]
                link = row[6]

                if image_path:
                    await bot.send_photo(user_id, photo=open(image_path, 'rb'), caption=identifier_text)

                elif video_path:
                    await bot.send_video(user_id, video=open(video_path, 'rb'), caption=identifier_text)

                elif file_path:
                    await bot.send_document(user_id, document=open(file_path, 'rb'), caption=identifier_text)

                elif link:
                    await bot.send_message(user_id, identifier_text + "\n" + link)

                else:
                    if user[7] == 2:
                        keyboard = InlineKeyboardMarkup()
                        button = InlineKeyboardButton('Записаться на пробы', url='http://project7536023.tilda.ws')
                        keyboard.add(button)
                        await bot.send_message(user_id, identifier_text, reply_markup=keyboard)
                    elif user[7] == 5:
                        await bot.send_message(user_id, identifier_text, parse_mode="HTML")
                    else:
                        await bot.send_message(user_id, identifier_text)


                increase_messages_viewed(user_id)
        except aiogram.utils.exceptions.BotBlocked as a:
            print(str(a) + " " + str(user_id))

# Schedule the task to run at a specific time each day
def schedule_task():
    asyncio.ensure_future(your_task())

# Start the scheduler
async def start_scheduler():
    schedule.every().day.at("12:00").do(schedule_task)
    # Keep the program running
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start_command_handler(message: types.Message):
    user_id = message.from_user.id

    # Проверяем, является ли пользователь администратором
    if is_admin_allowed(user_id):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.KeyboardButton(text="Отправить сообщение"))
        await message.answer("Доброго времени суток!",
                             reply_markup=keyboard)
    else:
        user_id = message.from_user.id
        user_first_name = message.from_user.first_name
        user_last_name = message.from_user.last_name
        user_username = message.from_user.username

        conn = connect_to_database()
        cursor = conn.cursor()

        # Проверяем, есть ли пользователь в базе данных
        cursor.execute('SELECT * FROM users WHERE tg_id = %s', (user_id,))
        existing_user = cursor.fetchone()

        current_date = datetime.date.today().strftime("%Y-%m-%d")
        current_time = datetime.datetime.now().strftime("%H:%M:%S")

        if existing_user:
            # Если пользователь уже есть в базе данных, обновляем его данные
            cursor.execute('UPDATE users SET tg_first_name = %s, tg_last_name = %s, tg_username = %s, '
                           'registration_date = %s, registration_time = %s WHERE tg_id = %s',
                           (user_first_name, user_last_name, user_username, current_date, current_time, user_id))

            conn.commit()
            conn.close()
        else:

            # Если пользователь новый, добавляем его в базу данных
            cursor.execute(
                'INSERT INTO users (tg_id, tg_first_name, tg_last_name, tg_username, registration_date, registration_time, messages_viewed) '
                'VALUES (%s, %s, %s, %s, %s, %s, 0)',
                (user_id, user_first_name, user_last_name, user_username, current_date, current_time))

            conn.commit()
            conn.close()
            increase_messages_viewed(user_id)



        # Отправляем сообщение пользователю с данными из таблицы data
        conn = connect_to_database()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM data WHERE identifier_name = "start_text"')
        data_rows = cursor.fetchall()

        conn.close()

        for row in data_rows:
            identifier_text = row[2]
            image_path = row[3]
            video_path = row[4]
            file_path = row[5]
            link = row[6]

            if image_path:
                await bot.send_photo(user_id, photo=open(image_path, 'rb'), caption=identifier_text)

            elif video_path:
                await bot.send_video(user_id, video=video_path, caption=identifier_text)
            elif file_path:
                await bot.send_document(user_id, document=open(file_path, 'rb'), caption=identifier_text)

            elif link:
                await bot.send_message(user_id, identifier_text + "\n" + link)

            else:
                await bot.send_message(user_id, identifier_text)


# Обработчик нажатия кнопки "Отправить сообщение"
@dp.message_handler(lambda message: message.text == "Отправить сообщение")
async def send_message_handler(message: types.Message):
    if message.text == "Отправить сообщение":
        user_id = message.from_user.id
        # Проверяем, является ли пользователь администратором
        if is_admin_allowed(user_id):
            await message.answer("Введите текст сообщения или прикрепите медиафайл:")
            await SendMessage.MESSAGE.set()
        else:
            await message.answer("У вас нет прав для выполнения этой команды.")
    else:
        await message.answer("У вас нет прав для выполнения этой команды.")

@dp.message_handler(content_types=types.ContentTypes.ANY)
async def message_read_handler(message: types.Message):
    user_id = message.from_user.id
    increase_messages_viewed(user_id)

# Обработчик сообщений для получения сообщения или медиафайла от администратора
@dp.message_handler(content_types=types.ContentTypes.ANY, state=SendMessage.MESSAGE)
async def forward_message_step(message: types.Message, state: FSMContext):
    # Получаем список всех пользователей
    users = get_all_users()
    # Отправляем сообщение каждому пользователю, кроме администратора
    for user in users:
        user_id = user[1]
        try:
            if not is_admin_allowed(user_id) and user[7] > 6:
                # Отправка текстового сообщения
                if message.text:
                    await bot.send_message(chat_id=user_id, text=message.text)

                # Отправка медиафайла с подписью
                if message.photo:
                    photo = message.photo[-1].file_id
                    await bot.send_photo(chat_id=user_id, photo=photo, caption=message.caption)

                # Отправка документа с подписью
                if message.document:
                    document = message.document.file_id
                    await bot.send_document(user_id, document=document, caption=message.caption)

                # Отправка видео с подписью
                if message.video:
                    video = message.video.file_id
                    await bot.send_video(user_id, video=video, caption=message.caption)

        except aiogram.utils.exceptions.BotBlocked as e:
            print(str(e) + " " + str(user_id))

    await bot.send_message(chat_id=message.from_user.id, text="Сообщение отправлено всем пользователям (кроме администратора).")
    await state.finish()

if __name__ == '__main__':
    create_db()
    create_admins_table()
    create_users_table()
    loop = asyncio.get_event_loop()
    loop.create_task(start_scheduler())
    executor.start_polling(dp, skip_updates=True)