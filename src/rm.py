from pathlib import Path
from src.errors import validate_path_exists
from src.constants import PROTECTED_DIRS
from src.history_manager import safe_remove


def rm(target: str, recursive: bool = False, input_func=input, 
       history_manager_module=None) -> str:
    '''Удаляет файл или директорию'''
    target_path = Path(target).expanduser().resolve()
    validate_path_exists(target_path)

    if target_path.resolve() in PROTECTED_DIRS:
        raise ValueError('Нельзя удалять системные директории')

    if target_path.is_dir():
        if not recursive:
            raise ValueError('Используйте -r для удаления директорий')

        while True:
            user_input = input_func(f'Удалить директорию "{target}" и всё её содержимое? (y/n): ').strip().lower()

            if user_input == 'y':
                break
            elif user_input == 'n':
                print('Отменено')
                return 'Отменено'
            else:
                print('Пожалуйста, введите "y" (да) или "n" (нет)')

        safe_remove_func = history_manager_module.safe_remove if history_manager_module else safe_remove
        safe_remove_func(target_path)
    else:
        safe_remove_func = history_manager_module.safe_remove if history_manager_module else safe_remove
        safe_remove_func(target_path)

    print('Успешно')
    return 'Успешно'