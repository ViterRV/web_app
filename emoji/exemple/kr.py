'''from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import random

bot = Bot(token="6632849538:AAFOSXP-UBCmgdDu8d-8XmLvfZ41JSjewDY")
dp = Dispatcher(bot)

async def on_startup(_):
    print("Bot starting")

HELP_COMMAND = """
/start - <em>Start</em>
/desk - <em>desk</em>"""

b1 = KeyboardButton('/help')
b2 = KeyboardButton('❤️')
kb = ReplyKeyboardMarkup().add(b1,b2)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text='HELLO',
                           reply_markup=kb)

@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    await bot.send_message(text=HELP_COMMAND,parse_mode="HTML")

@dp.message_handler(commands=['desc'])
async def help(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text = '❤️')
@dp.message_handler()
async def set_smile(message):
    if message.text == '❤️':
        await message.reply('😃')

#@dp.message_handler(commands=['help'])
#async def answer(message: types.Message):
#    await message.answer(text=message.text(random.randint(A-Z)))
#executor.start_polling(dp,skip_updates=True, on_startup=on_startup)

@dp.message_handler(commands=['desc'])
async def desc(message: types.Message):
    await message.answer(text='bot answer')


executor.start_polling(dp,skip_updates=True, on_startup=on_startup)'''


'''from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, \
    InlineKeyboardButton, \
    ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, \
    KeyboardButton

bot = Bot(token='6632849538:AAFOSXP-UBCmgdDu8d-8XmLvfZ41JSjewDY')
dp = Dispatcher(bot)

async def on_startup(_):
    print('Bot starting')

kb = ReplyKeyboardMarkup(resize_keyboard=True)
b1 = KeyboardButton(text='/help')
b2 = KeyboardButton(text='/vote')
kb.add(b1,b2)

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):


    await bot.send_message(chat_id=message.from_user.id,
                           text='Wolcome',
                           reply_markup=kb)

@dp.message_handler(commands=['vote'])

async def vote_command(message: types.Message):
    inb1 = InlineKeyboardButton(text='😀', callback_data="like")
    inb2 = InlineKeyboardButton(text='😕', callback_data="dislike")
    ikb = InlineKeyboardMarkup().add(inb1, inb2)
    await bot.send_photo(chat_id=message.from_user.id,
                         photo="https://static.ukrinform.com/photos/2022_12/thumb_files/630_360_1671628705-480.jpeg",
                         caption='Подабаэться?',
                         reply_markup=ikb)

@dp.callback_query_handler()
async def vote_callbeck(callback: types.CallbackQuery):
    if callback.data == "like":
        await callback.answer(text=callback.data)
    await callback.answer('Тобі не сподобалось')

executor.start_polling(dp,skip_updates=True, on_startup=on_startup)'''


from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove,KeyboardButton
import random

bot = Bot(token='6632849538:AAFOSXP-UBCmgdDu8d-8XmLvfZ41JSjewDY')
dp = Dispatcher(bot)
photo = ['https://www.deutschland.de/sites/default/files/media/image/tdt_10082022_ukraine_initiativen_muenchen.jpg',
         'https://www.atlanticcouncil.org/wp-content/uploads/2023/06/2023-06-11T000000Z_1445971206_MT1NURPHO00083XOTJ_RTRMADP_3_DEMONSTRATION-STOP-THE-ECOCIDE-IN-UKRAINE-IN-KRAKOW-POLAND-scaled-e1686611301861.jpg']

async def on_startup(_):
    print('Bot starting')

b1 = KeyboardButton(text='/help')
b2 = KeyboardButton(text='/desc')
rkb = ReplyKeyboardMarkup(resize_keyboard=True).add(b1).add(b2)

bi1 = InlineKeyboardButton(text='😀', callback_data='Сподобалось')
bi2 = InlineKeyboardButton(text='😐',callback_data='Не сподобалось')
ikb = InlineKeyboardMarkup().add(bi1,bi2)
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(text='Hello',
                       reply_markup=rkb )
 
#@dp.message_handler(commands=['help'])

@dp.message_handler(commands=['desc'])
async def desc(message: types.Message):
    await bot.send_photo(chat_id=message.from_user.id,
                         photo=random.choice(photo),
                         reply_markup=ikb)

@dp.callback_query_handler()
async def call(callback: types.CallbackQuery):
    if callback.data == 'Сподобалось':
        await callback.answer('COOL')
    await callback.answer('Ugle')

executor.start_polling(dp,skip_updates=True, on_startup=on_startup)