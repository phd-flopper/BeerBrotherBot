from aiogram import types as agt
import urllib.request
import six
import requests
from bs4 import BeautifulSoup
import pandas as pd

START = 'Сейчас Вы сможете указать свои предпочтения. ' \
            '\nЭто потребуется для команд /guideme и /locate.'

COLOUR = 'Выберите цвет пива'

url = 'https://birra.ru/beer/search?'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

colours_div_block = soup.find_all('div')[19]
colours = colours_div_block.find_all('option')
colours_names = [colour.text.strip() for colour in colours] #nice
colours_codes = [(colour['value']) for colour in colours] #nice
colours_code_to_name = dict(zip(colours_codes, colours_names))

c_button0 = agt.InlineKeyboardButton(colours_names[0],
                                     callback_data='a0')
c_button1 = agt.InlineKeyboardButton(colours_names[1],
                                     callback_data='a1')
c_button2 = agt.InlineKeyboardButton(colours_names[2],
                                     callback_data='a2')
markup_colour = agt.InlineKeyboardMarkup(resize_keyboard=True)
markup_colour.row(c_button0, c_button1, c_button2)

TYPE = 'Теперь выберите сорт пива'

types_div_block = soup.find_all('div')[18]
types = types_div_block.find_all('option')
types_names = [type_.text.strip() for type_ in types] #nice
types_codes = [type_['value'] for type_ in types] #nice
types_code_to_name = dict(zip(types_codes, types_names))
sorted_tctn = {types_codes[0]: types_names[0],
               types_codes[1]: types_names[2],
               types_codes[2]: types_names[1],
               types_codes[3]: types_names[3]}

t_button0 = agt.InlineKeyboardButton(types_names[0],
                                     callback_data='b0')
t_button1 = agt.InlineKeyboardButton(types_names[2],
                                     callback_data='b1')
t_button2 = agt.InlineKeyboardButton(types_names[1],
                                     callback_data='b2')
t_button3 = agt.InlineKeyboardButton(types_names[3],
                                     callback_data='b3')
markup_type = agt.InlineKeyboardMarkup(resize_keyboard=True)

markup_type.row(t_button0, t_button1)
markup_type.row(t_button2, t_button3)

REGION = 'Теперь выберите страну производителя.' \
         '\nПожалуйста, напечатайте одну страну из списка:'

regions_div_block = soup.find_all('div')[16]
regions = regions_div_block.find_all('option')
regions_names = [region.text.strip() for region in regions]
regions_names = [' '.join(region.split(' ')[:-1]) for region in regions_names]
regions_codes = [region['value'] for region in regions] #nice
regions_code_to_name = dict(zip(regions_names, regions_codes))
regions_dict = dict(zip(regions_codes, regions_names))

REGIONS_LIST = '\n'.join(regions_names)
REGION_ERROR = 'Такой страны я не знаю'

STRENGTH = 'Теперь выберите крепость напитка'

strengths_div_block = soup.find_all('div')[20]
strengths = strengths_div_block.find_all('option')
strengths_names = [strength.text.strip() for strength in strengths] #nice
strengths_codes = [strength['value'] for strength in strengths] #nice
strengths_code_to_name = dict(zip(strengths_codes, strengths_names))
sorted_sctn = {strengths_codes[0]: strengths_names[0],
               strengths_codes[1]: strengths_names[4],
               strengths_codes[2]: strengths_names[1],
               strengths_codes[3]: strengths_names[2],
               strengths_codes[4]: strengths_names[3],
               strengths_codes[5]: strengths_names[5]}

s_button0 = agt.InlineKeyboardButton(strengths_names[0],
                                     callback_data='c0')
s_button1 = agt.InlineKeyboardButton(strengths_names[4],
                                     callback_data='c1')
s_button2 = agt.InlineKeyboardButton(strengths_names[1],
                                     callback_data='c2')
s_button3 = agt.InlineKeyboardButton(strengths_names[2],
                                     callback_data='c3')
s_button4 = agt.InlineKeyboardButton(strengths_names[3],
                                     callback_data='c4')
s_button5 = agt.InlineKeyboardButton(strengths_names[5],
                                     callback_data='c5')
markup_strength = agt.InlineKeyboardMarkup(resize_keyboard=True)

markup_strength.row(s_button0, s_button1)
markup_strength.row(s_button2, s_button3)
markup_strength.row(s_button4, s_button5)

DONE = 'Параметры заданы.' \
       '\nИспользуйте команду /guideme'

SHOW = 'Предпочтения пока ещё не заданы.'