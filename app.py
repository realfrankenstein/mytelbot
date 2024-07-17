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

startesrs = []
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
linkdin_button = ikb(
    text="my linkedin", url='https://www.linkedin.com/in/amir-liqvany-676788318?lipi=urn%3Ali%3Apage%3Ad_flagship3_profile_view_base_contact_details%3BzUqqikfPRRa9rRq0TAivkw%3D%3D')
github_button = ikb(text="my git-hub",
                    url='https://github.com/realfrankenstein')
help_bt = ikb(text="/help")
links_box_bt = ikb(text="/links")
hi_bt = ikb(text="hi")
register_bt = KeyboardButton(text='register', request_contact=True)


# my inline keyboard
inline_keyboard = ikm(row_width=1)
inline_keyboard.add(chanell_button, ig_button,
                    linkdin_button, github_button, help_button)

# my reply keyboard
reply_kb = rkm(resize_keyboard=True, one_time_keyboard=False, row_width=2)
reply_kb.add(help_bt, links_box_bt, register_bt)


# start
@bot.message_handler(commands=['start'])
def welcome(messege):
    bot.send_message(messege.chat.id, "welcome to my dead mind",
                     reply_markup=reply_kb)
    # saves the user id
    if messege.chat.id not in startesrs:
        startesrs.append(messege.chat.id)
        print(messege.chat.id)

# send any messege for all users


@bot.message_handler(commands=['send'])
def send_any(messaege):
    for id in startesrs:
        bot.send_message(id, 'sokhum sana')

# to see list of users


@bot.message_handler(commands=['list'])
def show_list(messege):
    for id in startesrs:
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


his = [" سلام ", " سیلام ", " سلم ", " hi ", ' hey ', " های "]
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


def add_info(message):
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


@bot.message_handler(content_types=['contact'])
def info(message):
    if message.chat.id not in userid_list:
        add_info(message)

        userid_list.append(message.chat.id)
        bot.send_message(message.chat.id, text='your registration is done')
        bot.send_message(778221531, text=f'new victom: {message.contact}')
    else:
        bot.send_message(
            message.chat.id, text='looks like you have already registered')


'''using robots in groups and channels'''

# greating new members in groups


@bot.message_handler(content_types=['new_chat_members'])
def greating(message):
    wtext = f'گاربر \n{message.from_user.first_name}\n به یتم خانه ما پیوست.'
    bot.send_message(message.chat.id, text=wtext)

# cheking if a member of a group is an admin


def admin_chek(chat_id, user_is):
    admins = bot.get_chat_administrators(chat_id)
    for admin in admins:
        if admin.user.id == user_is:
            return True
    return False

# mangement of pinning messages by bot in order of admins


@bot.message_handler(func=lambda message: message.text == "pin")
def pin_message(message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if admin_chek(chat_id, user_id):
        if message.reply_to_message:
            bot.pin_chat_message(chat_id, message.reply_to_message.message_id)
            brt(message.reply_to_message, "زدمش رو در طویله که همه ببینه ")
        else:
            brt(message, "شماره ننتو بزنم بالا در ؟")
    else:
        brt(message.chat.id, "only members can pin messages!!")

# sending a message using the bot


@bot.message_handler(regexp="//write")
def bot_send(message):
    to_say_text = message.text.split()
    # removes the '//write' at the begining
    to_say_text.pop(0)
    bot.send_message(message.chat.id, text=' '.join(to_say_text))


bot.polling()
