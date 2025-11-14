import pytest
from unittest.mock import Mock, patch
from src.cat import cat


def test_nonexistent_file():
    with patch('src.cat.validate_path_exists') as mock_validate:
        mock_validate.side_effect = FileNotFoundError("Не существует")
        with pytest.raises(FileNotFoundError):
            cat('nonexisting.txt')


def test_directory_instead_file():
    with patch('src.cat.validate_path_exists'):
        with patch('src.cat.validate_is_file') as mock_validate_file:
            mock_validate_file.side_effect = IsADirectoryError("Не файл")
            with pytest.raises(IsADirectoryError):
                cat('test_dir')


def test_file_content():
    with patch('src.cat.validate_path_exists'):
        with patch('src.cat.validate_is_file'):
            with patch('src.cat.Path') as mock_path:
                with patch('builtins.print') as mock_print:
                    mock_file = Mock()
                    mock_file.stat.return_value.st_size = 100
                    mock_file.read_text.return_value = 'hello\nworld'
                    
                    mock_path.return_value = mock_file
                    
                    result = cat('test.txt')
                    
                    assert result == 'Успешно'
                    mock_print.assert_called_once_with('hello\nworld')


def test_large_file():
    with patch('src.cat.validate_path_exists'):
        with patch('src.cat.validate_is_file'):
            with patch('src.cat.Path') as mock_path:
                mock_file = Mock()
                mock_file.stat.return_value.st_size = 11 * 1024 * 1024  # 11MB
                
                mock_path.return_value = mock_file
                
                with pytest.raises(ValueError, match='Файл слишком большой'):
                    cat('large.txt')


def test_empty_file():
    with patch('src.cat.validate_path_exists'):
        with patch('src.cat.validate_is_file'):
            with patch('src.cat.Path') as mock_path:
                with patch('builtins.print') as mock_print:
                    mock_file = Mock()
                    mock_file.stat.return_value.st_size = 0
                    mock_file.read_text.return_value = ''
                    
                    mock_path.return_value = mock_file
                    
                    result = cat('empty.txt')
                    
                    assert result == 'Успешно'
                    mock_print.assert_called_once_with('')
