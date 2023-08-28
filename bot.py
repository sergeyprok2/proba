#  import callback as callback

print('Господи, помилуй.')
print('Слава Тебе, Бог наш, Слава Тебе.')
print()
import csv, json, os, sys, time, schedule, random
# from crontab import CronTab
from datetime import datetime
# import pandas as pd
from pprint import pprint
import time
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, Text, BaseFilter, CommandStart, StateFilter
from aiogram.types import ContentType, BotCommand, CallbackQuery
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.fsm.storage.redis import RedisStorage, Redis
# import os, dotenv
from environs import Env
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from config import Config, load_config


# from playwright_stealth import stealth_async

config1 = load_config()
BOT_TOKEN: str = config1.tg_bot.token
# Вместо BOT TOKEN HERE нужно вставить токен вашего бота,
# полученный у @BotFather
# API_TOKEN: str = '5959145787:AAHKfsD3UgNhcXuY78EoV0tqE8ZNAn7lK6w'
# Инициализируем Redis
redis: Redis = Redis(host='localhost')
# Инициализируем хранилище (создаем экземпляр класса RedisStorage)
storage: RedisStorage = RedisStorage(redis=redis)

# Создаем объекты бота и диспетчера
bot: Bot = Bot(token=BOT_TOKEN)
dp: Dispatcher = Dispatcher(storage=storage)

# Создаем "базу данных" пользователей
user_dict: dict[int, dict[str, str | int | bool]] = {}

# Cоздаем класс, наследуемый от StatesGroup, для группы состояний нашей FSM
class FSMFillForm(StatesGroup):
    # Создаем экземпляры класса State, последовательно
    # перечисляя возможные состояния, в которых будет находиться
    # бот в разные моменты взаимодейтсвия с пользователем
    fill_name = State()        # Состояние ожидания ввода имени
    fill_age = State()         # Состояние ожидания ввода возраста
    fill_gender = State()      # Состояние ожидания выбора пола
    upload_photo = State()     # Состояние ожидания загрузки фото
    fill_education = State()   # Состояние ожидания выбора образования
    fill_wish_news = State()   # Состояние ожидания выбора получать ли новости
    a = State()
    b = State()
    c = State()


# Создаем асинхронную функцию
async def set_main_menu(bot: Bot):
    # Создаем список с командами и их описанием для кнопки menu
    main_menu_commands = [
        BotCommand(command='/start',
                   description='Стартовать'),
        BotCommand(command='/help',
                   description='Справка по работе бота'),
        BotCommand(command='/support',
                   description='Поддержка'),
        BotCommand(command='/contacts',
                   description='Другие способы связи'),
        BotCommand(command='/cancel',
                   description='Платежи')]

    await bot.set_my_commands(main_menu_commands)


# Создаем объекты кнопок
button_1: KeyboardButton = KeyboardButton(text='1 кг')
button_2: KeyboardButton = KeyboardButton(text='Здесь пока ничего нет')
button_3: KeyboardButton = KeyboardButton(text='Здесь пока ничего нет')
button_4: KeyboardButton = KeyboardButton(text='Здесь пока ничего нет')
button_5: KeyboardButton = KeyboardButton(text='Посчитать')
button_6: KeyboardButton = KeyboardButton(text='Обнулить')

# Создаем объект клавиатуры, добавляя в него кнопки
keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
    keyboard=[[button_1, button_2, button_3, button_4, button_5, button_6]], resize_keyboard=True,
    one_time_keyboard=True)


# Этот хэндлер будет срабатывать на команду /start вне состояний
# и предлагать перейти к заполнению анкеты, отправив команду /fillform
@dp.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    await message.answer(text='Этот бот демонстрирует работу FSM\n\n'
                              'Чтобы перейти к заполнению анкеты - '
                              'отправьте команду /fillform')


# Этот хэндлер будет срабатывать на команду "/cancel" в любых состояниях,
# кроме состояния по умолчанию, и отключать машину состояний
@dp.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(text='Вы вышли из машины состояний\n\n'
                              'Чтобы снова перейти к заполнению анкеты - '
                              'отправьте команду /fillform')
    # Сбрасываем состояние
    await state.clear()


# Этот хэндлер будет срабатывать на команду "/cancel" в состоянии
# по умолчанию и сообщать, что эта команда доступна в машине состояний
@dp.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(text='Отменять нечего. Вы вне машины состояний\n\n'
                              'Чтобы перейти к заполнению анкеты - '
                              'отправьте команду /fillform')


# Этот хэндлер будет срабатывать на команду /fillform
# и переводить бота в состояние ожидания ввода имени
@dp.message(Command(commands='fillform'), StateFilter(default_state))
async def process_fillform_command(message: Message, state: FSMContext):
#     await message.answer(text='Пожалуйста, введите ваше имя')
#     # Устанавливаем состояние ожидания ввода имени
#     await state.set_state(FSMFillForm.fill_name)
#
#
# # Этот хэндлер будет срабатывать, если введено корректное имя
# # и переводить в состояние ожидания ввода возраста
# @dp.message(StateFilter(FSMFillForm.fill_name), F.text.isalpha())
# async def process_name_sent(message: Message, state: FSMContext):
    # Cохраняем введенное имя в хранилище по ключу "name"
    # await state.update_data(name=message.text)
#     await message.answer(text='Спасибо!\n\nА теперь введите ваш возраст')
#     # Устанавливаем состояние ожидания ввода возраста
#     await state.set_state(FSMFillForm.fill_age)
#
#
# # Этот хэндлер будет срабатывать, если во время ввода имени
# # будет введено что-то некорректное
# @dp.message(StateFilter(FSMFillForm.fill_name))
# async def warning_not_name(message: Message):
#     await message.answer(text='То, что вы отправили не похоже на имя\n\n'
#                               'Пожалуйста, введите ваше имя\n\n'
#                               'Если вы хотите прервать заполнение анкеты - '
#                               'отправьте команду /cancel')
#
#
# # Этот хэндлер будет срабатывать, если введен корректный возраст
# # и переводить в состояние выбора пола
# @dp.message(StateFilter(FSMFillForm.fill_age),
#             lambda x: x.text.isdigit() and 4 <= int(x.text) <= 120)
# async def process_age_sent(message: Message, state: FSMContext):
#     # Cохраняем возраст в хранилище по ключу "age"
#     await state.update_data(age=message.text)

    # Создаем объекты инлайн-кнопок
    male_button = InlineKeyboardButton(text='цена за кг',
                                       callback_data='male')
    female_button = InlineKeyboardButton(text='Женский ♀',
                                         callback_data='female')
    undefined_button = InlineKeyboardButton(text='🤷 Пока не ясно',
                                            callback_data='undefined_gender')
    # Добавляем кнопки в клавиатуру (две в одном ряду и одну в другом)
    keyboard: list[list[InlineKeyboardButton]] = [[male_button, female_button],
                                                  [undefined_button]]
    # Создаем объект инлайн-клавиатуры
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    # Отправляем пользователю сообщение с клавиатурой
    await message.answer(text='Спасибо!\n\nУкажите ваш пол',
                         reply_markup=markup)
    # Устанавливаем состояние ожидания выбора пола
    await state.set_state(FSMFillForm.fill_gender)


# Этот хэндлер будет срабатывать, если во время ввода возраста
# будет введено что-то некорректное
@dp.message(StateFilter(FSMFillForm.fill_age))
async def warning_not_age(message: Message):
    await message.answer(
        text='Возраст должен быть целым числом от 4 до 120\n\n'
             'Попробуйте еще раз\n\nЕсли вы хотите прервать '
             'заполнение анкеты - отправьте команду /cancel')


# Этот хэндлер будет срабатывать на нажатие кнопки при
# выборе пола и переводить в состояние отправки фото
@dp.callback_query(StateFilter(FSMFillForm.fill_gender),
                   Text(text=['male']))
async def process_gender_press(callback: CallbackQuery, state: FSMContext):
    # Cохраняем пол (callback.data нажатой кнопки) в хранилище,
    # по ключу "gender"
    await state.update_data(gender=callback.data)
    # Удаляем сообщение с кнопками, потому что следующий этап - загрузка фото
    # чтобы у пользователя не было желания тыкать кнопки
    # await callback.message.delete()
    await callback.message.answer(text='напишите вес')
    # Устанавливаем состояние ожидания загрузки фото
    await state.set_state(FSMFillForm.a)

@dp.message(StateFilter(FSMFillForm.a),
            lambda x: x.text.isdigit() and 4 <= int(x.text) <= 120000)
async def process_age_sent(message: Message, state: FSMContext):
    # Cохраняем возраст в хранилище по ключу "age"
    await state.update_data(wes=message.text)
    # print(message.answer(message.text))
    await message.answer(text='напишите цену')
    # Устанавливаем состояние ожидания выбора пола
    await state.set_state(FSMFillForm.b)


@dp.message(StateFilter(FSMFillForm.b),
            lambda x: x.text.isdigit() and 4 <= int(x.text) <= 120000)
async def process_age_sent(message: Message, state: FSMContext):
    # Cохраняем возраст в хранилище по ключу "age"
    await state.update_data(cena=message.text)
    # print(message.answer(message.text))
    # Добавляем в "базу данных" анкету пользователя
    # по ключу id пользователя
    print(await state.get_data())
    print(await state.get_state())
    user_dict[message.from_user.id] = await state.get_data()
    # Завершаем машину состояний
    await state.clear()
    # Отправляем в чат сообщение о выходе из машины состояний
    # await message.answer(text='Спасибо! Ваши данные сохранены!\n\n'
    #                                       'Вы вышли из машины состояний')
    # Отправляем в чат сообщение с предложением посмотреть свою анкету
#     await message.answer(text='Чтобы посмотреть данные вашей '
#                                        'анкеты - отправьте команду /showdata')
#
#
# # Этот хэндлер будет срабатывать, если во время согласия на получение
# # новостей будет введено/отправлено что-то некорректное
# @dp.message(StateFilter(FSMFillForm.fill_wish_news))
# async def warning_not_wish_news(message: Message):
#     await message.answer(text='Пожалуйста, воспользуйтесь кнопками!\n\n'
#                               'Если вы хотите прервать заполнение анкеты - '
#                               'отправьте команду /cancel')
#
#
# # Этот хэндлер будет срабатывать на отправку команды /showdata
# # и отправлять в чат данные анкеты, либо сообщение об отсутствии данных
# @dp.message(Command(commands='showdata'), StateFilter(default_state))
# async def process_showdata_command(message: Message):
    # Отправляем пользователю анкету, если она есть в "базе данных"
    if message.from_user.id in user_dict:
        y=int(user_dict[message.from_user.id]["wes"])
        r=int(user_dict[message.from_user.id]["cena"])
        await message.answer(
                    f'вес товара: {user_dict[message.from_user.id]["wes"]}\n'
                    f'цена товара: {user_dict[message.from_user.id]["cena"]}\n'
                    f'цена товара за 1 г: {round(r/y,2)}\n'
                    f'цена товара за 100 г: {round(r/y*100,2)}\n'
                    f'цена товара за 1 кг: {round(r/y*1000,2)}\n')
    else:
        # Если анкеты пользователя в базе нет - предлагаем заполнить
        await message.answer(text='Вы еще не заполняли анкету. '
                                  'Чтобы приступить - отправьте '
                                  'команду /fillform')


# Этот хэндлер будет срабатывать на любые сообщения, кроме тех
# для которых есть отдельные хэндлеры, вне состояний
@dp.message(StateFilter(default_state))
async def send_echo(message: Message):
    await message.reply(text='Извините, моя твоя не понимать')



# # Этот хэндлер будет срабатывать на нажатие кнопки при
# # выборе пола и переводить в состояние отправки фото
# @dp.callback_query(StateFilter(FSMFillForm.fill_gender),
#                    Text(text=['female']))
# async def process_gender_press(callback: CallbackQuery, state: FSMContext):
#     # Cохраняем пол (callback.data нажатой кнопки) в хранилище,
#     # по ключу "gender"
#     await state.update_data(gender=callback.data)
#     # Удаляем сообщение с кнопками, потому что следующий этап - загрузка фото
#     # чтобы у пользователя не было желания тыкать кнопки
#     await callback.message.delete()
#     await callback.message.answer(text='напишите цену')
#     # Устанавливаем состояние ожидания загрузки фото
#     await state.set_state(FSMFillForm.a)
#
#
# # Этот хэндлер будет срабатывать на нажатие кнопки при
# # выборе пола и переводить в состояние отправки фото
# @dp.callback_query(StateFilter(FSMFillForm.fill_gender),
#                    Text(text=['undefined_gender']))
# async def process_gender_press(callback: CallbackQuery, state: FSMContext):
#     # Cохраняем пол (callback.data нажатой кнопки) в хранилище,
#     # по ключу "gender"
#     await state.update_data(gender=callback.data)
#     # Удаляем сообщение с кнопками, потому что следующий этап - загрузка фото
#     # чтобы у пользователя не было желания тыкать кнопки
#     await callback.message.delete()
#     await callback.message.answer(text='Спасибо! А теперь загрузите, '
#                                        'пожалуйста, ваше фото')
#     # Устанавливаем состояние ожидания загрузки фото
#     await state.set_state(FSMFillForm.upload_photo)
#
#
# # Этот хэндлер будет срабатывать, если во время выбора пола
# # будет введено/отправлено что-то некорректное
# @dp.message(StateFilter(FSMFillForm.fill_gender))
# async def warning_not_gender(message: Message):
#     await message.answer(text='Пожалуйста, пользуйтесь кнопками '
#                               'при выборе пола\n\nЕсли вы хотите прервать '
#                               'заполнение анкеты - отправьте команду /cancel')


if __name__ == '__main__':
    dp.startup.register(set_main_menu)
    dp.run_polling(bot)