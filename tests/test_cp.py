import pytest
from unittest.mock import Mock, patch, MagicMock, call
from src.cp import cp

class TestCp:
    def test_nonexistent_source(self):
        with patch('os.path.exists') as mock_exists:
            mock_exists.side_effect = lambda x: False
            
            with pytest.raises(FileNotFoundError):
                cp('nonexistent.txt', 'copy.txt')
    
    def test_copy_file(self):
        with patch('os.path.exists') as mock_exists, \
             patch('os.path.isfile') as mock_isfile, \
             patch('os.path.isdir') as mock_isdir, \
             patch('shutil.copy2') as mock_copy, \
             patch('builtins.print') as mock_print:
            def exists_side_effect(path):
                return path == 'source.txt'
            
            mock_exists.side_effect = exists_side_effect
            mock_isfile.return_value = True
            mock_isdir.return_value = False
            result = cp('source.txt', 'destination.txt')
            assert result == 'Успешно'
            mock_copy.assert_called_once_with('source.txt', 'destination.txt')
            mock_print.assert_not_called()
    
    def test_dir_without_recursive(self):
        with patch('os.path.exists') as mock_exists, \
             patch('os.path.isfile') as mock_isfile, \
             patch('os.path.isdir') as mock_isdir:
            
            mock_exists.return_value = True
            mock_isfile.return_value = False
            mock_isdir.return_value = True
            with pytest.raises(NotADirectoryError):
                cp('source_dir', 'dest_dir')
    
    def test_recursive_copy(self):
        with patch('os.path.exists') as mock_exists, \
             patch('os.path.isfile') as mock_isfile, \
             patch('os.path.isdir') as mock_isdir, \
             patch('shutil.copytree') as mock_copytree, \
             patch('builtins.print') as mock_print:
            mock_exists.return_value = True
            mock_isfile.return_value = False
            mock_isdir.return_value = True
            result = cp('source_dir', 'dest_dir', recursive=True)
            assert result == 'Успешно'
            mock_copytree.assert_called_once_with('source_dir', 'dest_dir')
            mock_print.assert_not_called()
    
    def test_file_to_dir(self):
        with patch('os.path.exists') as mock_exists, \
             patch('os.path.isfile') as mock_isfile, \
             patch('os.path.isdir') as mock_isdir, \
             patch('shutil.copy2') as mock_copy, \
             patch('builtins.print') as mock_print:
            
            def exists_side_effect(path):
                return path in ['file.txt', 'target_dir']
            
            def isdir_side_effect(path):
                return path == 'target_dir'
            
            mock_exists.side_effect = exists_side_effect
            mock_isfile.side_effect = lambda x: x == 'file.txt'
            mock_isdir.side_effect = isdir_side_effect
            result = cp('file.txt', 'target_dir')
            assert result == 'Успешно'
            mock_copy.assert_called_once_with('file.txt', 'target_dir/file.txt')
            mock_print.assert_not_called()
    
    def test_overwrite_file(self):
        with patch('os.path.exists') as mock_exists, \
             patch('os.path.isfile') as mock_isfile, \
             patch('os.path.isdir') as mock_isdir, \
             patch('shutil.copy2') as mock_copy, \
             patch('builtins.print') as mock_print:
            
            mock_exists.return_value = True
            mock_isfile.return_value = True
            mock_isdir.return_value = False
            result = cp('source.txt', 'existing.txt')
            assert result == 'Успешно'
            mock_copy.assert_called_once_with('source.txt', 'existing.txt')
            mock_print.assert_not_called()
    
    def test_self_copy(self):
        with patch('os.path.exists') as mock_exists, \
             patch('os.path.isfile') as mock_isfile, \
             patch('os.path.isdir') as mock_isdir, \
             patch('os.path.commonpath') as mock_commonpath:
            
            mock_exists.return_value = True
            mock_isfile.return_value = False
            mock_isdir.return_value = True
            mock_commonpath.return_value = 'source_dir'
            with pytest.raises(ValueError):
                cp('source_dir', 'source_dir/copy', recursive=True)
    
    def test_multiple_files(self):
        with patch('os.path.exists') as mock_exists, \
             patch('os.path.isfile') as mock_isfile, \
             patch('os.path.isdir') as mock_isdir, \
             patch('shutil.copy2') as mock_copy, \
             patch('builtins.print') as mock_print:
            
            def exists_side_effect(path):
                return path in ['file1.txt', 'file2.txt', 'backup']
            
            def isdir_side_effect(path):
                return path == 'backup'
            
            mock_exists.side_effect = exists_side_effect
            mock_isfile.side_effect = lambda x: x in ['file1.txt', 'file2.txt']
            mock_isdir.side_effect = isdir_side_effect
            result1 = cp('file1.txt', 'backup')
            assert result1 == 'Успешно'
            result2 = cp('file2.txt', 'backup')
            assert result2 == 'Успешно'
            copy_calls = mock_copy.call_args_list
            assert len(copy_calls) == 2
            assert call('file1.txt', 'backup/file1.txt') in copy_calls
            assert call('file2.txt', 'backup/file2.txt') in copy_calls
    
    def test_copy_with_spaces_in_names(self):
        with patch('os.path.exists') as mock_exists, \
             patch('os.path.isfile') as mock_isfile, \
             patch('os.path.isdir') as mock_isdir, \
             patch('shutil.copy2') as mock_copy, \
             patch('builtins.print') as mock_print:
            
            mock_exists.return_value = True
            mock_isfile.return_value = True
            mock_isdir.return_value = False
            result = cp('file with spaces.txt', 'destination with spaces.txt')
            assert result == 'Успешно'
            mock_copy.assert_called_once_with('file with spaces.txt', 'destination with spaces.txt')
