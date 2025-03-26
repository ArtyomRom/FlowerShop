import os
from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton
from asgiref.sync import sync_to_async
from shop.models import Bouquet, Customer, Order
from telegram_bot.staticfiles import keyboards
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import dateparser

router = Router()


class CustomOccasionState(StatesGroup):
    waiting_for_custom_occasion = State()
    waiting_for_phone = State()


class OrderState(StatesGroup):
    waiting_for_name = State()
    waiting_for_address = State()
    waiting_for_delivery_time = State()
    waiting_for_phone = State()


@router.message(CommandStart())
async def start_handler(message: types.Message):
    user_name = (
        message.from_user.username
        if message.from_user.username
        else message.from_user.first_name
    )
    text = f"Привет, {user_name} 🙋‍♀️! FlowerShop приветствует тебя. К какому событию готовимся? Выберите один из вариантов, либо укажите свой"
    await message.answer(text, reply_markup=keyboards.get_occasion_keyboard())


@router.callback_query(lambda c: c.data == "occasion_other")
async def handle_other_occasion(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите ваш повод:")
    await state.set_state(CustomOccasionState.waiting_for_custom_occasion)
    await callback.answer()


@router.message(CustomOccasionState.waiting_for_custom_occasion)
async def process_custom_occasion(message: types.Message, state: FSMContext):
    user_occasion = message.text
    text = f"Спасибо! Вы указали повод: *{user_occasion}* 💐"
    keyboard = keyboards.get_occasion_keyboard()
    await message.answer(text, parse_mode="Markdown", reply_markup=keyboard)
    await state.clear()


@router.callback_query(lambda c: c.data == "view_collection")
async def view_collection(callback: types.CallbackQuery):
    bouquets = await sync_to_async(list)(Bouquet.objects.all())
    if not bouquets:
        await callback.message.answer("К сожалению, пока нет доступных букетов 😔")
        return
    for bouquet in bouquets:
        text = (
            f"🌸 *{bouquet.name}*\n{bouquet.description}\n💰 Цена: {bouquet.price} руб."
        )
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="✅ Выбрать этот букет",
                        callback_data=f"bouquet_{bouquet.id}",
                    )
                ]
            ]
        )
        if bouquet.image:
            image_path = bouquet.image.path
            if os.path.exists(image_path):
                img_input = FSInputFile(image_path)
                await callback.message.answer_photo(
                    img_input,
                    caption=text,
                    parse_mode="Markdown",
                    reply_markup=keyboard,
                )
            else:
                await callback.message.answer(
                    f"Изображение для букета {bouquet.name} не найдено!"
                )
        else:
            await callback.message.answer(
                text, parse_mode="Markdown", reply_markup=keyboard
            )
    await callback.answer()


@router.callback_query(lambda c: c.data == "consultation")
async def request_consultation(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "Пожалуйста, введите ваш номер телефона и наш администратор свяжется с вами в течение 20 минут"
    )
    await state.set_state(CustomOccasionState.waiting_for_phone)
    await callback.answer()


@router.message(CustomOccasionState.waiting_for_phone)
async def process_phone(message: types.Message, state: FSMContext):
    phone_number = message.text
    await message.answer(
        f"Спасибо! Ваш номер {phone_number} принят. Ожидайте звонка от администратора."
    )
    await state.clear()


@router.callback_query(lambda c: c.data.startswith("occasion_"))
async def handle_occasion(callback: types.CallbackQuery):
    occasion_key = callback.data.replace("occasion_", "")
    if occasion_key == "other":
        return
    bouquets = await sync_to_async(list)(Bouquet.objects.filter(occasion=occasion_key))
    if not bouquets:
        await callback.message.answer(
            "К сожалению, у нас пока нет букетов для этого случая 😔"
        )
        return
    for bouquet in bouquets:
        text = (
            f"🌸 *{bouquet.name}*\n{bouquet.description}\n💰 Цена: {bouquet.price} руб."
        )
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="✅ Выбрать этот букет",
                        callback_data=f"bouquet_{bouquet.id}",
                    )
                ]
            ]
        )
        if bouquet.image:
            image_path = bouquet.image.path
            if os.path.exists(image_path):
                img_input = FSInputFile(image_path)
                await callback.message.answer_photo(
                    img_input,
                    caption=text,
                    parse_mode="Markdown",
                    reply_markup=keyboard,
                )
            else:
                await callback.message.answer(
                    f"Изображение для букета {bouquet.name} не найдено!"
                )
        else:
            await callback.message.answer(
                text, parse_mode="Markdown", reply_markup=keyboard
            )
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("bouquet_"))
async def handle_bouquet_selection(callback: types.CallbackQuery):
    bouquet_id = int(callback.data.replace("bouquet_", ""))
    try:
        bouquet = await sync_to_async(Bouquet.objects.get)(id=bouquet_id)
    except Bouquet.DoesNotExist:
        await callback.message.answer("Этот букет больше недоступен 😔")
        return

    text = f"🎉 Вы выбрали букет *{bouquet.name}*! 💐\n💰 Цена: {bouquet.price} руб."
    keyboard = keyboards.get_bouquet_keyboard(bouquet)
    await callback.message.answer(text, parse_mode="Markdown", reply_markup=keyboard)
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("order_"))
async def start_order(callback: types.CallbackQuery, state: FSMContext):
    bouquet_id = int(callback.data.replace("order_", ""))
    user, created = await sync_to_async(Customer.objects.get_or_create)(
        tg_id=callback.from_user.id
    )
    selected_bouquet = await sync_to_async(Bouquet.objects.get)(id=bouquet_id)
    await state.update_data(user_id=user.id, bouquet_id=selected_bouquet.id)

    await callback.message.answer("Введите ваше имя:")
    await state.set_state(OrderState.waiting_for_name)
    await callback.answer()


@router.message(OrderState.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    await sync_to_async(Customer.objects.filter(tg_id=message.from_user.id).update)(
        name=message.text
    )
    await message.answer("Спасибо! Теперь введите ваш адрес для доставки:")
    await state.set_state(OrderState.waiting_for_address)


@router.message(OrderState.waiting_for_address)
async def process_address(message: types.Message, state: FSMContext):
    await state.update_data(address=message.text)
    await message.answer(
        "Спасибо! Теперь введите дату и время доставки(в формате YYYY-MM-DD HH:MM):"
    )
    await state.set_state(OrderState.waiting_for_delivery_time)


@router.message(OrderState.waiting_for_delivery_time)
async def process_delivery_time(message: types.Message, state: FSMContext):
    parsed_date = dateparser.parse(message.text, languages=["ru"])
    if not parsed_date:
        await message.answer(
            "Вы некорректно ввели данные. Пожалуйста, введите дату и время доставки(в формате YYYY-MM-DD HH:MM)"
        )
        return
    await state.update_data(delivery_time=parsed_date)
    await message.answer("Спасибо! Теперь введите ваш номер телефона:")
    await state.set_state(OrderState.waiting_for_phone)


@router.message(OrderState.waiting_for_phone)
async def process_phone(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    user = await sync_to_async(Customer.objects.get)(id=user_data["user_id"])
    bouquet = await sync_to_async(Bouquet.objects.get)(id=user_data["bouquet_id"])
    order = await sync_to_async(Order.objects.create)(
        customer=user,
        bouquet=bouquet,
        address=user_data["address"],
        delivery_time=user_data["delivery_time"],
        status="new",
    )
    await message.answer(
        f"✅ Ваш заказ оформлен!\n💐 Букет: {bouquet.name}\n📍 Адрес: {user_data['address']}\n"
        f"⏳ Дата и время: {user_data['delivery_time']}\n📞 Телефон: {message.text}"
    )
    await state.clear()
