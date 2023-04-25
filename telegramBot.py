import telebot
import emotionDetection
import os
import shutil

import markers
import messages
import config
import instagramSearch
import sentimentAnalyzer

ig_username = ''
ig_publications_number = ''

bot = telebot.TeleBot(config.telegram_bot_token)


def delete_ig_downloaded_source():
    current_directory = os.getcwd()
    current_dir_list = os.listdir(current_directory)
    for file_name in current_dir_list:
        if (".txt" in file_name) or (".jpg" in file_name):
            os.remove(file_name)


def ig_source_handling(message):
    for file_name in os.listdir(os.getcwd()):
        if ".txt" in file_name:
            text_file = open(file_name, "r")
            text = text_file.read()
            text_file.close()
            bot.send_message(message.chat.id, text)
            en_text = sentimentAnalyzer.auto_translate_to_en(text)
            result_score = sentimentAnalyzer.get_sentiment_analysis(en_text)
            bot.send_message(message.chat.id, result_score)
        if ".jpg" in file_name:
            recognised_photos = emotionDetection.detect_emotions(file_name)
            if recognised_photos == 'Error':
                bot.send_message(message.chat.id, messages.detection_error_answer)
            else:
                for recognised_photo in recognised_photos:
                    if recognised_photo.succeeded == False:
                        bot.send_message(message.chat.id, messages.detection_error_answer)
                    else:
                        bot.send_message(message.chat.id, messages.detection_summary_title + recognised_photo.summary)
                    file = open(recognised_photo.file_name, 'rb')
                    bot.send_photo(message.chat.id, file)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, messages.start_answer)


@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, messages.help_answer)


@bot.message_handler(commands=['analyze_last_x_ig_publications'])
def analyze_last_x_ig_publications(message):
    bot.send_message(message.chat.id, messages.enter_ig_username)
    bot.register_next_step_handler(message, reg_ig_username1)


def reg_ig_username1(message):
    global ig_username
    ig_username = message.text
    bot.send_message(message.chat.id, messages.enter_ig_last_x)
    bot.register_next_step_handler(message, reg_last_publications_number)


def reg_last_publications_number(message):
    global ig_username, ig_publications_number
    try:
        ig_publications_number = int(message.text)
        instagramSearch.download_last_x_publications(ig_username, ig_publications_number)
    except:
        bot.send_message(message.chat.id, messages.handling_ig_req_error1)

    ig_source_handling(message)
    delete_ig_downloaded_source()


@bot.message_handler(commands=['analyze_top_x_ig_publications'])
def analyze_top_x_ig_publications(message):
    bot.send_message(message.chat.id, messages.enter_ig_username)
    bot.register_next_step_handler(message, reg_ig_username2)


def reg_ig_username2(message):
    global ig_username
    ig_username = message.text
    bot.send_message(message.chat.id, messages.enter_ig_top_x)
    bot.register_next_step_handler(message, reg_top_publications_number)


def reg_top_publications_number(message):
    global ig_username, ig_publications_number
    try:
        ig_publications_number = int(message.text)
        instagramSearch.download_top_x_publications(ig_username, ig_publications_number)
    except:
        bot.send_message(message.chat.id, messages.handling_ig_req_error1)

    ig_source_handling(message)
    delete_ig_downloaded_source()


@bot.message_handler(commands=['analyze_specific_ig_publication'])
def analyze_specific_ig_publication(message):
    bot.send_message(message.chat.id, messages.enter_ig_username)
    bot.register_next_step_handler(message, reg_ig_username3)


def reg_ig_username3(message):
    global ig_username
    ig_username = message.text
    bot.send_message(message.chat.id, messages.enter_ig_specific_x)
    bot.register_next_step_handler(message, reg_specific_publication_number)


def reg_specific_publication_number(message):
    global ig_username, ig_publications_number
    try:
        ig_publications_number = int(message.text)
        instagramSearch.download_specific_publication(ig_username, ig_publications_number)
    except:
        bot.send_message(message.chat.id, messages.handling_ig_req_error1)

    ig_source_handling(message)
    delete_ig_downloaded_source()


@bot.message_handler(commands=['sentiment_analysis'])
def analyze_text(message):
    bot.send_message(message.chat.id, messages.enter_sentiment_analysis_source)
    bot.register_next_step_handler(message, reg_sentiment_analyze_source)


def reg_sentiment_analyze_source(message):
    sentiment_analyze_source = message.text
    try:
        translated_source = sentimentAnalyzer.auto_translate_to_en(sentiment_analyze_source)
        score = sentimentAnalyzer.get_sentiment_analysis(translated_source)
        bot.send_message(message.chat.id, score)
    except:
        bot.send_message(message.chat.id, messages.sentiment_analysis_error)


@bot.message_handler(content_types=["photo"])
def handle_photo(message):
    bot.send_message(message.chat.id, messages.photo_handling_status)
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    filename, file_extension = os.path.splitext(file_info.file_path)
    downloaded_file = bot.download_file(file_info.file_path)

    with open(file_id + file_extension, 'wb') as new_file:
        new_file.write(downloaded_file)

    recognised_photos = emotionDetection.detect_emotions(file_id + file_extension)
    if recognised_photos == 'Error':
        bot.send_message(message.chat.id, messages.detection_error_answer)
    else:
        for recognised_photo in recognised_photos:
            if recognised_photo.succeeded == False:
                bot.send_message(message.chat.id, messages.detection_error_answer)
            else:
                bot.send_message(message.chat.id, messages.detection_summary_title + recognised_photo.summary)
            file = open(recognised_photo.file_name, 'rb')
            bot.send_photo(message.chat.id, file)
        delete_ig_downloaded_source()



@bot.message_handler(content_types=["document", "audio", "sticker", "video", "location", "contact"])
def handle_doc(message):
    bot.send_message(message.chat.id, messages.documents_handling_answer)


bot.polling()
