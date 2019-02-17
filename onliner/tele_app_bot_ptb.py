import requests
import time
import pprint
from catalog_classifier import *
from sold_analyse import *
import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

UsersStates={}

updater = Updater(token='777208205:AAHhiYS_ZX28pAGbPSEs2KB1XmCnxMLCIic') # Токен API к Telegram
dispatcher = updater.dispatcher

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=(str(update.message.chat.first_name)+' , какая модель телефона Вас интересует?'))
    

def textMessage(bot, update):
    print(update.message.text)
    print(ClassifyAd(update.message.text)[2])
        
    response = "Телефон " + ClassifyAd(update.message.text)[2]+' ,средняя цена '+str(int(getMeanAndStdPrice(ClassifyAd(update.message.text)[2])[0]))+ " BYN"
    
    bot.send_message(chat_id=update.message.chat_id, text=str(response))

    

    '''
    keyboard = [[InlineKeyboardButton("Iphone 3", callback_data='Iphone 3')],[InlineKeyboardButton("Iphone 4", callback_data='Iphone 4')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)
    '''


def button(bot, update):
    query = update.callback_query

    if (UsersStates.get(query.message.chat_id)==None):
        UsersStates[query.message.chat_id]=query.data
            
    
        bot.edit_message_text(text="Какая модель Вас интересует?",
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    print('Update "%s" caused error "%s"', update, error)

text_message_handler = MessageHandler(Filters.text, textMessage)
# Добавляем хендлеры в диспетчер
dispatcher.add_handler(text_message_handler)
dispatcher.add_handler(CallbackQueryHandler(button))
updater.dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_error_handler(error)

# Начинаем поиск обновлений
updater.start_polling()
# Останавливаем бота, если были нажаты Ctrl + C
updater.idle()




'''
url = "https://api.telegram.org/bot777208205:AAHhiYS_ZX28pAGbPSEs2KB1XmCnxMLCIic/"


def get_updates_json(request,last_id=None):
    if last_id==None:        
        response = requests.get(request + 'getUpdates')
        return response.json()
    else:
        params = {'offset': last_id}
        response = requests.get(request + 'getUpdates',data=params)
        return response.json()
        


def last_update(data):  
    results = data['result']
    total_updates = len(results) - 1
    return results[total_updates]

def get_chat_id(update):  
    chat_id = update['message']['chat']['id']
    return chat_id

def send_mess(chat, text):  
    params = {'chat_id': chat, 'text': text,'parse_mode':'html'}
    response = requests.post(url + 'sendMessage', data=params)
    return response



last_update_id=None
while True:
       
    ud = get_updates_json(url,last_update_id)
    if (ud['result']!=[]):
        
        
        last_update_id=ud['result'][len(ud['result'])-1]['update_id']
        pprint.pprint(ud['result'][len(ud['result'])-1])
        last_update_id=int(last_update_id)+1
        print(last_update_id)
        send_mess(get_chat_id(ud['result'][0]),ud['result'][0]['message']['text'])
        send_mess(get_chat_id(ud['result'][0]),'<a href="https://example.com">This is an example</a>')
        
        
        time.sleep(1) 
   
'''
