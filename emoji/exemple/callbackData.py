from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

bot = Bot(token='6632849538:AAFOSXP-UBCmgdDu8d-8XmLvfZ41JSjewDY')
dp = Dispatcher(bot)

cd = CallbackData('ikb', 'action')

ikb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('Button', callback_data=),InlineKeyboardButton('dislike', callback_data='dislike')],
 ])

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer('text',reply_markup=ikb)

@dp.callback_query_handler(text='hello')
async  def ikb_callback(callback: types.CallbackQuery):
    await callback.answer('Somesing')

executor.start_polling(dp)