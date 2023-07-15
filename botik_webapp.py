import sqlite3
import re

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.web_app_info import WebAppInfo

bot = Bot('6095288525:AAG9NZQqQekdbvqoZ_NoN6F4EKZBpczzUrE')
dp = Dispatcher(bot)

conn = sqlite3.connect('users.db')  
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    links TEXT
                )''')
conn.commit()

users = {}

def extract_link(text):
    pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    matches = re.findall(pattern, text)
    if matches:
        return matches[0] 
    else:
        return None

def is_user_id_in_db(user_id):
    cursor.execute("SELECT user_id FROM users")
    user_ides = cursor.fetchall()
    for i in user_ides:
        return i[0]==user_id


@dp.message_handler(commands=['start'])
async def main(message: types.Message):
    user_id = message.from_user.id

    if not is_user_id_in_db(user_id):
        username =  message.from_user.username
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name
        users[user_id] = {
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'links': []
        }
        cursor.execute(
            'INSERT INTO users VALUES (?, ?, ?, ?, ?)',
            (user_id, username, first_name, last_name, '')
            )
        conn.commit()

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    btn4 = types.KeyboardButton('chatgpt', web_app=WebAppInfo(url='https://chat.openai.com'))
    btn2 = types.KeyboardButton('youtube', web_app=WebAppInfo(url='https://www.youtube.com'))
    btn1 = types.KeyboardButton('google', web_app=WebAppInfo(url='https://www.google.com'))
    btn3 = types.KeyboardButton('bard', web_app=WebAppInfo(url='https://bard.google.com/?hl=en'))
    markup.row(btn1, btn2, btn3, btn4)
    await message.answer('Hi, share me a link, I will open it!', reply_markup=markup)



@dp.message_handler(commands=['chatgpt'])
async def chatgpt_command(message: types.Message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Open ChatGPT', web_app=WebAppInfo(url='https://chat.openai.com'))
    markup.row(btn1)
    await message.answer('Opening ChatGPT...', reply_markup=markup)



@dp.message_handler(commands=['links'])
async def show_links(message: types.Message):
    user_id = message.from_user.id
    if is_user_id_in_db(user_id=user_id):
        cursor.execute(f'SELECT links FROM users WHERE user_id={user_id}')
        user_links = cursor.fetchall()        
        if user_links:
            # links_text = '\n'.join(user_links)
            links_text = f'{user_links[0][0]}'

            await message.answer(f'Your links:\n{links_text}')
        else:
            await message.answer('No links found!')
    else:
        await message.answer('User data not found!')


@dp.message_handler(content_types=['text'])
async def link(message: types.Message):
    user_id = message.from_user.id
    link = extract_link(message.text)
    if link:
        try:
            cursor.execute(f"SELECT links FROM users WHERE user_id={user_id}")
            user_links = cursor.fetchone()[0]
            user_links += link + '\n'+'\n'
            cursor.execute(f"UPDATE users SET links='{user_links}' WHERE user_id={user_id}")
            conn.commit()

            markup = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton('Open link', web_app=WebAppInfo(url=f'{link}'))
            markup.row(btn1)
            await message.answer(f'Link: {link}', reply_markup=markup)
        except Exception as e:
            await message.answer(f'An error occurred: {str(e)}')
    else:
        await message.answer('Links not found!')


def show_db():
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    if rows:
        print(rows)
    else:
        print('-- None --')

 
executor.start_polling(dp)

# https://api.telegram.org/bot6095288525:AAG9NZQqQekdbvqoZ_NoN6F4EKZBpczzUrE/sendMessage?chat_id=1169895301&text=lalala