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
        [InlineKeyboardButton(text="~2000 руб.", callback_data="price_2000")],
        [InlineKeyboardButton(text="~3000 руб.", callback_data="price_3000")],
        [InlineKeyboardButton(text="~4000 руб.", callback_data="price_4000")],
        [InlineKeyboardButton(text="~5000 руб.", callback_data="price_5000")],
        [InlineKeyboardButton(text=">5000 руб.", callback_data="price_over5000")],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)
