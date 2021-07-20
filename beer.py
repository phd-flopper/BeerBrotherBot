from aiogram import types as agt
import cfg
import guidance as gd
import help_texts as ht
import httplib2
import preferences as spr
from random import choice
import reactions as react
import requests
from selenium import webdriver
import start_texts as st
import telebot
from time import sleep

bot = telebot.TeleBot(cfg.token)


markup_start = agt.ReplyKeyboardMarkup(resize_keyboard=True).add(st.START[4])


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, st.START[0])
    bot.send_message(message.chat.id, st.START[1])
    bot.send_message(message.chat.id, st.START[2])
    bot.send_message(message.chat.id, st.START[3],
                     reply_markup=[markup_start])


@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(message.chat.id, ht.HELP[0])


@bot.message_handler(commands=['set_preferences'])
def set_command(message):
    bot.send_message(message.chat.id, spr.START)
    bot.send_message(message.chat.id, spr.COLOUR,
                     reply_markup=[spr.markup_colour])

@bot.callback_query_handler(func=lambda c: c.data[0] == 'a')
def process_callback_сolour(callback_query):
    bot.answer_callback_query(callback_query.id, text='Выбор учтён')
    bot.send_message(callback_query.from_user.id,
                text=f'Выбор: '
                     f'{spr.colours_code_to_name[callback_query.data[-1]]}')
    gd.user_preferences[2] = callback_query.data[-1]
    bot.send_message(callback_query.from_user.id, spr.TYPE,
                     reply_markup=[spr.markup_type])

@bot.callback_query_handler(func=lambda c: c.data[0] == 'b')
def process_callback_type(callback_query):
    bot.answer_callback_query(callback_query.id, text='Выбор учтён')
    bot.send_message(callback_query.from_user.id,
                text=f'Выбор: '
                    f'{spr.sorted_tctn[callback_query.data[-1]]}')
    gd.user_preferences[1] = callback_query.data[-1]
    bot.send_message(callback_query.from_user.id, spr.REGION)
    bot.send_message(callback_query.from_user.id, spr.REGIONS_LIST)

@bot.message_handler(func=lambda c: c.text in spr.regions_names)
def set_region(message):
    bot.send_message(message.chat.id,
                     text=f'Выбор: '
                          f'{message.text}')
    gd.user_preferences[0] = spr.regions_code_to_name[message.text]
    bot.send_message(message.chat.id, spr.STRENGTH,
                     reply_markup=[spr.markup_strength])

@bot.callback_query_handler(func=lambda c: c.data[0] == 'c')
def process_callback_сolour(callback_query):
    bot.answer_callback_query(callback_query.id, text='Выбор учтён')
    bot.send_message(callback_query.from_user.id,
                text=f'Выбор: '
                    f'{spr.sorted_sctn[callback_query.data[-1]]}')
    gd.user_preferences[3] = callback_query.data[-1]
    bot.send_message(callback_query.from_user.id, spr.DONE)
    gd.user_url = 'https://birra.ru/beer/search?' \
           f'country[]={gd.user_preferences[0]}' \
           f'&type={gd.user_preferences[1]}' \
           f'&color={gd.user_preferences[2]}' \
           f'&alcohol={gd.user_preferences[3]}'


@bot.message_handler(commands=['guideme'])
def guideme_command(message):
    if gd.user_preferences == gd.TEMP_CHECKER:
        bot.send_message(message.chat.id, gd.GUIDANCE_FAILED)
    else:
        bot.send_message(message.chat.id, gd.GUIDANCE)
        guidance(message.chat.id)

def guidance(id):
    browser = webdriver.Firefox()
    browser.get(gd.user_url)
    sleep(cfg.sleep_time)
    beer_entities = browser.find_elements_by_class_name("title")
    for beer_entity in beer_entities:
        gd.recomended_beers.append(beer_entity.text)
    if gd.recomended_beers == []:
        bot.send_message(id, gd.GUIDANCE_NOT_FOUND)
        return
    beer_images = browser.find_elements_by_class_name("brands_img")
    for beer_image in beer_images:
        image = beer_image.find_element_by_tag_name('img')
        gd.recomended_beers_images.append(image.get_attribute('src'))
    gd.names_to_links = dict(zip(gd.recomended_beers, gd.recomended_beers_images))
    choice_name = choice(gd.recomended_beers)
    choice_img = gd.names_to_links[choice_name]
    gd.GUIDEME = 'С радостью сообщаю, что в моих силах наставить Вас!' \
              f'\nЯ считаю Вам понравится пиво:\n{choice_name}'
    bot.send_message(id, gd.GUIDEME)
    h = httplib2.Http('.cache')
    response, content = h.request(choice_img)
    file = open('img.jpg', 'wb')
    file.write(content)
    file.close()
    file = open('img.jpg', 'rb')
    bot.send_photo(id, file)
    file.close()
    bot.send_message(id, gd.GUIDANCE_DONE)


@bot.message_handler(commands=['show_preferences'])
def show_command(message):
    if gd.user_preferences != gd.TEMP_CHECKER:
        spr.SHOW = 'Страна: ' \
                f'{spr.regions_dict[gd.user_preferences[0]]}\n' \
               'Сорт: ' \
                f'{spr.types_code_to_name[gd.user_preferences[2]]}\n' \
               'Цвет: ' \
                f'{spr.colours_code_to_name[gd.user_preferences[2]]}\n' \
               'Крепость: ' \
                f'{spr.strengths_code_to_name[gd.user_preferences[3]]}'
    bot.send_message(message.chat.id, spr.SHOW)


LOCATE = 'Данная команда недоступна в тестовой версии'
@bot.message_handler(commands=['locate'])
def locate_command(message):
    bot.send_message(message.chat.id, LOCATE)


@bot.message_handler(commands=['bigfloppa'])
def bigfloppa_command(message):
    file = open('floppa.jpg', 'rb')
    bot.send_photo(message.chat.id, file)
    file.close()


@bot.message_handler(content_types=['sticker'])
def sticker_reaction(message):
    bot.send_sticker(message.chat.id, react.STICKER)


@bot.message_handler(content_types=['photo', 'document'])
def file_reaction(message):
    bot.send_message(message.chat.id, react.PHOTO)

@bot.message_handler(content_types=['voice'])
def text_reaction(message):
    bot.send_message(message.chat.id, choice(react.VOICE))


@bot.message_handler(content_types=['text'])
def text_reaction(message):
    bot.send_message(message.chat.id, choice(react.TEXT))


bot.polling(none_stop=True)