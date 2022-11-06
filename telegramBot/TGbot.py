import telebot
import Edetectorgit
import config
import os

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привiт ✌️ Надішлшть мені, будь ласка, фото (НЕ ФАЙЛОМ! 😅) - "
                                      "і я розпізнаю емоції на ньому)")


@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.chat.id, "Привiт ✌️ Я, бот🦾🤖, що був створений для розпізнавання емоцій на фото\n"
                                      "✍️Вимоги до використання:\n✅ Надсилайте лише стиснені фото\n"
                                      "✅ Надсилайте фото, на якому є лише одне обличчя, інакше емоції будуть розпізнені"
                                      " лише на одному\n")


@bot.message_handler(content_types=["photo"])
def handle_photo(message):
    bot.send_message(message.chat.id, "⚙️Триває розпізнавання...")
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    filename, file_extension = os.path.splitext(file_info.file_path)
    downloaded_file = bot.download_file(file_info.file_path)
    file_id = 'z' + file_id
    with open(file_id + file_extension, 'wb') as new_file:
        new_file.write(downloaded_file)

    photo_summary = Edetectorgit.emotion_detection(file_id, file_extension)
    if photo_summary == 'Error':
        bot.send_message(message.chat.id, "Вибачте за незручності, дане фото не підлягає аналізу🥲")

    else:
        bot.send_message(message.chat.id, "🌟 Підсумок аналізу фото 🫡\n" + photo_summary)
        file = open('zEmotion'+file_id + file_extension, 'rb')
        bot.send_photo(message.chat.id, file)
        os.remove(file_id + file_extension)
        os.remove('zEmotion'+file_id + file_extension)


@bot.message_handler(content_types=["document", "audio", "sticker", "video", "location", "contact"])
def handle_doc(message):
    bot.send_message(message.chat.id, "На жаль, я можу працювати лише з фото😌")


@bot.message_handler(content_types=["text"])
def handle_doc(message):
    bot.send_message(message.chat.id, "Надішліть, будь ласка, фото для аналізу😊")


bot.polling()
