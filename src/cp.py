import shutil
from pathlib import Path
from src.errors import validate_path_exists, validate_not_self_copy


def cp(source: str, destination: str, recursive: bool = False, 
       shutil_module=shutil, print_func=print) -> str:
    '''Копирует файл или директорию'''
    src_path = Path(source)
    dst_path = Path(destination)
    validate_path_exists(src_path)

    if src_path.is_dir():
        if not recursive:
            raise NotADirectoryError('Для копирования директорий используйте флаг -r')

        validate_not_self_copy(src_path, dst_path)
        shutil_module.copytree(src_path, dst_path)
    else:
        shutil_module.copy2(src_path, dst_path)

    print_func('Успешно')
    return 'Успешно'