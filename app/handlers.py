from aiogram import F, Router
# from main import dp  <-- IT'S prohibited to do this ! u should import Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup

import app.keyboards as kb
from app.middlewares import SomeMiddleware
import app.database.requests as req

router = Router()
router.message.middleware(SomeMiddleware())  # внутренний работает ПОСЛЕ фильтра
# router.message.outer_middleware(SomeMiddleware())  # будет всегда срабатывать

class Register(StatesGroup):  # дочерний класс от StatesGroup
    name = State()
    age = State()
    number = State()

# #  Приветствие
# @dp.message(CommandStart())  # decorator - обработка сообщений
# async def cmd_start(message: Message):  # сообщения поступают сюда (класс Меssage обрабатываеt ответ 'message.answer')
#     await message.answer ('Hello, bro ')


# #  Приветствие с указанием ID
@router.message(CommandStart())  # decorator - обработка сообщений
async def cmd_first_start(message: Message):  # сообщения поступают сюда (класс Меssage обрабатываеt ответ 'message.answer')
    await req.set_user(message.from_user.id)  # в функцию 'set_user' передаем ID пользователя
    await message.reply(f'Привет,\nтвой ID: {message.from_user.id}\n'
                        f'Имя: {message.from_user.first_name}\n\nПриветствуем в магазине КОТОВ', # message.reply  - отвечает на сообщени

                        # Вызываем меню с выбором INLINE BUTTON (c беззубым фото)
                        # reply_markup=kb.small_info)  # 'kb.small_info' - файл 'small_info' в 'keyboards'

                        # Вызываем меню с выбором REPLY BUTTONS
                        reply_markup=kb.main)  # 'kb.main' - файл 'main' в 'keyboards'

                        # Вызываем меню с динамическим выбором машин
                        #Inline
                        # reply_markup=await kb.inline_cars())  # 'kb.main' - файл 'main' в 'keyboards'
                        # Reply
                        # reply_markup = await kb.inline_cars())  # 'kb.main' - файл 'main' в 'keyboards'
    await message.answer('Дорогой любитель Котяр, Вэлком!', reply_markup=kb.main)


@router.message(Command('help'))
async def get_help(message: Message):
    await message.answer('это команда /help, но она тебе не поможет')


@router.message(F.text == 'Как дела?')  # Ловит ВСЁ, что отправит пользователь: картинки, видео, локации
async def how_r_u(message: Message):
    await message.answer('Да что тебе нужно от меня, мешок с костями ......')

# #  Вариант с показом ID фото от пользователя
# @dp.message(F.photo)  # Ловит ВСЁ, что отправит пользователь: картинки, видео, локации
# async def get_photo (message: Message):
#     await message.answer(f'ID photo: {message.photo[-1].file_id}')  # message.photo[-1].file_id - ЛУЧШЕЕ качество картинки

# #  Вариант с комментарием к фото по ID фото
# @dp.message(Command ('get_photo'))  # Ловит ВСЁ, что отправит пользователь: картинки, видео, локации
# async def get_photo (message: Message):
#     await message.answer_photo(photo='AgACAgIAAxkBAAMSZ6Y0KQkgsuDQ1C5FctWEy7Gs7FgAAmfmMRsYHjBJPuSG5xha-_gBAAMCAAN5AAM2BA',
#     caption = 'это робот')

#  Вариант с сылкой на фото в инете
@router.message(Command ('get_photo'))  # Ловит ВСЁ, что отправит пользователь: картинки, видео, локации
async def get_photo(message: Message):
    await message.answer_photo(photo='https://kpfu.ru/portal/docs/F662567500/nao_debout.jpg',
                               caption='это робот')  # !!! ссылка на картинку с расширением

# КНОПКА 'КOШАКИ'

#@dp.message(F.text == 'Хорошо')  # decorator - work with messages
@router.message(F.text == 'КОШАКИ')  # decorator - work with messages from app.keyboards  "Каталог Котяр"
async def catalog(message: Message):  # messages will go here
    await message.answer('Мне от этого легче не стало, мешок с костями ! \n Но если ты хотел найти котов -смотри здесь',
                         reply_markup=kb.catalog)  # принимает и обрабатывает выбор из файла keyboards main "Каталог"


# МЕНЮ 'КOШАКИ'

@router.callback_query(F.data == 'Shaggy')
async def shaggy(callback: CallbackQuery):
    await callback.answer('Любишь с волосиками ?', show_alert=True)  # show_alert=True  - более навязчивое уведомление
    await callback.message.answer_photo(photo='https://i.pinimg.com/originals/de/d3/db/ded3db2bce7c951938bf5984b3c63643.jpg', caption='В доме, где живет кот : \n шерсть - это приправа')

@router.callback_query(F.data == 'Bold as a toad')
async def bold (callback: CallbackQuery):
    await callback.answer('Ленишься шерсть пропылесосить?', show_alert=True)
    await callback.message.answer_photo(photo='https://i0.wp.com/rusnord.ru/uploads/posts/2023-03/1662165001_1-oir-mobi-p-blatnoi-kot-instagram-1.jpg?ssl=1', caption='Пот - не шерсть  \n Топай -вытирай')

@router.callback_query(F.data == 'In between')
async def middle (callback: CallbackQuery):
    await callback.answer('Да что ж ты за человек такой ....', show_alert=True)
    await callback.message.answer_photo(photo='https://i.pinimg.com/originals/18/c7/ae/18c7ae86f29272ab3f096e5d39bbef63.jpg', caption='Ты на помойке его нашел?')


# МЕНЮ МАШИНЫ c cылкой на клавиатуру 'inline_cars'

@router.callback_query(F.data == 'Cars')
async def shaggy(callback: CallbackQuery):
    await callback.answer('Тачку на прокачку ', show_alert=True)  # show_alert=True  - более навязчивое уведомление
    await callback.message.edit_text('тачки, тачки, х#я@ки', reply_markup=await kb.inline_cars())


# РЕГИСТРАЦИЯ ПОЛЬЗОВАТЕЛЯ  через команду '/register'

@router.message(Command('register'))  # '/register' для активации ввести в терминале
async def register(message: Message, state: FSMContext):
    await state.set_state(Register.name)  # устанавливаем состояние 'Register.name'
    await message.answer('Введите Ваше имя ') #  задаем пользователю вопрос

@router.message(Register.name)
async def register_name (message: Message, state: FSMContext):
    await state.update_data(name=message.text)  # сохраняем информацию 'update_data' под ключем  'name' , то, что прислал 'message.text'
    await state.set_state(Register.age)  # user will press the register and obtain 'Register.age'
    await message.answer ('Введите Ваш возраст ')

@router.message(Register.age)
async def register_age (message: Message, state: FSMContext):
    await state.update_data(age=message.text)  # сохраняем информацию 'update_data' под ключем  'name' , то, что прислал 'message.text'
    await state.set_state(Register.number)  # user will press the register and obtain 'Register.age'
    await message.answer('Отправить свой номер', reply_markup=kb.get_number)  # user will send his number from 'Keybords.getnumber'

@router.message(Register.number, F.contact)  # F.contact - пользователь отправит нам только контакт
async def register_number(message: Message, state: FSMContext):
    await state.update_data(number=message.contact.phone_number)  # сохранили информацию и показать номер "message.contact.phone_number"
    data = await state.get_data()  # извлекаем сохраненную информацию
    await message.answer(f'Ваше имя: {data["name"]}\nВаш возраст: {data["age"]}\nВаш номер: {data["number"]}')  # выводим собранную информацию
    await state.clear()  # Очистить состояние, чтобы пользователь продолжил пользоваться ботом


#  МЕНЮ МАГАЗИНА

@router.message(F.text == 'МЕШОК ДЛЯ КОТОВ')
async def cat_catalog(message: Message):  # catalog -> cat_catalog   !!!!!!!!!!
    await message.answer('Выберите тип кота', reply_markup=await kb.categories())

@router.callback_query(F.data.startswith('category_'))
async def category(callback: CallbackQuery):
    await callback.answer('Вы выбрали категорию')
    await callback.message.answer('Выберите породу кота',
                                  reply_markup=await kb.items(callback.data.split('_')[1]))


@router.callback_query(F.data.startswith('item_'))
async def category(callback: CallbackQuery):
    item_data = await req.get_item(callback.data.split('_')[1])
    await callback.answer('Вы выбрали кошку')
    await callback.message.answer(f'Название: {item_data.name}\nХарактер: {item_data.description}\nЦена: {item_data.price} ₽',
                                  reply_markup=await kb.items(callback.data.split('_')[1]))

