from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from app.database.requests import get_categories, get_category_item   # импорт функции из 'requests'

# Динамичные клавиатуры
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder



main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='КОШАКИ')],
    [KeyboardButton(text='МЕШОК ДЛЯ КОТОВ'),KeyboardButton(text='ПОЗВОНИТЬ ХОЗЯЕВАМ')]
],
resize_keyboard=True,  # изменение размера клавиатуры
input_field_placeholder='Тапай кнопки,  разминай пальцы')  # задний фон сообщения


""" список - это сама клавиатура,  
    внутри клавиатуры есть ряды 
    внутри ряда мы создаем кнопку """

catalog = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Мохнатки',  callback_data='Shaggy')],
    [InlineKeyboardButton(text='Плешивые',  callback_data='Bold as a toad')],
    [InlineKeyboardButton(text='Что-то среднее', callback_data='In between')],   # одна кнопка в одной строке
    [InlineKeyboardButton(text='Машины', callback_data='Cars')]])   # одна кнопка в одной строке

#  фото с беззубым

small_info = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='А ЭТО ТВОЁ ФОТО', url='https://live.staticflickr.com/3145/3095158490_1fde96bb13_b.jpg')]
    ], resize_keyboard=True)  # сноска под основной текст информации о пользователе

#  регистрация номера
get_number = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отправить свой номер', request_contact=True)]],
                                 resize_keyboard=True)  # Запрос на отправку номера

""" Inline не отправляет текст в чат, а показывает инфо   
    поэтому дополнительно используется "callback_data"  
    благодаря этому свойству мы понимаем, что отправили именно это сообщение """

# Динамичные клавиатуры
cars = ['VW', 'MB', 'BMW', 'Tesla']

#  REPLY
async def reply_cars():
    keyboard = ReplyKeyboardBuilder()
    for car in cars:
        keyboard.add(KeyboardButton(text=car))
    return keyboard.adjust(2).as_markup()

#  INLINE
async def inline_cars():
    keyboard = InlineKeyboardBuilder()
    for car in cars:
        # Inline HE может быть ТОЛЬКО текст - либо + ссылка , либо + URL
        keyboard.add(InlineKeyboardButton(text=car, url='https://live.staticflickr.com/3145/3095158490_1fde96bb13_b.jpg'))
    return keyboard.adjust(2).as_markup()  # !!! в одном ряду 2 кнопки - 'adjust(2)'


# КАТАЛОГИ

async def categories():
    all_categories = await get_categories()
    keyboard = InlineKeyboardBuilder()
    for category in all_categories:
        keyboard.add(InlineKeyboardButton(text=category.name, callback_data=f"category_{category.id}"))
        # ловит все 'callback_data'  , которые начинаются с 'category_'  и вытаскивает 'category.id'
    keyboard.add(InlineKeyboardButton(text='Назад', callback_data='to_main'))
    return keyboard.adjust(2).as_markup()
    # 'adjust' - регулировка клавиатуры по ширине (2 кнопки),
    # '.as_markup()' - всегда, когда используется '...Builder', чтобы превратить в клавиатуру



async def items(category_id):
    all_items = await get_category_item(category_id)
    keyboard = InlineKeyboardBuilder()
    for item in all_items:
        keyboard.add(InlineKeyboardButton(text=item.name, callback_data=f"item_{item.id}"))
    keyboard.add(InlineKeyboardButton(text='Назад', callback_data='to_main'))
    return keyboard.adjust(2).as_markup()