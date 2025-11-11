import pytest
from unittest.mock import Mock, patch, MagicMock
from src.cat import cat

class TestCat:
    def test_nonexistent_file(self):
        with patch('src.cat.os.path.exists') as mock_exists:
            mock_exists.return_value = False
            with pytest.raises(FileNotFoundError):
                cat('nonexisting.txt')
    
    def test_directory_instead_file(self):
        with patch('src.cat.os.path.exists') as mock_exists, \
             patch('src.cat.os.path.isfile') as mock_isfile:
            mock_exists.return_value = True
            mock_isfile.return_value = False
            with pytest.raises(IsADirectoryError):
                cat('test_dir')
    
    def test_file_content(self):
        with patch('src.cat.os.path.exists') as mock_exists, \
             patch('src.cat.os.path.isfile') as mock_isfile, \
             patch('src.cat.os.path.getsize') as mock_getsize, \
             patch('builtins.open') as mock_open, \
             patch('builtins.print') as mock_print:
            mock_exists.return_value = True
            mock_isfile.return_value = True
            mock_getsize.return_value = 100
            mock_file = MagicMock()
            mock_file.__enter__.return_value = mock_file
            mock_file.readlines.return_value = ['hello\n', 'world\n']
            mock_open.return_value = mock_file
            result = cat('test.txt')
            assert result == 'Успешно'
            mock_open.assert_called_once_with('test.txt', 'r', encoding='utf-8')
            assert mock_print.call_count == 2
            mock_print.assert_any_call('hello\n', end='')
            mock_print.assert_any_call('world\n', end='')
    
    def test_large_file(self):
        with patch('src.cat.os.path.exists') as mock_exists, \
             patch('src.cat.os.path.isfile') as mock_isfile, \
             patch('src.cat.os.path.getsize') as mock_getsize:
            mock_exists.return_value = True
            mock_isfile.return_value = True
            mock_getsize.return_value = 11 * 1024 * 1024 + 1
            with pytest.raises(ValueError):
                cat('large.txt')
    
    def test_empty_file(self):
        with patch('src.cat.os.path.exists') as mock_exists, \
             patch('src.cat.os.path.isfile') as mock_isfile, \
             patch('src.cat.os.path.getsize') as mock_getsize, \
             patch('builtins.open') as mock_open, \
             patch('builtins.print') as mock_print:
            mock_exists.return_value = True
            mock_isfile.return_value = True
            mock_getsize.return_value = 0
            mock_file = MagicMock()
            mock_file.__enter__.return_value = mock_file
            mock_file.readlines.return_value = []
            mock_open.return_value = mock_file
            result = cat('empty.txt')
            assert result == 'Успешно'
            mock_open.assert_called_once_with('empty.txt', 'r', encoding='utf-8')
            mock_print.assert_not_called()
    
    def test_special_chars(self):
        with patch('src.cat.os.path.exists') as mock_exists, \
             patch('src.cat.os.path.isfile') as mock_isfile, \
             patch('src.cat.os.path.getsize') as mock_getsize, \
             patch('builtins.open') as mock_open, \
             patch('builtins.print') as mock_print:
            mock_exists.return_value = True
            mock_isfile.return_value = True
            mock_getsize.return_value = 100
            mock_file = MagicMock()
            mock_file.__enter__.return_value = mock_file
            mock_file.readlines.return_value = ['свэг\n', '∞\n', '฿\n']
            mock_open.return_value = mock_file
            result = cat('special.txt')
            assert result == 'Успешно'
            assert mock_print.call_count == 3
            mock_print.assert_any_call('свэг\n', end='')
            mock_print.assert_any_call('∞\n', end='')
            mock_print.assert_any_call('฿\n', end='')
    
    def test_file_without_newline(self):
        with patch('src.cat.os.path.exists') as mock_exists, \
             patch('src.cat.os.path.isfile') as mock_isfile, \
             patch('src.cat.os.path.getsize') as mock_getsize, \
             patch('builtins.open') as mock_open, \
             patch('builtins.print') as mock_print:

            mock_exists.return_value = True
            mock_isfile.return_value = True
            mock_getsize.return_value = 50
            mock_file = MagicMock()
            mock_file.__enter__.return_value = mock_file
            mock_file.readlines.return_value = ['single line without newline']
            mock_open.return_value = mock_file
            result = cat('single_line.txt')
            assert result == 'Успешно'
            mock_print.assert_called_once_with('single line without newline', end='')
    
    def test_multiple_files(self):
        pass
