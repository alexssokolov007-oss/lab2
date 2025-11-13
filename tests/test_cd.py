import pytest
from unittest.mock import Mock, patch, MagicMock
from src.cd import cd

class TestCd:
    def test_nonexistent_dir(self):
        with patch('os.path.exists') as mock_exists:
            mock_exists.return_value = False
            with pytest.raises(FileNotFoundError):
                cd('nonexistent_dir')
    
    def test_file_instead_dir(self):
        with patch('os.path.exists') as mock_exists, \
             patch('os.path.isdir') as mock_isdir:
            mock_exists.return_value = True
            mock_isdir.return_value = False
            with pytest.raises(NotADirectoryError):
                cd('test_file.txt')
    
    def test_absolute_path(self):
        with patch('os.path.exists') as mock_exists, \
             patch('os.path.isdir') as mock_isdir, \
             patch('os.path.abspath') as mock_abspath, \
             patch('os.chdir') as mock_chdir:
            mock_exists.return_value = True
            mock_isdir.return_value = True
            mock_abspath.return_value = '/test/dir'
            result = cd('/test/dir')
            assert result == 'Успешно'
            mock_chdir.assert_called_once_with('/test/dir')
    
    def test_relative_path(self):
        with patch('os.path.exists') as mock_exists, \
             patch('os.path.isdir') as mock_isdir, \
             patch('os.path.abspath') as mock_abspath, \
             patch('os.chdir') as mock_chdir:
            mock_exists.return_value = True
            mock_isdir.return_value = True
            mock_abspath.return_value = '/current/dir/subdir'
            result = cd('subdir')
            assert result == 'Успешно'
            mock_chdir.assert_called_once_with('/current/dir/subdir')
    
    def test_home_dir(self):
        with patch('os.path.expanduser') as mock_expanduser, \
             patch('os.path.exists') as mock_exists, \
             patch('os.path.isdir') as mock_isdir, \
             patch('os.chdir') as mock_chdir:
            mock_expanduser.return_value = '/home/user'
            mock_exists.return_value = True
            mock_isdir.return_value = True
            result = cd('~')
            assert result == 'Успешно'
            mock_expanduser.assert_called_once_with('~')
            mock_chdir.assert_called_once_with('/home/user')
    
    def test_parent_dir(self):
        with patch('os.path.exists') as mock_exists, \
             patch('os.path.isdir') as mock_isdir, \
             patch('os.path.abspath') as mock_abspath, \
             patch('os.chdir') as mock_chdir:
            mock_exists.return_value = True
            mock_isdir.return_value = True
            mock_abspath.return_value = '/parent'
            result = cd('..')
            assert result == 'Успешно'
            mock_chdir.assert_called_once_with('/parent')
    
    def test_current_dir(self):
        with patch('os.path.exists') as mock_exists, \
             patch('os.path.isdir') as mock_isdir, \
             patch('os.path.abspath') as mock_abspath, \
             patch('os.chdir') as mock_chdir:
            mock_exists.return_value = True
            mock_isdir.return_value = True
            mock_abspath.return_value = '/current'
            result = cd('.')
            assert result == 'Успешно'
            mock_chdir.assert_called_once_with('/current')
    
    def test_empty_path(self):
        with patch('os.path.expanduser') as mock_expanduser, \
             patch('os.path.exists') as mock_exists, \
             patch('os.path.isdir') as mock_isdir, \
             patch('os.chdir') as mock_chdir:
            mock_expanduser.return_value = '/home/user'
            mock_exists.return_value = True
            mock_isdir.return_value = True
            result = cd()
            assert result == 'Успешно'
            mock_expanduser.assert_called_once_with('~')
            mock_chdir.assert_called_once_with('/home/user')
    
    def test_tilde_expansion(self):
        with patch('os.path.expanduser') as mock_expanduser, \
             patch('os.path.exists') as mock_exists, \
             patch('os.path.isdir') as mock_isdir, \
             patch('os.chdir') as mock_chdir:
            mock_expanduser.return_value = '/home/user/documents'
            mock_exists.return_value = True
            mock_isdir.return_value = True
            result = cd('~/documents')
            assert result == 'Успешно'
            mock_expanduser.assert_called_once_with('~/documents')
            mock_chdir.assert_called_once_with('/home/user/documents')
    
    def test_complex_relative_path(self):
        with patch('os.path.exists') as mock_exists, \
             patch('os.path.isdir') as mock_isdir, \
             patch('os.path.abspath') as mock_abspath, \
             patch('os.chdir') as mock_chdir:
            mock_exists.return_value = True
            mock_isdir.return_value = True
            mock_abspath.return_value = '/target/dir'
            result = cd('../sibling/../target/dir')
            assert result == 'Успешно'
            mock_chdir.assert_called_once_with('/target/dir')
