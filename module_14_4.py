import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, Router
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile, Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from crud_functions import get_all_products

all_media_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media')
start_router: Router = Router()
# Запуск бота
async def main():
    bot = Bot(token='??????????????????????????????????')
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(start_router)
    # Запускаем бота и пропускаем все накопленные входящие
    # Да, этот метод можно вызвать даже если у вас поллинг
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

start_kb = ReplyKeyboardMarkup(
    keyboard = [
        [
        KeyboardButton(text = "Рассчитать"),
        KeyboardButton(text = "Информация"),
        KeyboardButton(text = "Купить")
        ]
    ], resize_keyboard=True
)

inline_kb = InlineKeyboardMarkup(
    inline_keyboard = [
        [InlineKeyboardButton(text = "Формулы расчёта", callback_data = "formulas")],
        [InlineKeyboardButton(text = "Рассчитать норму калорий", callback_data =  "calories")]
    ]
)

buy_kb = InlineKeyboardMarkup(
    inline_keyboard = [
        [InlineKeyboardButton(text = "Product_1", callback_data = "product_buying")],
        [InlineKeyboardButton(text = "Product_2", callback_data = "product_buying")],
        [InlineKeyboardButton(text = "Product_3", callback_data = "product_buying")],
        [InlineKeyboardButton(text = "Product_4", callback_data = "product_buying")]
    ]
)


@start_router.message(F.text == 'Купить')
async def get_buying_list(message):
    await message.answer('У вас есть возможность приобрести следующие товары:')
    all_product = get_all_products()
    for i in range(len(all_product)):    #Вынимаем из BD характеристики товаров, и соответствующие "фото"
        await message.answer(f'Название: {all_product[i][1]} | Описание: {all_product[i][2]} | Цена'
                             f':{all_product[i][3]}')
        file_name = f'{all_product[i][4]}'
        photo_file = FSInputFile(path=os.path.join(all_media_dir, f'{file_name}'))
        msg_id = await message.answer_photo(photo=photo_file)
        print(msg_id.photo[-1].file_id)
    await message.answer(text='Выберите продукт для покупки: ', reply_markup=buy_kb)


@start_router.callback_query(F.data == 'product_buying')
async def start_router_(call: CallbackQuery):
    await call.message.answer(text='Вы успешно приобрели продукт!')


@start_router.message(CommandStart())  # перехватывает команды после "/" в данном случае "/start"
async def cmd_start(message: Message):
    await message.answer("Привет! Я бот помогающий твоему здоровью.", reply_markup = start_kb)

@start_router.message(F.text == "Рассчитать") # перехватывает текстовое сообщение
async def start_router_process(message: Message):
    await message.answer("Выберите опцию:", reply_markup = inline_kb)

@start_router.message(F.text == "Информация") # перехватывает текстовое сообщение
async def start_router_process(message: Message):
    await message.answer("Этот БОТ написан Alexandr62reg \n"
                         "31 января 2025 года", reply_markup = inline_kb)


@start_router.callback_query(F.data == "formulas")
async def start_router_process(call: CallbackQuery):
    await call.message.answer(
        "Упрощенный вариант формулы Миффлина-Сан Жеора: \n"
        "для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5;\n"
        "для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161. "
                         )

@start_router.callback_query(F.data == "calories")
async def start_router_process(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Введите свой возраст")
    await state.set_state(UserState.age)

@start_router.message(F.text, UserState.age)
async def start_router_process(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост")
    await state.set_state(UserState.growth)

@start_router.message(F.text, UserState.growth)
async def start_router_process(message: Message, state: FSMContext):
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес")
    await state.set_state(UserState.weight)

@start_router.message(F.text, UserState.weight)
async def start_router_process(message: Message, state: FSMContext):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    result = (10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5)
    result1 = (10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) - 161)
    await message.answer(f'Ваша норма калорий: {result} ккал в сутки (для мужчин)\n'
                         f'Ваша норма калорий: {result1} ккал в сутки (для женщин)')
    await state.clear()



if __name__ == "__main__":
    asyncio.run(main())
