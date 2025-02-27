import asyncio
from openai import AsyncOpenAI

client = AsyncOpenAI(api_key="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")

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
