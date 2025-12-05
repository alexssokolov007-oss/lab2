# Лабораторная работа №2

Мини-оболочка Shell на Python. Реализует базовые Unix-подобные команды (`ls`, `cd`, `cat`, `cp`, `mv`, `rm`), работу с архивами (`zip`, `unzip`, `tar`, `untar`), поиск по содержимому (`grep`), историю и откат (`history`, `undo`), а также безопасное удаление через корзину `.trash`.

## Возможности
- Просмотр файлов и директорий с опцией подробного вывода (`ls`, `ls -l`).
- Навигация по файловой системе, включая `..` и `~` (`cd`).
- Чтение файлов с ограничением размера 10 МБ (`cat`).
- Копирование/перемещение файлов и директорий с проверками (`cp`, `cp -r`, `mv`).
- Безопасное удаление и очистка корзины (`rm`, `rm -r`, `undo`, `clear_trash`).
- Создание и распаковка ZIP/TAR.GZ-архивов (`zip`, `unzip`, `tar`, `untar`).
- Поиск по содержимому с флагами `-r` и `-i` (`grep`).
- Ведение истории команд и откат изменений (`history`, `undo`).

## Структура проекта
```
lab2/
├── src/
│   ├── archive.py
│   ├── cat.py
│   ├── cd.py
│   ├── constants.py
│   ├── cp.py
│   ├── errors.py
│   ├── grep.py
│   ├── history_manager.py
│   ├── logsetup.py
│   ├── ls.py
│   ├── main.py
│   ├── mv.py
│   ├── rm.py
│   ├── shell.py
│   └── __init__.py
├── tests/                         # pytest-тесты на команды
├── uv.lock                        # lock-файл менеджера uv
├── pyproject.toml                 # конфигурация проекта
├── requirements.txt               # зависимости для pip
└── README.md
```

## Требования
- Python 3.12+
- pytest (для тестов)
- (опционально) [uv](https://docs.astral.sh/uv/) или стандартный `pip`

## Установка зависимостей
```bash
python -m venv .venv
. .venv/bin/activate              # PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt   # или `uv pip sync`
```

## Запуск Shell
```bash
python -m src.main
```

## Тесты
```bash
pytest
```

## История, корзина и логи
- Все успешные изменения (`cp`, `mv`, `rm`) фиксируются в `.history` (JSON).
- Удалённые файлы складываются в `.trash`, откуда их можно восстановить через `undo` или очистить `clear_trash`.
- Все команды и ошибки логируются в корневой `shell.log` (ротация по ~1 МБ, до 3 файлов) в формате `[дата-время] CMD: ... | RESULT/ERROR`.
