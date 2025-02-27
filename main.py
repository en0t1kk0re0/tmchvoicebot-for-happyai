import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from utils import save_audio_data_to_file, get_fs_input_file, remove_file
from openaiclient import process_voice_message, get_assistant_response, generate_voice_response
from config import settings


bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage()) 

@dp.message(F.voice)
async def handle_voice_message(message: Message):
    try:
        # Шаг 1: Голос -> Текст
        file = await bot.get_file(message.voice.file_id)
        file_path = f"voice_{message.voice.file_id}.ogg"
        await bot.download_file(file.file_path, file_path)

        user_text = await process_voice_message(file_path)

        # Шаг 2: Получение ответа от ассистента
        assistant_response = await get_assistant_response(user_text, settings.ASSISTANT_ID)

        # Шаг 3: Текст -> Голос
        audio_data = await generate_voice_response(assistant_response)

        # Шаг 4: Сохранение и отправка голосового ответа
        temp_audio_path = save_audio_data_to_file(audio_data)
        voice_file = get_fs_input_file(temp_audio_path)
        await message.answer_voice(voice=voice_file)

        # Удаляем временные файлы
        remove_file(file_path)
        remove_file(temp_audio_path)

    except Exception as e:
        await message.answer(f"⚠️ Ошибка: {str(e)}")

async def main():
    print("🤖 Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Ошибка при запуске: {e}")
