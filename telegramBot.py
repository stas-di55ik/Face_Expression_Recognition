import telebot
import emotionDetection
import os

import markers
import messages
import config
import instagramSearch


bot = telebot.TeleBot(config.telegram_bot_token)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, messages.start_answer)


@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, messages.help_answer)


@bot.message_handler(content_types=["photo"])
def handle_photo(message):
    bot.send_message(message.chat.id, messages.photo_handling_status)
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    filename, file_extension = os.path.splitext(file_info.file_path)
    downloaded_file = bot.download_file(file_info.file_path)

    with open(file_id + file_extension, 'wb') as new_file:
        new_file.write(downloaded_file)

    photo_summary = emotionDetection.emotion_detection(file_id, file_extension)
    if photo_summary == markers.Error:
        bot.send_message(message.chat.id, messages.detection_error_answer)

    else:
        bot.send_message(message.chat.id, messages.detection_summary_title + photo_summary)
        file = open(markers.Detected_emotions_tag + file_id + file_extension, 'rb')
        bot.send_photo(message.chat.id, file)
        os.remove(file_id + file_extension)
        os.remove(markers.Detected_emotions_tag + file_id + file_extension)


@bot.message_handler(content_types=["document", "audio", "sticker", "video", "location", "contact"])
def handle_doc(message):
    bot.send_message(message.chat.id, messages.documents_handling_answer)


@bot.message_handler(content_types=["text"])
def handle_text(message):
    if markers.Instagram_link in message.text:
        bot.send_message(message.chat.id, messages.photo_searching_status)
        file_name = instagramSearch.load_instagram_image(message)
        bot.send_message(message.chat.id, messages.photo_handling_status)
        photo_summary = emotionDetection.emotion_detection(file_name[0], file_name[1])
        if photo_summary == markers.Error or file_name == markers.Error:
            bot.send_message(message.chat.id, messages.detection_searching_error_answer)

        else:
            bot.send_message(message.chat.id, messages.detection_summary_title + photo_summary)
            file = open(file_name[0] + file_name[1], 'rb')
            bot.send_photo(message.chat.id, file)
            os.remove(file_name[0] + file_name[1])
            os.remove(markers.Detected_emotions_tag + file_name[0] + file_name[1])
    else:
        bot.send_message(message.chat.id, messages.text_handling_answer)


bot.polling()
