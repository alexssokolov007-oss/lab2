python
import os
import zipfile

def show_help():
    print("=== Простой ZIP менеджер ===")
    print("Команды:")
    print("  create <архив> <файл1> <файл2> ... - создать архив")
    print("  add <архив> <файл1> <файл2> ... - добавить в архив")
    print("  remove <архив> <файл> - удалить из архива")
    print("  extract <архив> - распаковать архив")
    print("  list <архив> - посмотреть что в архиве")
    print("  help - показать справку")
    print("  exit - выход")
    print()

def create_zip(archive_name, files):
    """Создает новый ZIP архив с файлами"""
    if not files:
        print("Ошибка: не указаны файлы для архива")
        return False

    for file in files:
        if not os.path.exists(file):
            print(f"Ошибка: файл {file} не найден")
            return False

    try:
        with zipfile.ZipFile(archive_name, 'w') as zipf:
            for file in files:
                zipf.write(file)
                print(f"Добавлен: {file}")
        print(f"Архив {archive_name} успешно создан!")
        return True
    except Exception as e:
        print(f"Ошибка при создании архива: {e}")
        return False

def add_to_zip(archive_name, files):
    """Добавляет файлы в существующий архив"""
    if not os.path.exists(archive_name):
        print("Ошибка: архив не найден")
        return False
        
    if not files:
        print("Ошибка: не указаны файлы для добавления")
        return False
    
    for file in files:
        if not os.path.exists(file):
            print(f"Ошибка: файл {file} не найден")
            return False
    
    try:
        temp_name = "temp_" + archive_name

        with zipfile.ZipFile(archive_name, 'r') as old_zip:
            with zipfile.ZipFile(temp_name, 'w') as new_zip:
                for item in old_zip.namelist():
                    new_zip.writestr(item, old_zip.read(item))

                for file in files:
                    new_zip.write(file)
                    print(f"Добавлен: {file}")

        os.remove(archive_name)
        os.rename(temp_name, archive_name)
        print("Файлы успешно добавлены в архив!")
        return True
        
    except Exception as e:
        print(f"Ошибка при добавлении файлов: {e}")
        if os.path.exists(temp_name):
            os.remove(temp_name)
        return False

def remove_from_zip(archive_name, file_to_remove):
    if not os.path.exists(archive_name):
        print("Ошибка: архив не найден")
        return False
    
    if not file_to_remove:
        print("Ошибка: не указан файл для удаления")
        return False
    
    try:
        temp_name = "temp_" + archive_name
        file_found = False
        
        with zipfile.ZipFile(archive_name, 'r') as old_zip:
            with zipfile.ZipFile(temp_name, 'w') as new_zip:
                for item in old_zip.namelist():
                    if item != file_to_remove:
                        new_zip.writestr(item, old_zip.read(item))
                    else:
                        file_found = True
                        print(f"Удален: {file_to_remove}")
        
        if file_found:
            os.remove(archive_name)
            os.rename(temp_name, archive_name)
            print("Файл успешно удален из архива!")
            return True
        else:
            os.remove(temp_name)
            print(f"Ошибка: файл {file_to_remove} не найден в архиве")
            return False
            
    except Exception as e:
        print(f"Ошибка при удалении файла: {e}")
        if os.path.exists(temp_name):
            os.remove(temp_name)
        return False

def extract_zip(archive_name):
    """Распаковывает архив"""
    if not os.path.exists(archive_name):
        print("Ошибка: архив не найден")
        return False
    
    try:
        folder_name = archive_name.replace('.zip', '') + "_extracted"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        
        with zipfile.ZipFile(archive_name, 'r') as zipf:
            zipf.extractall(folder_name)
            files = zipf.namelist()
        
        print(f"Архив распакован в папку: {folder_name}")
        print(f"Извлечено файлов: {len(files)}")
        return True
        
    except Exception as e:
        print(f"Ошибка при распаковке: {e}")
        return False

def list_zip(archive_name):
    """Показывает содержимое архива"""
    if not os.path.exists(archive_name):
        print("Ошибка: архив не найден")
        return False
    
    try:
        with zipfile.ZipFile(archive_name, 'r') as zipf:
            files = zipf.namelist()
            
            if not files:
                print("Архив пуст")
                return True
            
            print(f"Содержимое архива {archive_name}:")
            print("-" * 40)
            for i, filename in enumerate(files, 1):
                file_info = zipf.getinfo(filename)
                print(f"{i:2d}. {filename}")
                print(f"     Размер: {file_info.file_size} байт")
            print("-" * 40)
            print(f"Всего файлов: {len(files)}")
            return True
            
    except Exception as e:
        print(f"Ошибка при чтении архива: {e}")
        return False

def main():
    print("Добро пожаловать в простой ZIP менеджер!")
    show_help()
    
    while True:
        try:
            user_input = input("> ").strip()
            if not user_input:
                continue
                
            parts = user_input.split()
            command = parts[0].lower()
            
            if command == "exit":
                print("До свидания!")
                break
                
            elif command == "help":
                show_help()
                
            elif command == "create":
                if len(parts) >= 3:
                    create_zip(parts[1], parts[2:])
                else:
                    print("Использование: create <архив> <файл1> <файл2> ...")
                    
            elif command == "add":
                if len(parts) >= 3:
                    add_to_zip(parts[1], parts[2:])
                else:
                    print("Использование: add <архив> <файл1> <файл2> ...")
                    
            elif command == "remove":
                if len(parts) >= 3:
                    remove_from_zip(parts[1], parts[2])
                else:
                    print("Использование: remove <архив> <файл>")
                    
            elif command == "extract":
                if len(parts) >= 2:
                    extract_zip(parts[1])
                else:
                    print("Использование: extract <архив>")
                    
            elif command == "list":
                if len(parts) >= 2:
                    list_zip(parts[1])
                else:
                    print("Использование: list <архив>")
                    
            else:
                print("Неизвестная команда. Напишите 'help' для справки.")
                
        except KeyboardInterrupt:
            print("\nВыход из программы...")
            break
        except Exception as e:
            print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()
