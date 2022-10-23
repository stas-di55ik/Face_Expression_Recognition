import telebot
import cv2
import Edetectorgit
import config
import os
from pathlib import Path

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привiт ✌️ Надішли мені фото - і я розпізнаю емоції на ньому)")

@bot.message_handler(content_types=["photo"])
def handle_photo(message):
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    # photo_name = message.photo.file_name
    filename, file_extension = os.path.splitext(file_info.file_path)
    downloaded_file = bot.download_file(file_info.file_path)
    # src = str(Path.home() / "Desktop/src/university/TermPaper/Face_Expression_Recognition-master/received/" + file_id + file_extension)
    file_id = 'z' + file_id
    with open(file_id + file_extension, 'wb') as new_file:
        new_file.write(downloaded_file)

    photo_summary = Edetectorgit.emotion_detection(file_id, file_extension)
    print(photo_summary)
    file = open(photo_summary, 'rb')
    bot.send_document(message.chat.id, file)


bot.polling()
