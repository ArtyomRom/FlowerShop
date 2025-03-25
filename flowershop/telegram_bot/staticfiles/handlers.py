from aiogram import Router, types
import os

from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from asgiref.sync import sync_to_async
from shop.models import Bouquet, Customer, Order
from telegram_bot.staticfiles import keyboards
from aiogram.fsm.context import FSMContext  # Для управления состояниями
from aiogram.fsm.state import State, StatesGroup
import dateparser
router = Router()


@router.message(CommandStart())
async def start_handler(message: types.Message):
    """Приветственное сообщение с Inline-кнопками"""
    await message.answer(
        "К какому событию готовимся? Выберите один из вариантов, либо укажите свой",
        reply_markup=keyboards.get_occasion_keyboard()
    )


@router.callback_query(lambda c: c.data.startswith("occasion_"))
async def handle_occasion(callback: types.CallbackQuery):
    """Обработчик выбора повода через inline-кнопки"""
    occasion_key = callback.data.replace("occasion_", "")  # Достаем ключ

    # Достаем все букеты для этого случая
    bouquets = await sync_to_async(list)(Bouquet.objects.filter(occasion=occasion_key))

    if not bouquets:
        await callback.message.answer("К сожалению, у нас пока нет букетов для этого случая 😔")
        return

    for bouquet in bouquets:
        text = f"🌸 *{bouquet.name}*\n{bouquet.description}\n💰 Цена: {bouquet.price} руб."
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[
                InlineKeyboardButton(
                    text="✅ Выбрать этот букет",
                    callback_data=f"bouquet_{bouquet.id}"
                )
            ]]
        )

        # Проверяем, если изображение есть и оно локальное (например, лежит в папке media/)
        if bouquet.image:
            image_path = bouquet.image.path  # Получаем абсолютный путь к файлу изображения
            print(f"Путь к изображению: {image_path}")  # Печатаем путь для отладки

            if os.path.exists(image_path):
                print('Существует файл')
                # Используем FSInputFile для отправки локального изображения
                img_input = FSInputFile(image_path)  # Передаем путь к файлу в FSInputFile
                await callback.message.answer_photo(
                    img_input,  # Используем FSInputFile для отправки локального изображения
                    caption=text,
                    parse_mode="Markdown",
                    reply_markup=keyboard
                )
            else:
                await callback.message.answer(f"Изображение для букета {bouquet.name} не найдено!")
        else:
            await callback.message.answer(text, parse_mode="Markdown", reply_markup=keyboard)

        await callback.answer()


@router.callback_query(lambda c: c.data.startswith("bouquet_"))
async def handle_bouquet_selection(callback: types.CallbackQuery):
    """Обработчик выбора букета"""
    bouquet_id = int(callback.data.replace("bouquet_", ""))

    try:
        bouquet = await sync_to_async(Bouquet.objects.get)(id=bouquet_id)
    except Bouquet.DoesNotExist:
        await callback.message.answer("Этот букет больше недоступен 😔")
        return

    text = f"🎉 Вы выбрали букет *{bouquet.name}*! 💐\n💰 Цена: {bouquet.price} руб."

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(
            text="🛒 Оформить заказ", callback_data=f"order_{bouquet.id}"),
            InlineKeyboardButton(
                text="🌸 Заказать консультацию", callback_data=f"consultation_{bouquet.id}")],
            [InlineKeyboardButton(
                text="📚 Посмотреть всю коллекцию", callback_data="view_collection")]
        ]
    )

    await callback.message.answer(text, parse_mode="Markdown", reply_markup=keyboard)
    await callback.answer()


# @router.callback_query(lambda c: c.data.startswith("order_"))
# async def handle_order(callback: types.CallbackQuery):
#     """Обработчик оформления заказа"""
#     bouquet_id = int(callback.data.replace("order_", ""))
#     try:
#         bouquet = await sync_to_async(Bouquet.objects.get)(id=bouquet_id)
#     except Bouquet.DoesNotExist:
#         await callback.message.answer("Этот букет больше недоступен 😔")
#         return
#
#     # Сохраняем выбранный букет
#     user_data = await sync_to_async(Customer.objects.get_or_create)(tg_id=callback.from_user.id)
#     user_data = user_data[0]
#     user_data.selected_bouquet = bouquet
#     user_data.save()
#
#     # Запросим имя пользователя
#     await callback.message.answer("Введите ваше имя для оформления заказа.")
#     await callback.answer()


# @router.message(lambda message: message.text and not message.text.startswith('/'))
# async def collect_order_details(message: types.Message):
#     """Сбор данных для оформления заказа"""
#
#     # Получаем данные клиента по tg_id
#     try:
#         user_data = await sync_to_async(Customer.objects.get)(tg_id=message.from_user.id)
#     except Customer.DoesNotExist:
#         await message.answer("Ваши данные не найдены. Пожалуйста, зарегистрируйтесь.")
#         return
#
#     # Если у пользователя нет имени, запрашиваем его
#     if not user_data.name:
#         user_data.name = message.text
#         await sync_to_async(user_data.save)()  # Сохраняем имя
#         await message.answer("Спасибо! Теперь, пожалуйста, введите ваш адрес для доставки.")
#         return
#
#     # Если у пользователя нет адреса, запрашиваем его
#     if not hasattr(user_data, 'address') or not user_data.address:
#         user_data.address = message.text
#         await sync_to_async(user_data.save)()  # Сохраняем адрес
#         await message.answer("Спасибо за ваш адрес! Теперь введите дату и время доставки.")
#         return
#
#     # Если у пользователя нет даты и времени доставки, запрашиваем их
#     if not hasattr(user_data, 'delivery_time') or not user_data.delivery_time:
#         user_data.delivery_time = message.text
#         await sync_to_async(user_data.save)()  # Сохраняем дату и время
#         await message.answer("Спасибо! Теперь введите ваш номер телефона.")
#         return
#
#     # Если у пользователя нет телефона, запрашиваем его
#     if not user_data.phone:
#         user_data.phone = message.text
#         await sync_to_async(user_data.save)()  # Сохраняем телефон
#
#         # Получаем выбранный букет (здесь предполагается, что вы где-то храните выбор пользователя)
#         selected_bouquet = await sync_to_async(Bouquet.objects.get)(id=user_data.selected_bouquet.id)
#
#         # Создаем заказ
#         await sync_to_async(Order.objects.create)(
#             customer=user_data,
#             bouquet=selected_bouquet,
#             address=user_data.address,
#             delivery_time=user_data.delivery_time,
#             status="new"
#         )
#
#         await message.answer(
#             f"✅ Ваш заказ оформлен!\n💐 Букет: {selected_bouquet.name}\n📍 Адрес: {user_data.address}\n⏳ Дата и время: {user_data.delivery_time}\n📞 Телефон: {user_data.phone}")
# # @router.callback_query(lambda c: c.data.startswith("bouquet_"))
# # async def handle_bouquet_selection(callback: types.CallbackQuery):
# #     """Обработчик выбора букета"""
# #     bouquet_id = int(callback.data.replace("bouquet_", ""))
# #
# #     try:
# #         bouquet = await sync_to_async(Bouquet.objects.get)(id=bouquet_id)
# #     except Bouquet.DoesNotExist:
# #         await callback.message.answer("Этот букет больше недоступен 😔")
# #         return
# #
# #     text = f"🎉 Вы выбрали букет *{bouquet.name}*! 💐\n💰 Цена: {bouquet.price} руб."
# #
# #     keyboard = InlineKeyboardMarkup(
# #         inline_keyboard=[[
# #             InlineKeyboardButton(
# #                 text="🛒 Оформить заказ", callback_data=f"order_{bouquet.id}"
# #             )
# #         ]]
# #     )
# #
# #     await callback.message.answer(text, parse_mode="Markdown", reply_markup=keyboard)
# #     await callback.answer()
# #
# # @router.callback_query(lambda c: c.data.startswith("price_"))
# # async def handle_price_selection(callback: types.CallbackQuery):
# #     """Обработчик выбора цены"""
# #     price_key = callback.data.replace("price_", "")  # Достаем цену
# #     bouquet_id = callback.message.reply_to_message.text.split("_")[1]  # Извлекаем ID букета из текста сообщения
# #
# #     # Достаем выбранный букет из базы данных
# #     bouquet = await sync_to_async(Bouquet.objects.get)(id=bouquet_id)
# #
# #     # Проверяем, подходит ли выбранный букет под выбранную цену
# #     if price_key == "more":
# #         # Если больше, показываем все букеты, цена которых больше, чем выбранная
# #         bouquets = await sync_to_async(list)(Bouquet.objects.filter(price__gte=bouquet.price))
# #     elif price_key == "any":
# #         # Если "Не важно", то показываем этот букет
# #         bouquets = [bouquet]
# #     else:
# #         # Если выбрана конкретная цена, фильтруем по цене
# #         bouquets = await sync_to_async(list)(Bouquet.objects.filter(price=price_key))
# #
# #     # Отправляем пользователю фото и описание подходящего букета
# #     for bouquet in bouquets:
# #         text = f"🌸 *{bouquet.name}*\n{bouquet.description}\n💰 Цена: {bouquet.price} руб."
# #         if bouquet.image:
# #             await callback.message.answer_photo(photo=bouquet.image.url, caption=text, parse_mode="Markdown")
# #         else:
# #             await callback.message.answer(text, parse_mode="Markdown")
# #
# #     # Закрываем уведомление Telegram
# #     await callback.answer()
#         return

class OrderState(StatesGroup):
    waiting_for_name = State()
    waiting_for_address = State()
    waiting_for_delivery_time = State()
    waiting_for_phone = State()


# Начало оформления заказа
@router.callback_query(lambda c: c.data.startswith("order_"))
async def start_order(callback: types.CallbackQuery, state: FSMContext):
    """Обработчик начала оформления заказа"""

    bouquet_id = int(callback.data.replace("order_", ""))

    # Получаем пользователя по Telegram ID
    user, created = await sync_to_async(Customer.objects.get_or_create)(
        tg_id=callback.from_user.id
    )

    # Сохраняем букет в данные пользователя
    selected_bouquet = await sync_to_async(Bouquet.objects.get)(id=bouquet_id)

    # Сохраняем данные в FSM
    await state.update_data(user_id=user.id, bouquet_id=selected_bouquet.id)

    # Запрашиваем имя
    await callback.message.answer("Введите ваше имя:")
    await state.set_state(OrderState.waiting_for_name)

    await callback.answer()


# Обработчик ввода имени
@router.message(OrderState.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    """Сохранение имени и запрос адреса"""
    await sync_to_async(Customer.objects.filter(tg_id=message.from_user.id).update)(name=message.text)

    await message.answer("Спасибо! Теперь введите ваш адрес для доставки:")
    await state.set_state(OrderState.waiting_for_address)


# Обработчик ввода адреса
@router.message(OrderState.waiting_for_address)
async def process_address(message: types.Message, state: FSMContext):
    """Сохранение адреса и запрос даты/времени"""
    await state.update_data(address=message.text)

    await message.answer("Спасибо! Теперь введите дату и время доставки(в формате YYYY-MM-DD HH:MM):")
    await state.set_state(OrderState.waiting_for_delivery_time)
    # parsed_date = dateparser.parse(message.text, languages=["ru"])  # Парсим естественный ввод
    #
    # if not parsed_date:
    #     await message.answer("Не смог распознать дату 😔 Попробуйте еще раз, например: 'завтра в 18:00'.")
    #     return


# Обработчик ввода даты и времени доставки
@router.message(OrderState.waiting_for_delivery_time)
async def process_delivery_time(message: types.Message, state: FSMContext):
    """Сохранение даты/времени и запрос номера телефона"""
    await state.update_data(delivery_time=message.text)

    await message.answer("Спасибо! Теперь введите ваш номер телефона:")
    await state.set_state(OrderState.waiting_for_phone)


# Обработчик ввода номера телефона и создание заказа
@router.message(OrderState.waiting_for_phone)
async def process_phone(message: types.Message, state: FSMContext):
    """Сохранение номера телефона и финальное подтверждение заказа"""
    user_data = await state.get_data()

    user = await sync_to_async(Customer.objects.get)(id=user_data['user_id'])
    bouquet = await sync_to_async(Bouquet.objects.get)(id=user_data['bouquet_id'])

    # Создание заказа
    order = await sync_to_async(Order.objects.create)(
        customer=user,
        bouquet=bouquet,
        address=user_data['address'],
        delivery_time=user_data['delivery_time'],
        status="new"
    )

    # Подтверждение заказа
    await message.answer(
        f"✅ Ваш заказ оформлен!\n💐 Букет: {bouquet.name}\n📍 Адрес: {user_data['address']}\n"
        f"⏳ Дата и время: {user_data['delivery_time']}\n📞 Телефон: {message.text}"
    )

    await state.clear()  # Сбрасываем состояние