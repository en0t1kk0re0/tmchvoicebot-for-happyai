import os
from tempfile import NamedTemporaryFile

def save_audio_data_to_file(audio_data: bytes, suffix: str = ".ogg") -> str:
    """Сохраняет бинарные данные в файл и возвращает путь к файлу"""
    with NamedTemporaryFile(delete=False, suffix=suffix) as temp_audio:
        temp_audio.write(audio_data)
        return temp_audio.name

def remove_file(file_path: str):
    """Удаляет файл после использования"""
    try:
        os.remove(file_path)
    except OSError as e:
        print(f"Ошибка удаления файла {file_path}: {e}")
