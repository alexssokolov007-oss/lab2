import pytest
from unittest.mock import Mock, patch, MagicMock
from src.rm import rm

class TestRm:
    def test_nonexistent_file(self):
        with patch('src.rm.os.path.exists') as mock_exists:
            mock_exists.return_value = False
            with pytest.raises(FileNotFoundError):
                rm('nonexistent.txt')

    def test_dir_without_recursive(self):
        with patch('src.rm.os.path.exists') as mock_exists, \
             patch('src.rm.os.path.isfile') as mock_isfile:
            mock_exists.return_value = True
            mock_isfile.return_value = False
            with pytest.raises(ValueError):
                rm('test_dir')

    def test_remove_file(self):
        with patch('src.rm.os.path.exists') as mock_exists, \
             patch('src.rm.os.path.isfile') as mock_isfile, \
             patch('src.rm.os.remove') as mock_remove, \
             patch('builtins.print') as mock_print:
            mock_exists.return_value = True
            mock_isfile.return_value = True
            result = rm('test_file.txt')
            assert result == 'Успешно'
            mock_remove.assert_called_once_with('test_file.txt')

    def test_recursive_delete(self):
        with patch('src.rm.os.path.exists') as mock_exists, \
             patch('src.rm.os.path.isfile') as mock_isfile, \
             patch('src.rm.shutil.rmtree') as mock_rmtree, \
             patch('builtins.input') as mock_input, \
             patch('builtins.print') as mock_print:
            mock_exists.return_value = True
            mock_isfile.return_value = False
            mock_input.return_value = 'y'
            result = rm('test_dir', recursive=True)
            assert result == 'Успешно'
            mock_rmtree.assert_called_once_with('test_dir')

    def test_cancel_delete(self):
        with patch('src.rm.os.path.exists') as mock_exists, \
             patch('src.rm.os.path.isfile') as mock_isfile, \
             patch('builtins.input') as mock_input, \
             patch('builtins.print') as mock_print:
            mock_exists.return_value = True
            mock_isfile.return_value = False
            mock_input.return_value = 'n'
            result = rm('test_dir', recursive=True)
            assert result == 'Отменено'

    def test_empty_dir(self):
        with patch('src.rm.os.path.exists') as mock_exists, \
             patch('src.rm.os.path.isfile') as mock_isfile, \
             patch('src.rm.shutil.rmtree') as mock_rmtree, \
             patch('builtins.input') as mock_input, \
             patch('builtins.print') as mock_print:
            mock_exists.return_value = True
            mock_isfile.return_value = False
            mock_input.return_value = 'y'
            result = rm('empty_dir', recursive=True)
            assert result == 'Успешно'
            mock_rmtree.assert_called_once_with('empty_dir')

    def test_multiple_files(self):
        with patch('src.rm.os.path.exists') as mock_exists, \
             patch('src.rm.os.path.isfile') as mock_isfile, \
             patch('src.rm.os.remove') as mock_remove, \
             patch('builtins.print') as mock_print:
            mock_exists.return_value = True
            mock_isfile.return_value = True
            rm('file1.txt')
            rm('file2.txt')
            assert mock_remove.call_count == 2
            mock_remove.assert_any_call('file1.txt')
            mock_remove.assert_any_call('file2.txt')

    def test_system_dirs(self):
        with patch('src.rm.os.path.exists') as mock_exists, \
             patch('src.rm.os.path.isfile') as mock_isfile:
            mock_exists.return_value = True
            mock_isfile.return_value = False
            with pytest.raises(ValueError):
                rm('/')
            with pytest.raises(ValueError):
                rm('/home/user')
