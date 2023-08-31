from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.exceptions import BotBlocked
import asyncio 

bot = Bot(token='6632849538:AAFOSXP-UBCmgdDu8d-8XmLvfZ41JSjewDY')
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await asyncio.sleep(10)
    await message.answer('text')

@dp.errors_handler(exception=BotBlocked) #визначаємо що ми будемо обробляти
async def error(update, exception):
    print('Не можна відправити повідомлення бо нас заблокували')
    return True



executor.start_polling(dp)