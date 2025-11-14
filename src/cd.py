import os
from pathlib import Path
from src.errors import validate_path_exists, validate_is_directory


def cd(path: str = None, os_module=os) -> str:
    '''Изменяет текущую рабочую директорию'''
    if not path or path == '~':
        new_path = Path.home()
    elif path == '..':
        new_path = Path.cwd().parent
    else:
        new_path = Path(path).expanduser().resolve()
        validate_path_exists(new_path)
        validate_is_directory(new_path)

    os_module.chdir(new_path)
    return 'Успешно'