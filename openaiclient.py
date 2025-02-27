import asyncio
from openai import AsyncOpenAI
from config import settings


client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def get_assistant_response(prompt: str, assistant_id: str) -> str:
    """Получение ответа через Assistant API"""
    thread = await client.beta.threads.create()
    
    await client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=prompt
    )
    
    run = await client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistant_id
    )
    
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

async def process_voice_message(file_path: str) -> str:
    """Обработка голосового сообщения через Whisper"""
    with open(file_path, "rb") as audio_file:
        transcript = await client.audio.transcriptions.create(
            file=audio_file,
            model="whisper-1"
        )
    return transcript.text
