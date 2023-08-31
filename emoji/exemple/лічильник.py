from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
bot = Bot(token='6632849538:AAFOSXP-UBCmgdDu8d-8XmLvfZ41JSjewDY')
dp = Dispatcher(bot)

number = 0

def get_inline_key():
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Збільшити',callback_data='btn_increase'),
         InlineKeyboardButton(text='Зменшити',callback_data='btn_decrease')],
        [InlineKeyboardButton(text='рандомне число', callback_data='btn_random')]
    ])
    return ikb

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(f'поточне число {number}',
                         reply_markup=get_inline_key())


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('btn'))#будуть облоклятись тілльки ті запити що починаються з btn
async def ikb_callback(callback: types.CallbackQuery):
    global number
    if callback.data == 'btn_increase':
        number +=1
        await callback.message.edit_text(f'поточне число {number}',
                                         reply_markup=get_inline_key())
    elif callback.data == 'btn_decrease':
        number -=1
        await callback.message.edit_text(f'поточне число {number}',
                                         reply_markup=get_inline_key())
    elif callback.data == 'btn_random':

        await callback.message.edit_text(f'Число {random.randint(1,50)}',
                                         reply_markup=get_inline_key())

    else:
        1/0


executor.start_polling(dp)