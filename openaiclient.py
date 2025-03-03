import asyncio
from openai import AsyncOpenAI
from config import settings
from utils import save_audio_data_to_file
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import UserValue
from database import get_db
import json


client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def get_assistant_response(prompt: str, assistant_id: str) -> str:
    """Получение ответа через Assistant API"""
    try:
        # Создаем новый thread
        thread = await client.beta.threads.create()

        # Отправляем сообщение пользователем в этот thread
        await client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=prompt  # Передаем текстовое содержимое
        )

        # Запускаем и проверяем процесс выполнения
        run = await client.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id=assistant_id
        )

        if run.status != "completed" and run.status != "requires_action":
            raise Exception(f"Ошибка выполнения: {run.status}")

        # Получаем список сообщений из потока
        messages = await client.beta.threads.messages.list(thread_id=thread.id)

        # Проверка, есть ли сообщения
        if messages.data:
            # Проверяем, что первый элемент содержит content и извлекаем текст
            content = messages.data[0].content
            if content and isinstance(content, list) and len(content) > 0:
                text_block = content[0]
                if text_block and hasattr(text_block, 'text') and hasattr(text_block.text, 'value'):
                    return text_block.text.value
                else:
                    raise Exception("Невозможно извлечь текст из блока.")
            else:
                raise Exception("Ответ от ассистента не содержит текст.")
        else:
            raise Exception("Ответ от ассистента не получен.")
    
    except Exception as e:
        # Логируем ошибку и возвращаем сообщение об ошибке
        print(f"Ошибка при получении ответа от ассистента: {e}")
        raise Exception(f"Ошибка при получении ответа от ассистента: {e}")
    

async def save_value(user_id: int, value: str):
    """Сохраняет ценность пользователя в БД"""
    async for session in get_db():
        new_value = UserValue(user_id=user_id, value=value)
        session.add(new_value)
        await session.commit()
        return new_value


async def validate_value(value: str) -> bool:
    """Проверяет, является ли ценность адекватной"""
    response = await client.chat.completions.create(
        model="gpt-4-turbo",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "Ты — помощник, который возвращает JSON. Всегда отвечай строго в формате JSON."},
            {"role": "user", "content": f"Определи, корректна ли ценность пользователя: {value}. Ответ должен быть JSON."}
        ],
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "validate",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "is_valid": {"type": "boolean"}
                        },
                        "required": ["is_valid"]
                    }
                }
            }
        ],
        tool_choice="auto"
    )

    if response.choices[0].message.tool_calls:
        arguments_str = response.choices[0].message.tool_calls[0].function.arguments
        arguments = json.loads(arguments_str)  # Преобразуем строку в JSON-объект

        return arguments["is_valid"]
    
    raise ValueError("OpenAI API не вызвал функцию 'validate'. Проверьте запрос.")



async def generate_voice_response(text: str) -> bytes:
    """Генерация голосового ответа через TTS"""
    response = await client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=text
    )
    print("Response:", response)
    audio_data = response.read()
    return save_audio_data_to_file(audio_data)

async def process_voice_message(file_path: str) -> tuple[str, str]:
    """Обработка голосового сообщения через Whisper"""
    with open(file_path, "rb") as audio_file:
        transcript = await client.audio.transcriptions.create(
            file=audio_file,
            model="whisper-1"
        )
    return transcript.text, file_path 