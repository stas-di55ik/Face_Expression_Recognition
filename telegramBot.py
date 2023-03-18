from datetime import datetime

import telebot
import emotionDetection
import os

import markers
import messages
import config
import instagramSearch

ig_username = ''
ig_start_period = ''
ig_finish_period = ''

bot = telebot.TeleBot(config.telegram_bot_token)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, messages.start_answer)


@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, messages.help_answer)

@bot.message_handler(commands=['analyze_ig_specific_period'])
def analyze_ig_specific_period_message(message):
    bot.send_message(message.chat.id, messages.enter_ig_usernsme)
    bot.register_next_step_handler(message, reg_ig_username)


def reg_ig_username(message):
    global ig_username
    ig_username = message.text
    bot.send_message(message.chat.id, messages.enter_ig_start_date)
    bot.register_next_step_handler(message, reg_ig_start_period)


def reg_ig_start_period(message):
    global ig_start_period
    ig_start_period = message.text
    bot.send_message(message.chat.id, messages.enter_ig_finish_date)
    bot.register_next_step_handler(message, reg_ig_finish_period)


def reg_ig_finish_period(message):
    global ig_username, ig_start_period, ig_finish_period
    ig_finish_period = message.text

    handled_start_date = handle_date(ig_start_period)
    handled_finish_date = handle_date(ig_finish_period)
    if handled_start_date == False or handled_finish_date == False:
        bot.send_message(message.chat.id, messages.handling_date_error)

    else:
        instagramSearch.analyze_ig_specific_period(ig_username, ig_start_period, ig_finish_period)



def handle_date(input_date):
    try:
        splited_date = input_date.split(".")
        day = int(splited_date[0])
        month = int(splited_date[1])
        year = int(splited_date[2])
        return datetime(year, month, day)

    except:
        return False


@bot.message_handler(content_types=["photo"])
def handle_photo(message):
    bot.send_message(message.chat.id, messages.photo_handling_status)
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    filename, file_extension = os.path.splitext(file_info.file_path)
    downloaded_file = bot.download_file(file_info.file_path)

    with open(file_id + file_extension, 'wb') as new_file:
        new_file.write(downloaded_file)

    recognised_photos = emotionDetection.detect_emotions(file_id, file_extension)

    for recognised_photo in recognised_photos:
        if recognised_photo.succeeded == False:
            bot.send_message(message.chat.id, messages.detection_error_answer)
        else:
            bot.send_message(message.chat.id, messages.detection_summary_title + recognised_photo.summary)
        file = open(recognised_photo.file_name, 'rb')
        bot.send_photo(message.chat.id, file)

        os.remove(recognised_photo.file_name)
    os.remove(file_id + file_extension)


@bot.message_handler(content_types=["document", "audio", "sticker", "video", "location", "contact"])
def handle_doc(message):
    bot.send_message(message.chat.id, messages.documents_handling_answer)


bot.polling()
