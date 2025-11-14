import pytest
from unittest.mock import Mock, patch
from src.errors import validate_path_exists, validate_is_file, validate_is_directory


class TestValidatePathExists:
    def test_path_exists(self):
        """Тест: путь существует"""
        with patch('src.errors.os.path.exists') as mock_exists:
            mock_exists.return_value = True
            
            # Не должно вызывать исключение
            validate_path_exists('/existing/path')
            mock_exists.assert_called_once_with('/existing/path')

    def test_path_not_exists(self):
        """Тест: путь не существует"""
        with patch('src.errors.os.path.exists') as mock_exists:
            mock_exists.return_value = False
            
            with pytest.raises(FileNotFoundError, match="не существует"):
                validate_path_exists('/nonexistent/path')


class TestValidateIsFile:
    def test_is_file(self):
        """Тест: путь является файлом"""
        with patch('src.errors.os.path.exists') as mock_exists:
            with patch('src.errors.os.path.isfile') as mock_isfile:
                mock_exists.return_value = True
                mock_isfile.return_value = True
                
                # Не должно вызывать исключение
                validate_is_file('/path/to/file')
                mock_exists.assert_called_once_with('/path/to/file')
                mock_isfile.assert_called_once_with('/path/to/file')

    def test_is_not_file(self):
        """Тест: путь не является файлом (директория)"""
        with patch('src.errors.os.path.exists') as mock_exists:
            with patch('src.errors.os.path.isfile') as mock_isfile:
                mock_exists.return_value = True
                mock_isfile.return_value = False
                
                with pytest.raises(IsADirectoryError, match="не является файлом"):
                    validate_is_file('/path/to/directory')

    def test_is_not_file_nonexistent(self):
        """Тест: путь не существует"""
        with patch('src.errors.os.path.exists') as mock_exists:
            mock_exists.return_value = False
            
            with pytest.raises(FileNotFoundError):
                validate_is_file('/nonexistent/path')


class TestValidateIsDirectory:
    def test_is_directory(self):
        """Тест: путь является директорией"""
        with patch('src.errors.os.path.exists') as mock_exists:
            with patch('src.errors.os.path.isdir') as mock_isdir:
                mock_exists.return_value = True
                mock_isdir.return_value = True
                
                # Не должно вызывать исключение
                validate_is_directory('/path/to/directory')
                mock_exists.assert_called_once_with('/path/to/directory')
                mock_isdir.assert_called_once_with('/path/to/directory')

    def test_is_not_directory(self):
        """Тест: путь не является директорией (файл)"""
        with patch('src.errors.os.path.exists') as mock_exists:
            with patch('src.errors.os.path.isdir') as mock_isdir:
                mock_exists.return_value = True
                mock_isdir.return_value = False
                
                with pytest.raises(NotADirectoryError, match="не является директорией"):
                    validate_is_directory('/path/to/file')

    def test_is_not_directory_nonexistent(self):
        """Тест: путь не существует"""
        with patch('src.errors.os.path.exists') as mock_exists:
            mock_exists.return_value = False
            
            with pytest.raises(FileNotFoundError):
                validate_is_directory('/nonexistent/path')


class TestValidateIntegration:
    def test_validate_file_complete(self):
        """Интеграционный тест: полная валидация файла"""
        with patch('src.errors.os.path.exists') as mock_exists:
            with patch('src.errors.os.path.isfile') as mock_isfile:
                mock_exists.return_value = True
                mock_isfile.return_value = True
                
                # Не должно вызывать исключений
                validate_path_exists('/some/file.txt')
                validate_is_file('/some/file.txt')
                
                assert mock_exists.call_count == 2
                mock_isfile.assert_called_once()

    def test_validate_directory_complete(self):
        """Интеграционный тест: полная валидация директории"""
        with patch('src.errors.os.path.exists') as mock_exists:
            with patch('src.errors.os.path.isdir') as mock_isdir:
                mock_exists.return_value = True
                mock_isdir.return_value = True
                
                # Не должно вызывать исключений
                validate_path_exists('/some/directory')
                validate_is_directory('/some/directory')
                
                assert mock_exists.call_count == 2
                mock_isdir.assert_called_once()
