import os
from pathlib import Path

def validate_path_exists(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f'{path} не существует')

def validate_is_file(path):
    validate_path_exists(path)
    if not os.path.isfile(path):
        raise IsADirectoryError(f'{path} не является файлом')

def validate_is_directory(path):
    validate_path_exists(path)
    if not os.path.isdir(path):
        raise NotADirectoryError(f'{path} не является директорией')

def validate_not_self_copy(source, destination):
    source_path = Path(source).resolve()
    dest_path = Path(destination).resolve()
    
    if dest_path.is_relative_to(source_path):
        raise ValueError(f'Невозможно скопировать/переместить {source} в {destination} - целевой путь находится внутри исходного')
