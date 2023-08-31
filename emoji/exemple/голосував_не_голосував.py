from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = Bot(token='6632849538:AAFOSXP-UBCmgdDu8d-8XmLvfZ41JSjewDY')
dp = Dispatcher(bot)

fuse = False

ikb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('like', callback_data='like'),InlineKeyboardButton('dislike', callback_data='dislike')],
    [InlineKeyboardButton('close keyboard',callback_data='close')]
])
@dp.message_handler(commands=['start'])
async def cmd_start(message):

    await bot.send_photo(chat_id=message.from_user.id,
                         photo='https://content1.rozetka.com.ua/goods/images/big/311240182.jpg',
                         caption='do yu like?',
                         reply_markup=ikb)

@dp.callback_query_handler(text='close')
async def ikb_close(callback):
    await callback.message.delete()

@dp.callback_query_handler()
async def ikb_close1(callback):
    global fuse
    if not fuse: #якщо не голосував\
        if callback.data == 'like':
            await callback.answer(text='Тобі сподобалось')
            fuse = True
        await callback.answer(text='Тобі не сподобалось')
        fuse = True
    await callback.answer('Ти уже голосував',
                          show_alert=True)

executor.start_polling(dp)