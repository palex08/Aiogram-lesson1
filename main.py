from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram import Router, F
import aiohttp
import asyncio
from config import TOKEN, w_api_key

# Создаем экземпляр бота и роутера
bot = Bot(token=TOKEN)
router = Router()  # Используем Router в aiogram 3.x
dp = Dispatcher()  # Создаем Dispatcher


# Функция для асинхронного получения прогноза погоды
async def get_weather(city: str = "Moscow") -> str:
    api_key = w_api_key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ru"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                temp = data["main"]["temp"]
                description = data["weather"][0]["description"]
                return f"Погода в {city}:\nТемпература: {temp}°C\nОписание: {description}"
            else:
                return "Не удалось получить прогноз погоды"


# Обработка команды /start
@router.message(F.text == "/start")
async def send_welcome(message: Message):
    await message.answer("Привет! Я погодный бот. Который показывает прогноз погоды в Москве.")
    await send_weather(message)


# Обработка команды /help
@router.message(F.text == "/help")
async def send_help(message: Message):
    await message.answer("Список команд:\n/start - Начать работу\n/weather - Узнать прогноз погоды в Москве")


# Обработка команды /weather
@router.message(F.text.startswith("/weather"))
async def send_weather(message: Message):
    city = "Moscow"

    weather_info = await get_weather(city)
    await message.answer(weather_info)


# Функция для запуска бота
async def main():
    # Включаем обработку сообщений через роутер
    dp.include_router(router)

    # Запускаем бот с использованием Dispatcher
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
