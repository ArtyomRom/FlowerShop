from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_help_keyboard():
    buttons=[
        [InlineKeyboardButton(text="🌸 Заказать консультацию", callback_data="consultation")],
        [InlineKeyboardButton(text="📚 Посмотреть всю коллекцию", callback_data="view_collection")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
     

def get_occasion_keyboard():
    """Генерирует inline-клавиатуру с поводами"""
    buttons = [
        [InlineKeyboardButton(text="🎂 День рождения", callback_data="occasion_birthday")],
        [InlineKeyboardButton(text="💍 Свадьба", callback_data="occasion_wedding")],
        [InlineKeyboardButton(text="🎒 В школу", callback_data="occasion_school")],
        [InlineKeyboardButton(text="💐 Без повода", callback_data="occasion_no_reason")],
        [InlineKeyboardButton(text="❓ Другой повод", callback_data="occasion_other")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_select_price():
    """Генерирует inline-клавиатуру с выбором цены"""
    buttons = [
        [InlineKeyboardButton(text="~500 руб.", callback_data="price_500")],
        [InlineKeyboardButton(text="~1000 руб.", callback_data="price_1000")],
        [InlineKeyboardButton(text="~2000 руб.", callback_data="price_2000")],
        [InlineKeyboardButton(text=">2000 руб.", callback_data="price_over2000")],
        [InlineKeyboardButton(text="Неважно", callback_data="price_nometter")],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)
