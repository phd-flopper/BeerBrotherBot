from aiogram import types as agt
import urllib.request
import six
import requests
from bs4 import BeautifulSoup
import pandas as pd

user_preferences = [-1, -1, -1, -1]
#u_p[0] - region, u_p[1] - type, u_p[2] - colour, u_p[3] - strength
TEMP_CHECKER = [-1, -1, -1, -1]

GUIDANCE_FAILED = 'Будьте любезны для начала установить предпочтения.' \
                  '\nИспользуйте команду /set_preferences'
GUIDANCE = 'Позвольте же мне наставить Вас. Мне нужно немного времени, ' \
           'дабы собраться с мыслями.'

user_url = 'https://birra.ru/beer/search?'

GUIDANCE_NOT_FOUND = 'К сожалению удовлетворить Ваши предпочтения не ' \
                     'в моих силах' \
                     '.\nПопробуйте изменить их. /set_preferences'

recomended_beers = []
recomended_beers_images = []
names_to_links = ''

GUIDEME = ''

GUIDANCE_DONE = 'Если Вы считаете, что я ошибся с выбором - используйте' \
                'команду /guideme ещё раз. Иначе Вы можете использовать' \
                'команду /set_preferences, чтобы задать другие' \
                'предпочтения. Также Вы можете посмотреть свои предпочтения,' \
                'воспользовавшись командой /show_preferences.'