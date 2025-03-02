import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from utils import remove_file
from openaiclient import process_voice_message, get_assistant_response, generate_voice_response
from config import settings
from aiogram.types import FSInputFile
from openaiclient import validate_value, save_value

TELEGRAM_BOT_TOKEN=settings.TELEGRAM_BOT_TOKEN
# Инициализация бота
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
import os

print("BOT_TOKEN из окружения:", os.getenv("TELEGRAM_BOT_TOKEN"))

# Обработчик голосового сообщения
@dp.message(F.voice)
async def handle_voice_message(message: Message):
    try:
        # Получаем голосовое сообщение
        file = await bot.get_file(message.voice.file_id)
        file_path = f"voice_{message.voice.file_id}.ogg"
        download_path = f"./{file_path}"
        await bot.download_file(file.file_path, download_path)
        print(f"File ID: {message.voice.file_id}")
        print(f"File Path: {file.file_path}")

        print(1)
        if not os.path.exists(file_path):
            await message.answer(f"Ошибка: файл {file_path} не найден!")
        # Обрабатываем голосовое сообщение и получаем текст
        user_text, _ = await process_voice_message(file_path)
        print(2)
        # Получаем ответ ассистента
        assistant_response = await get_assistant_response(user_text, settings.ASSISTANT_ID)
        print(3)
        # Генерируем голосовой ответ от ассистента
        voice_file_path = await generate_voice_response(assistant_response)
        print(4)
        # Проверка, является ли ответ ценностью
        if await validate_value(assistant_response):
            # Сохраняем ценность в базу данных
            await save_value(message.from_user.id, assistant_response)
            await message.answer("✅ Ценность сохранена!")
        else:
            await message.answer("⚠️ Ценность не прошла проверку. Попробуйте еще раз.")
        # Отправляем голосовой ответ пользователю
        voice_file = FSInputFile(voice_file_path)
        await message.answer_voice(voice=voice_file)

        # Удаляем временные файлы
        remove_file(file_path)
        remove_file(voice_file_path)

    except Exception as e:
        await message.answer(f"⚠️ Ошибка: {str(e)}")

# Основная функция для запуска бота
async def main():
    print("🤖 Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Ошибка при запуске: {e}")
