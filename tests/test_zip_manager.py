python
import os
import zipfile
import tempfile
import shutil
from main import create_zip, add_to_zip, remove_from_zip, extract_zip, list_zip

class TestZipManager:
    def setup_method(self):
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)

        self.create_test_files()
    
    def teardown_method(self):
        os.chdir(self.original_dir)
        shutil.rmtree(self.test_dir)
    
    def create_test_files(self):
        with open("test1.txt", "w") as f:
            f.write("тестовый файл 1")
        with open("test2.txt", "w") as f:
            f.write("тестовый файл 2")
        with open("test3.txt", "w") as f:
            f.write("тестовый файл 3")
    
    def test_create_zip_basic(self):
        print("Создание архива")
        result = create_zip("test_archive.zip", ["test1.txt", "test2.txt"])
        assert result == True
        assert os.path.exists("test_archive.zip")
        print("Архив успешно создан")
    
    def test_create_zip_nonexistent_file(self):
        print("Создание архива с несуществующим файлом")
        result = create_zip("test_archive.zip", ["nonexistent.txt"])
        assert result == False
        print("Корректно обработана ошибка несуществующего файла")
    
    def test_create_zip_no_files(self):
        print("Создание архива без файлов")
        result = create_zip("test_archive.zip", [])
        assert result == False
        print("Корректно обработана ошибка отсутствия файлов")
    
    def test_add_to_zip(self):
        print("Добавление файлов в архив")
        create_zip("test_archive.zip", ["test1.txt"])

        result = add_to_zip("test_archive.zip", ["test2.txt"])
        assert result == True

        with zipfile.ZipFile("test_archive.zip", 'r') as zipf:
            files = zipf.namelist()
            assert "test1.txt" in files
            assert "test2.txt" in files
        print("Файлы успешно добавлены в архив")
    
    def test_add_to_nonexistent_zip(self):
        print("Добавление в несуществующий архив")
        result = add_to_zip("nonexistent.zip", ["test1.txt"])
        assert result == False
        print("Корректно обработана ошибка несуществующего архива")
    
    def test_remove_from_zip(self):
        print("Удаление файла из архива")
        create_zip("test_archive.zip", ["test1.txt", "test2.txt"])
        
        result = remove_from_zip("test_archive.zip", "test1.txt")
        assert result == True

        with zipfile.ZipFile("test_archive.zip", 'r') as zipf:
            files = zipf.namelist()
            assert "test1.txt" not in files
            assert "test2.txt" in files
        print("Файл успешно удален из архива")
    
    def test_remove_nonexistent_file(self):
        print("Удаление несуществующего файла")
        create_zip("test_archive.zip", ["test1.txt"])
        
        result = remove_from_zip("test_archive.zip", "nonexistent.txt")
        assert result == False
        print("Корректно обработана ошибка несуществующего файла в архиве")
    
    def test_extract_zip(self):
        print("Распаковка архива")
        create_zip("test_archive.zip", ["test1.txt", "test2.txt"])
        
        result = extract_zip("test_archive.zip")
        assert result == True

        extract_folder = "test_archive_extracted"
        assert os.path.exists(extract_folder)
        assert os.path.exists(os.path.join(extract_folder, "test1.txt"))
        assert os.path.exists(os.path.join(extract_folder, "test2.txt"))
        print("Архив успешно распакован")
    
    def test_extract_nonexistent_zip(self):
        print("Распаковка несуществующего архива")
        result = extract_zip("nonexistent.zip")
        assert result == False
        print("Корректно обработана ошибка несуществующего архива")
    
    def test_list_zip(self):
        print("Просмотр содержимого архива")
        create_zip("test_archive.zip", ["test1.txt", "test2.txt"])
        
        result = list_zip("test_archive.zip")
        assert result == True
        print("Содержимое архива успешно показано")
    
    def test_list_nonexistent_zip(self):
        print("Просмотр несуществующего архива")
        result = list_zip("nonexistent.zip")
        assert result == False
        print("Корректно обработана ошибка несуществующего архива")
    
    def test_list_empty_zip(self):
        print("Просмотр пустого архива")
        with zipfile.ZipFile("empty.zip", 'w'):
            pass
        
        result = list_zip("empty.zip")
        assert result == True
        print("Корректно обработан пустой архив")

def run_all_tests():
    print("Запуск тестов ZIP менеджера")
    print("=" * 50)
    
    test_class = TestZipManager()

    test_methods = [method for method in dir(test_class) 
                   if method.startswith('test_')]
    
    passed = 0
    failed = 0
    
    for method_name in test_methods:
        try:
            test_class.setup_method()
            method = getattr(test_class, method_name)
            method()
            print(f"{method_name} - ПРОЙДЕН")
            passed += 1
        except Exception as e:
            print(f"{method_name} - ОШИБКА: {e}")
            failed += 1
        finally:
            test_class.teardown_method()
    
    print("=" * 50)
    print(f"Результаты: {passed} пройдено, {failed} не пройдено")
    
    if failed == 0:
        print("Все тесты успешно пройдены")
    else:
        print("Некоторые тесты не пройдены")

if __name__ == "__main__":
    run_all_tests()
