print("скрипт запущен")
import os
import asyncio
from tempfile import NamedTemporaryFile
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, FSInputFile
from aiogram.fsm.storage.memory import MemoryStorage
from openai import AsyncOpenAI
from dotenv import dotenv_values

env_vars = dotenv_values(".env")  # Загружаем вручную

# Загружаем .env перед инициализацией настроек
load_dotenv()

# Конфигурация приложения
class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str
    OPENAI_API_KEY: str
    ASSISTANT_ID: str

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()
# Инициализация клиентов
bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())  # Указали хранилище FSM
client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def process_voice_message(message: Message) -> str:
    """Обработка голосового сообщения через Whisper"""
    voice = message.voice
    file = await bot.get_file(voice.file_id)
    ext = file.file_path.split('.')[-1]

    with NamedTemporaryFile(suffix=f".{ext}", delete=False) as tmp:
        await bot.download_file(file.file_path, tmp.name)
        temp_path = tmp.name  # Сохраняем путь перед закрытием файла

    try:
        with open(temp_path, "rb") as audio_file:
            transcript = await client.audio.transcriptions.create(
                file=audio_file,
                model="whisper-1"
            )
    finally:
        os.remove(temp_path)  # Удаляем файл после использования
    
    return transcript.text

async def get_assistant_response(prompt: str) -> str:
    """Получение ответа через Assistant API"""
    thread = await client.beta.threads.create()
    
    await client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=prompt
    )
    
    run = await client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=settings.ASSISTANT_ID
    )
    
    while True:
        run = await client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        if run.status == "completed":
            break
        await asyncio.sleep(1)
    
    messages = await client.beta.threads.messages.list(thread_id=thread.id)
    return messages.data[0].content[0].text.value

async def generate_voice_response(text: str) -> bytes:
    """Генерация голосового ответа через TTS"""
    response = await client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=text
    )
    return response.read()

async def send_voice_response(message: Message, audio_data: bytes):
    """Сохранение и отправка голосового ответа"""
    with NamedTemporaryFile(delete=False, suffix=".ogg") as temp_audio:
        temp_audio.write(audio_data)
        temp_audio_path = temp_audio.name

    try:
        voice_file = FSInputFile(temp_audio_path)
        await message.answer_voice(voice=voice_file)
    finally:
        os.remove(temp_audio_path)  # Удаляем файл после отправки

@dp.message(F.voice)
async def handle_voice_message(message: Message):
    try:
        # Шаг 1: Голос -> Текст
        user_text = await process_voice_message(message)
        
        # Шаг 2: Получение ответа от ассистента
        assistant_response = await get_assistant_response(user_text)
        
        # Шаг 3: Текст -> Голос
        audio_data = await generate_voice_response(assistant_response)
        
        # Шаг 4: Отправка ответа
        await send_voice_response(message, audio_data)

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
