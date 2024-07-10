import bot
import telebot
import random
# for putting buttoons
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
# for making a list of actions
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import sqlite3
bot = telebot.TeleBot(bot.tok, )

brt = bot.reply_to

user_ID = []
# my shortvuts
ikb = InlineKeyboardButton
ikm = InlineKeyboardMarkup
rkm = ReplyKeyboardMarkup

# creating a data base for collecting user info
with sqlite3.connect('users.db') as connection:
    cursor = connection.cursor()
    crt = """
        CREATE TABLE IF NOT EXISTS user(
            id integer primary key,
            first_name text,
            last_name text,
            phone_number text
        );
    """
    cursor.execute(crt)


# my buttons
help_button = ikb(text='help', callback_data="help")
chanell_button = ikb(
    text='my channel',
    url='https://t.me/kanale_un_khostipi_ke_ashegeshi')
ig_button = ikb(
    text='my instagrm',
    url='https://www.instagram.com/nlamirali?igsh=MWZhZGg1bzI1aDM1Yw==')
help_bt = ikb(text="/help")
links_box_bt = ikb(text="/links")
hi_bt = ikb(text="hi")
register_bt = KeyboardButton(text='register', request_contact=True)


# my inline keyboard
inline_keyboard = ikm(row_width=1)
inline_keyboard.add(chanell_button, ig_button, help_button)

# my reply keyboard
reply_kb = rkm(resize_keyboard=True, one_time_keyboard=False, row_width=2)
reply_kb.add(help_bt, links_box_bt, hi_bt, register_bt)


# start
@bot.message_handler(commands=['start'])
def welcome(messege):
    bot.send_message(messege.chat.id, "welcome to my dead mind",
                     reply_markup=reply_kb)
    # saves the user id
    if messege.chat.id not in user_ID:
        user_ID.append(messege.chat.id)

# send any messege for all users


@bot.message_handler(commands=['send'])
def send_any(messaege):
    for id in user_ID:
        bot.send_message(id, 'sokhum sana')

# to see list of users


@bot.message_handler(commands=['list'])
def show_list(messege):
    for id in user_ID:
        print(id)

# my link box


@bot.message_handler(commands=['links'])
def link_box(message):
    bot.send_message(
        message.chat.id, "here are the links you can be pain in an ass through", reply_markup=inline_keyboard)
# answering callbacks from buttons


@bot.callback_query_handler(func=lambda call: True)
def chek(call):
    if call.data == 'help':
        bot.answer_callback_query(
            call.id, 'fuck off bitch \nno help here \nfinde it out yorself', show_alert=True)

# just fun


@bot.message_handler(commands=['help'])
def help(messege):
    brt(messege, "no help here \nfinde it out yorself")


# using lamda for filtering
@bot.message_handler(func=lambda message: message.document.mime_type == 'text/plain', content_types=['document'])
def too_lazy_to_read(message):
    brt(
        message, "too lazier than that 2 read all this man \nu better put some picks in it")


'''another wat to filter like lambda'''
# def test_message(message):
#     return message.document.mime_type == 'trext/plain'


# @bot.message_handler(func=test_message, content_types=['document'])
# def lazy_2_read(message):
#     brt(message, "same shit i told\nput some fucking pics")


# content type filtering
@bot.message_handler(content_types=['document', 'audio'])
def handle(message):
    if message.audio:
        brt(message, "کیرم تو سلیقه موسیقیت")
    elif message.document:
        brt(message, "u except me to read all this shit ?")

# regular exprssion


his = ["سلام", "سیلام", "سلم", "hi", 'hey', "های"]
hibacks = ["سلام به سس عمه ت ", "سلام و کیر خر ",
           "کیرم تو سلامت ", "hi yourself",
           "این بار کاریت ندارم علیک سلام"]

for hi in his:
    @bot.message_handler(regexp=hi)
    def aleyk(message):
        brt(message, random.choice(hibacks))

'''echooooo'''
# @bot.message_handler(func=lambda m: True)
# def echo_all(message):
#     brt(message, f"{message.text} yourself")


# getting user info and saving it to database
userid_list = []


@bot.message_handler(content_types=['contact'])
def info(message):
    if message.chat.id != 778221531:
        bot.send_message(778221531, text=f'got a new victom{message.contact}')
        # bot.send_message(message.chat.id, text='your registration is done')
    else:
        bot.send_message(message.chat.id, text=f'{message.contact}')
    if message.chat.id not in user_ID:
        with sqlite3.connect('users.db') as connection:
            cursor = connection.cursor()
            insert_data_query = """
                INSERT INTO user (id, first_name, last_name, phone_number)
                VALUES (?,?,?,?)
            """
            data = (
                message.contact.user_id,
                f'{message.contact.first_name}',
                f'{message.contact.last_name}',
                f'{message.contact.phone_number}',
            )
            cursor.execute(insert_data_query, data)
        user_ID.append(message.chat.id)
        bot.send_message(message.chat.id, text='your registration is done')

# greating new members in groups


@bot.message_handler(content_types=['new_chat_members'])
def greating(message):
    for new_member in message.new_chat_members:
        text = f'به یتیم خانه ما پیوست {message.from_user.firs_name} کاربر  '
        bot.send_message(message.chat.id, text)


bot.polling()
