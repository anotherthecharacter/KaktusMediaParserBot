import parsing
from decouple import config
import telebot


token = config('token')
bot = telebot.TeleBot(token)
news = {}


@bot.message_handler(commands=['start', 'restart'])
def start_message(message):
    global news

    user = message.from_user.id

    bot.send_message(user, 'Идет загрузка новостей... это может занять около минуты. Пожалуйста подождите.')
    news = parsing.get_data(parsing.news_collect())

    start_m = ''

    for id_, single_n in news.items():
        start_m += f"{id_}. {single_n['title']}\n\n"
         
    bot.send_message(user, 'Последние 20 новостей KaktusMedia (введите номер статьи):\n\n\n' + start_m)


@bot.message_handler(content_types=['text'])
def text_messages_reply(message):
    user = message.from_user.id
    
    if message.text in news.keys():
        try:        
            interaction_keys = telebot.types.InlineKeyboardMarkup()
            button_desciption = telebot.types.InlineKeyboardButton('Description', callback_data='description')
            button_photo = telebot.types.InlineKeyboardButton('Photo', callback_data='photo')
            button_quit = telebot.types.InlineKeyboardButton('Quit', callback_data='quit')
            interaction_keys.add(button_desciption, button_photo, button_quit)

            bot.send_message(user, f'some "{news[message.text]["title"]}" news\nyou can see Description of this news and Photo', reply_markup=interaction_keys)
        except (NameError, Exception):
            bot.send_message(user, 'Что-то пошло не так... Попробуйте ещё раз.')
            bot.send_message(user, 'Чтобы продолжить, напишите: /restart')
    else:
        bot.send_message(user, 'Такой новости нет.')
        bot.send_message(user, 'Чтобы продолжить, напишите: /restart')


@bot.callback_query_handler(func=lambda call: True)
def reply_to_button(call):
    user = call.from_user.id

    if call.data == 'description':
        try:
            text = [i['description'] for i in news.values() if i['title'] == call.message.text[6:-53]][0]
        except (IndexError, Exception):
            bot.send_message(user, 'К сожалению, данное описание сейчас недоступно.')
            bot.send_message(user, 'Чтобы продолжить, напишите: /restart')
        else:
            for i in range(0, len(text), 4095):
                bot.send_message(user, text[i:i+4095])
    elif call.data == 'photo':
        bot.send_photo(user, [i['photo'] for i in news.values() if i['title'] == call.message.text[6:-53]][0])
    else:
        bot.send_message(user, 'До свидания')


bot.polling()
