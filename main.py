import requests
from bs4 import BeautifulSoup
import telebot


bot = telebot.TeleBot('')

# Parsing
page = 'https://community.uzbekcoders.uz/home/blogs'
agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.13 Safari/537.36'}

# Get Page Info
get_page = requests.get(page, headers=agent)
bs = BeautifulSoup(get_page.content, 'html.parser')

# Get information witch need to us
author = bs.select('div.ui.fluid.card.post-item.post-list-item > div.content.post-title > div.user-bar.clearfix > div.user-bar-content > div.header.user-bar-name > a > b')[0].text
title = bs.select('div.ui.fluid.card.post-item.post-list-item > div.content.post-title > h3')[0].text
link = bs.select('div.ui.fluid.card.post-item.post-list-item > div.content.post-title > h3 > a')[0]['href']
full_link = f"https://community.uzbekcoders.uz{link}"
image = bs.select('div.ui.fluid.card.post-item.post-list-item > div.content.post-content > div.description > div > figure.image > div > img')[0]['src']
text = bs.select('div.ui.fluid.card.post-item.post-list-item > div.content.post-content > div.description > div')[0].text[:500]


# Seting up the bot
@bot.message_handler(commands=["start"])
def start(message):
    caption = f"\tNew post by <b>{author}</b>\n<strong>{title}</strong>\n<i>{text}</i>\n\n<a href=\"{full_link}\">To'liq maqolani o'qish</a>"
    bot.send_photo(message.chat.id, caption=caption, photo=requests.get(image).content, parse_mode='html')

bot.polling()
