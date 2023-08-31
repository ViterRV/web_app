from aiogram.types import InlineKeyboardButton, \
    InlineKeyboardMarkup, \
    ReplyKeyboardMarkup,\
    KeyboardButton

inline_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Радість 😁", callback_data="Радість")],
    [InlineKeyboardButton(text="Сила 💪", callback_data="Сила")],
    [InlineKeyboardButton(text="Спокій ☺️", callback_data="Спокій")],
    [InlineKeyboardButton(text="Смуток 😞", callback_data="Смуток")],
    [InlineKeyboardButton(text="Навіженість 😡", callback_data="Навіженість")],
    [InlineKeyboardButton(text="Страх 😨", callback_data="Страх")]
])
key_fear = ("Покинутість","Збентеження","Безпорадність","Покірність","Безнадійність","Тривожність")
key_fury = ("Вразливість","Ворожість","Злість","Лютість","Ненависть","Прискіпливість")
key_sadness = ("Провина","Сором","Подавленість","Самотність","Нудьга","Млявість")
key_calm = ("Умиротворення","Замисленість","Близкість","Ніжність","Довіра","Стриманість")
key_force = ("Гордість","Повага","Визнання","Впевненість","Величність","Відданість")
key_happy = ("Захоплення","Чуттєвість","Енергійність","Грайливість","Творчість","Усвідомленість")

def keyboard(key):
    inline_kb = []
    for i in key:
        inline_kb.append([InlineKeyboardButton(text=i, callback_data=i)])
    return InlineKeyboardMarkup(inline_keyboard=inline_kb)




rkm = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(text="Додати запис ✍️"),
                                KeyboardButton(text="Переглянути записи 👀")).add(
                                KeyboardButton(text="Редагувати запис 📝"),
                                KeyboardButton(text="Видалити запис ✖️"))


def update_keyboard(records):
    keyboard = []
    for record_id, record_info in records.items():
        keyboard.append([InlineKeyboardButton(text=record_info['display_text'], callback_data=f"edit_record_{record_id}")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

