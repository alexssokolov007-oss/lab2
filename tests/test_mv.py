import pytest
from unittest.mock import Mock, patch
from src.mv import mv

class TestMv:
    def test_nonexistent_source(self):
        with patch('src.mv.os.path.exists') as mock_exists:
            mock_exists.return_value = False
            with pytest.raises(FileNotFoundError):
                mv('nonexistent.txt', 'new_location.txt')

    def test_rename_file(self):
        with patch('src.mv.os.path.exists') as mock_exists, \
             patch('src.mv.os.path.isfile') as mock_isfile, \
             patch('src.mv.shutil.move') as mock_move, \
             patch('builtins.print') as mock_print:
            mock_exists.return_value = True
            mock_isfile.return_value = True
            result = mv('old_name.txt', 'new_name.txt')
            assert result == 'Успешно'
            mock_move.assert_called_once_with('old_name.txt', 'new_name.txt')

    def test_file_to_dir(self):
        with patch('src.mv.os.path.exists') as mock_exists, \
             patch('src.mv.os.path.isfile') as mock_isfile, \
             patch('src.mv.os.path.isdir') as mock_isdir, \
             patch('src.mv.shutil.move') as mock_move, \
             patch('builtins.print') as mock_print:
            def exists_side_effect(path):
                return path in ['file.txt', 'target_dir']
            def isdir_side_effect(path):
                return path == 'target_dir'
            mock_exists.side_effect = exists_side_effect
            mock_isfile.side_effect = lambda x: x == 'file.txt'
            mock_isdir.side_effect = isdir_side_effect
            result = mv('file.txt', 'target_dir')
            assert result == 'Успешно'
            mock_move.assert_called_once_with('file.txt', 'target_dir/file.txt')

    def test_move_dir(self):
        with patch('src.mv.os.path.exists') as mock_exists, \
             patch('src.mv.os.path.isfile') as mock_isfile, \
             patch('src.mv.os.path.isdir') as mock_isdir, \
             patch('src.mv.shutil.move') as mock_move, \
             patch('builtins.print') as mock_print:
            mock_exists.return_value = True
            mock_isfile.return_value = False
            mock_isdir.return_value = True
            result = mv('old_dir', 'new_dir')
            assert result == 'Успешно'
            mock_move.assert_called_once_with('old_dir', 'new_dir')

    def test_overwrite_file(self):
        with patch('src.mv.os.path.exists') as mock_exists, \
             patch('src.mv.os.path.isfile') as mock_isfile, \
             patch('src.mv.shutil.move') as mock_move, \
             patch('builtins.print') as mock_print:
            mock_exists.return_value = True
            mock_isfile.return_value = True
            result = mv('new.txt', 'old.txt')
            assert result == 'Успешно'
            mock_move.assert_called_once_with('new.txt', 'old.txt')

    def test_self_move(self):
        with patch('src.mv.os.path.exists') as mock_exists, \
             patch('src.mv.os.path.isfile') as mock_isfile, \
             patch('src.mv.os.path.isdir') as mock_isdir, \
             patch('src.mv.os.path.commonpath') as mock_commonpath:
            mock_exists.return_value = True
            mock_isfile.return_value = False
            mock_isdir.return_value = True
            mock_commonpath.return_value = 'source_dir'
            with pytest.raises(ValueError):
                mv('source_dir', 'source_dir/copy')

    def test_to_existing_dir(self):
        with patch('src.mv.os.path.exists') as mock_exists, \
             patch('src.mv.os.path.isfile') as mock_isfile, \
             patch('src.mv.os.path.isdir') as mock_isdir, \
             patch('src.mv.shutil.move') as mock_move, \
             patch('builtins.print') as mock_print:
            def exists_side_effect(path):
                return path in ['file.txt', 'existing_dir']
            def isdir_side_effect(path):
                return path == 'existing_dir'
            mock_exists.side_effect = exists_side_effect
            mock_isfile.side_effect = lambda x: x == 'file.txt'
            mock_isdir.side_effect = isdir_side_effect
            result = mv('file.txt', 'existing_dir')
            assert result == 'Успешно'
            mock_move.assert_called_once_with('file.txt', 'existing_dir/file.txt')
