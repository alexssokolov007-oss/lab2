import pytest
from unittest.mock import Mock, patch
from src.ls import ls, format_size, get_permissions


def test_format_size():
    """Форматирование размеров файлов в читабельный вид"""
    assert format_size(500) == '500.0B'
    assert format_size(1024) == '1.0K'
    assert format_size(1536) == '1.5K'
    assert format_size(1048576) == '1.0M'


def test_get_permissions():
    """Преобразование числовых режимов доступа в строковый формат"""
    dir_mode = 0o40755
    assert get_permissions(dir_mode) == 'drwxr-xr-x'

    file_mode = 0o100644
    assert get_permissions(file_mode) == '-rw-r--r--'

    link_mode = 0o120755
    assert get_permissions(link_mode) == 'lrwxr-xr-x'


def test_nonexistent_dir():
    """Попытка просмотра несуществующей директории"""
    with patch('src.ls.validate_path_exists') as mock_validate:
        mock_validate.side_effect = FileNotFoundError("Не существует")
        with pytest.raises(FileNotFoundError):
            ls('nonexistent_dir')


def test_current_dir():
    """Вывод содержимого текущей директории"""
    mock_print = Mock()
    
    with patch('src.ls.validate_path_exists'):
        with patch('src.ls.Path') as mock_path:
            file1 = Mock()
            file1.name = 'file1.txt'
            file1.is_dir.return_value = False
            file1.stat.return_value.st_size = 100
            file1.stat.return_value.st_mtime = 1609459200
            file1.stat.return_value.st_mode = 0o100644
            
            file2 = Mock()
            file2.name = 'file2.txt'
            file2.is_dir.return_value = False
            file2.stat.return_value.st_size = 200
            file2.stat.return_value.st_mtime = 1609459200
            file2.stat.return_value.st_mode = 0o100644
            
            subdir = Mock()
            subdir.name = 'subdir'
            subdir.is_dir.return_value = True
            subdir.stat.return_value.st_size = 4096
            subdir.stat.return_value.st_mtime = 1609459200
            subdir.stat.return_value.st_mode = 0o40755
            
            mock_folder = Mock()
            mock_folder.exists.return_value = True
            mock_folder.iterdir.return_value = [file1, file2, subdir]
            
            mock_path.return_value = mock_folder
            
            result = ls(print_func=mock_print)
            
            assert result == 'Успешно'
            assert mock_print.call_count == 3