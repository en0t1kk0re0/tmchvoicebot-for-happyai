from openai import AsyncOpenAI
from config import settings

# Создание клиента OpenAI
client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def create_assistant():
    # Создаем ассистента с функцией
    assistant = await client.beta.assistants.create(
        name="Value Identifier",
        instructions="Определи ключевые ценности пользователя и сохрани их в БД.",
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "save_value",
                    "description": "Сохраняет ценность пользователя",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "integer"},
                            "value": {"type": "string"}
                        },
                        "required": ["user_id", "value"]
                    }
                }
            }
        ],
        model="gpt-4-turbo"
    )

    # Вернем id ассистента, чтобы убедиться, что он был создан
    return assistant.id

# Запуск асинхронной функции
import asyncio
assistant_id = asyncio.run(create_assistant())
print(f"Assistant ID: {assistant_id}")
