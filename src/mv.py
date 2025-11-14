import shutil
from pathlib import Path
from src.errors import validate_path_exists, validate_not_self_copy


def mv(source: str, destination: str, shutil_module=shutil, print_func=print) -> str:
    '''Перемещает или переименовывает файл/директорию'''
    src_path = Path(source)
    dst_path = Path(destination)
    validate_path_exists(src_path)

    if src_path.is_dir():
        validate_not_self_copy(src_path, dst_path)

    if dst_path.exists() and dst_path.is_dir():
        dst_path = dst_path / src_path.name

    shutil_module.move(str(src_path), str(dst_path))
    print_func('Успешно')
    return 'Успешно'