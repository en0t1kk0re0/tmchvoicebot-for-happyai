import os
from tempfile import NamedTemporaryFile
from aiogram.types import FSInputFile

def save_audio_data_to_file(audio_data: bytes, suffix: str = ".ogg") -> str:
    """Сохраняет бинарные данные в файл и возвращает путь к файлу"""
    with NamedTemporaryFile(delete=False, suffix=suffix) as temp_audio:
        temp_audio.write(audio_data)
        return temp_audio.name

def get_fs_input_file(file_path: str) -> FSInputFile:
    """Возвращает FSInputFile для отправки через aiogram"""
    return FSInputFile(file_path)

def remove_file(file_path: str):
    """Удаляет файл после использования"""
    try:
        os.remove(file_path)
    except OSError as e:
        print(f"Ошибка удаления файла {file_path}: {e}")
