from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.filters import Text
from sq import db_start, create_profile, edit_profile,read_db, update_profile,delete_profile,check_record
from keyboard import inline_kb, rkm, key_force,key_happy,key_calm,key_sadness,key_fury,key_fear,keyboard
from datetime import datetime
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

storage = MemoryStorage() #створюємо екземпляр нашого сховища, де будуть зберігатись дані нашого стану (дані зв'язані з цими станами)
bot = Bot(token='6632849538:AAFOSXP-UBCmgdDu8d-8XmLvfZ41JSjewDY')
dp = Dispatcher(bot, storage=storage)


async def on_startup(_):
    await db_start()


class ProfileStates(StatesGroup): #клас що буде зберігати всі необхідні стани нашого бота
    id_update = State()
    id_delete = State()
    emoji = State()
    emoji1 = State()
    value = State()
    what_heppend = State()
    editing = State()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer('Menu',
                        reply_markup=rkm)

@dp.message_handler(Text(equals="Переглянути записи 👀"))
async def read(message: types.Message):
    if message.from_user.id == 346422904:
        data = await read_db()
        await message.answer(data)
    else:
        data = await read_db(user_id= message.from_user.id)
        await message.answer(data)

@dp.message_handler(Text(equals="Видалити запис ✖️"))
async def delete(message: types.Message):
    if message.from_user.id == 346422904:
        data = await read_db()
        await message.answer(text=f"<b>Список записів:</b>\n\n{data}\n\nВведіть номер ID запису для видалення",
                             parse_mode=types.ParseMode.HTML)
    else:
        data = await read_db(user_id=message.from_user.id)
        await message.answer(text=f"<b>Список записів:</b>\n\n{data}\n\nВведіть номер ID запису для видалення",
                             parse_mode=types.ParseMode.HTML)

    await ProfileStates.id_delete.set()
@dp.message_handler(state=ProfileStates.id_delete)
async def number_id_for_delete(message,state:FSMContext):
    try:
        id = int(message.text)
        if id > 0:
            async with state.proxy() as data:
                data['id_delete'] = id
            if message.from_user.id == 346422904:
                data = await check_record(id=id)
                if data == True:
                    await delete_profile(id)
                    await message.answer(f'Запис № {id} видалено')
                else:
                    await message.answer(f'Запису № {id} не існує')
            else:
                data = await check_record(id=id,user_id=message.from_user.id)
                if data == True:
                    await delete_profile(id)
                    await message.answer(f'Запис № {id} видалено')
                else:
                    await message.answer(f'Запису № {id} не існує')
        else:
            await message.reply('Введіть коректне число')
    except ValueError:
        await message.answer('Введіть коректне число1')
    await state.finish()


@dp.message_handler(Text(equals="Додати запис ✍️"))
async def start(message: types.Message):
    await message.answer("Привіт! Як справи? Обери свій стан!",
                        reply_markup=inline_kb)

    await ProfileStates.emoji.set()  # установлюмо стан емоції

@dp.callback_query_handler(state=ProfileStates.emoji)
async def callback_emoji(callback: types.CallbackQuery, state:FSMContext):
    async with state.proxy() as data: #відкриваємо локальний менеджер збереження даних де будемо тимчасово зберігати дані
        data['emoji'] = callback.data
    if data['emoji'] == "Радість":
        await callback.message.reply(text='зробіть вибір', reply_markup=keyboard(key_happy))
    elif data['emoji'] == "Сила":
        await callback.message.reply(text='зробіть вибір', reply_markup=keyboard(key_force))
    elif data['emoji'] == "Спокій":
        await callback.message.reply(text='зробіть вибір', reply_markup=keyboard(key_calm))
    elif data['emoji'] == "Смуток":
        await callback.message.reply(text='зробіть вибір', reply_markup=keyboard(key_sadness))
    elif data['emoji'] == "Навіженість":
        await callback.message.reply(text='зробіть вибір', reply_markup=keyboard(key_fury))
    elif data['emoji'] == "Страх":
        await callback.message.reply(text='зробіть вибір', reply_markup=keyboard(key_fear))
    await ProfileStates.next()


@dp.callback_query_handler(state=ProfileStates.emoji1)
async def emoji1(callback: types.CallbackQuery, state:FSMContext):
    async with state.proxy() as data:
        data['emoji1'] = callback.data
    await callback.message.reply('Виберіть рівень емоції від 0 до 10')
    await ProfileStates.next()


@dp.message_handler(state=ProfileStates.value)
async def get_emotion_level(message: types.Message, state: FSMContext):
    try:
        level = int(message.text)
        if 0 <= level <= 10:
            async with state.proxy() as data:
                data['value'] = level
            await message.reply('Що спровокувало?')
            await ProfileStates.next()
        else:
            await message.answer('Введіть рівень емоції від 0 до 10')
    except ValueError:
        await message.answer('Введіть коректне число від 0 до 10')

@dp.message_handler(state=ProfileStates.value)
async def value_emoji(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['value'] = message.text

    await message.reply('Що спровокувало?')
    await ProfileStates.next()

@dp.message_handler(state=ProfileStates.what_heppend)
async def what_heppend(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['what_heppend'] = message.text

    if 'id_update' in data:  # Перевірка наявності ключа 'id' в словнику data
        await update_profile(state, id=data['id_update'], user_id=message.from_user.id, user_name=message.from_user.full_name,
                             time=datetime.now())
        await message.answer('Запис відредаговано')
        await state.finish()
    else:
        await edit_profile(state, user_id=message.from_user.id, user_name=message.from_user.full_name,
                           time=datetime.now())
        await message.answer('Запис додано')
        await state.finish()


@dp.message_handler(Text(equals="Редагувати запис 📝"))
async def edit_records(message: types.Message):
    if message.from_user.id == 346422904:
        data = await read_db()
        await message.answer(text=f"<b>Список записів:</b>\n\n{data}\n\nВведіть номер ID запису для редагування",
                             parse_mode=types.ParseMode.HTML)
    else:
        data = await read_db(user_id=message.from_user.id)
        await message.answer(text=f"<b>Список записів:</b>\n\n{data}\n\nВведіть номер ID запису для редагування",
                             parse_mode=types.ParseMode.HTML)

    await ProfileStates.id_update.set()

@dp.message_handler(state=ProfileStates.id_update)
async def number_id_for_update(message,state:FSMContext):
    try:
        id = int(message.text)
        if id > 0:
            async with state.proxy() as data:
                data['id_update'] = id
            if message.from_user.id == 346422904:
                data = await check_record(id=id)
                if data == True:
                    await message.answer('Виберіть емоцію', reply_markup=inline_kb)
                    print(message.text)
                    await ProfileStates.emoji.set()
                else:
                    await message.answer(f'Запису № {id} не існує')
            else:
                data = await check_record(id=id,user_id=message.from_user.id)
                if data == True:
                    await message.answer('Виберіть емоцію', reply_markup=inline_kb)
                    print(message.text)
                    await ProfileStates.emoji.set()
                else:
                    await message.answer(f'Запису № {id} не існує')
        else:
            await message.reply('Введіть коректне число')
    except ValueError:
        await message.answer('Введіть коректне число')


executor.start_polling(dp,
                       on_startup=on_startup)

