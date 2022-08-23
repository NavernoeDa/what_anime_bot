from base64 import b64encode

from telebot import TeleBot
import requests

bot = TeleBot('')


def download(message):
    file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open('photo.jpg', 'wb') as new_file:
        new_file.write(downloaded_file)


def update_file(file_path, key):
    with open(file_path, 'rb') as file:
        link = 'https://api.imgbb.com/1/upload'
        post = {
            'key': key,
            'image': b64encode(file.read()),
            'expiration': 60
        }
        post = requests.post(link, post)
        return post.json()['data']['url']


def give_me_anime(url):
    link = f'https://api.trace.moe/search?anilistInfo&url={url}'
    post = requests.get(link)
    return post.json()


@bot.message_handler(commands=['start', 'help'])
def help(message):
    bot.reply_to(message, 'Этот бот позволяет определить аниме по картинке. Достаточно отправить фото с аниме')


@bot.message_handler(content_types=['photo'])
def main(message):
    download(message)
    link = update_file('photo.jpg', '78b20c60bec9967d77fc8e9eb750cd44')
    result = give_me_anime(link)['result'][0]
    text = f'><b>Name</b>: {result["anilist"]["title"]["romaji"]} ({result["anilist"]["title"]["english"]})\n' \
           f'><b>Is Adult</b>: {result["anilist"]["isAdult"]}\n' \
           f'><b>Episode</b>: {result["episode"]}\n' \
           f'><b>From</b>: {result["from"]} sec\n' \
           f'><b>To</b>: {result["to"]} sec'
    bot.reply_to(message, text, parse_mode='HTML')


bot.infinity_polling(timeout=10, long_polling_timeout=5)
