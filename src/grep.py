import re
from pathlib import Path
from src.errors import validate_path_exists


def grep(pattern: str, search_path: str, recursive: bool = False, 
         ignore_case: bool = False, re_module=re, open_func=open, print_func=print) -> str:
    '''Ищет строки по шаблону в файлах'''
    path_obj = Path(search_path)
    validate_path_exists(path_obj)

    flags = re_module.IGNORECASE if ignore_case else 0
    regex = re_module.compile(pattern, flags)
    found_matches = False

    def search_in_file(file_path):
        nonlocal found_matches
        try:
            with open_func(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                for line_num, line in enumerate(file, 1):
                    if regex.search(line):
                        found_matches = True
                        print_func(f'{file_path}:{line_num}: {line.strip()}')
        except (UnicodeDecodeError, PermissionError):
            pass

    if path_obj.is_file():
        search_in_file(path_obj)
    elif path_obj.is_dir():
        files = path_obj.rglob('*') if recursive else path_obj.iterdir()
        for file_item in files:
            if file_item.is_file():
                search_in_file(file_item)

    if not found_matches:
        print_func('Совпадений не найдено')

    return 'Успешно'