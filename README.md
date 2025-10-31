# Лабораторная работа №2 (М1)

Программа для работы с ZIP архивами на Python.

## Команды программы
create archive.zip file1.txt file2.jpg - создать архив

add archive.zip newfile.pdf - добавить файл в архив

remove archive.zip file.txt - удалить файл из архива

extract archive.zip - распаковать архив

list archive.zip - посмотреть что в архиве

help - показать справку

exit - выйти из программы

## Установка и запуск
git clone https://github.com/alexssokolov007-oss/lab2 cd lab2

python -m venv .venv source .venv/bin/activate or for W .venv\Scripts\activate

pip install -r requirements.txt

python main.py

/for tests: python test_zip_manager.py

## Структура проекта
├── src  
│ ├── init.py  
│ ├── untils.py  
│ └── main.py  
│  
├── tests  
│ ├── init.py  
│ └── test_zip_manager.py  
│  
├── .gitignore  
├── .pre-commit-config.yaml  
├── README.md  
├── pyproject.toml  
└── requirements.txt  
