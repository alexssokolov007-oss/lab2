import pytest
from unittest.mock import Mock, patch
from src.errors import validate_path_exists, validate_is_file, validate_is_directory

class TestValidatePathExists:
    def test_path_exists(self):
        with patch('src.errors.os.path.exists') as mock_exists:
            mock_exists.return_value = True
            validate_path_exists('/some/path')
            mock_exists.assert_called_once_with('/some/path')
    
    def test_path_not_exists(self):
        with patch('src.errors.os.path.exists') as mock_exists:
            mock_exists.return_value = False
            with pytest.raises(FileNotFoundError):
                validate_path_exists('/nonexistent/path')
            mock_exists.assert_called_once_with('/nonexistent/path')

class TestValidateIsFile:
    def test_is_file(self):
        with patch('src.errors.os.path.isfile') as mock_isfile:
            mock_isfile.return_value = True
            validate_is_file('/some/file.txt')
            mock_isfile.assert_called_once_with('/some/file.txt')
    
    def test_is_not_file_directory(self):
        with patch('src.errors.os.path.isfile') as mock_isfile:
            mock_isfile.return_value = False
            with pytest.raises(IsADirectoryError):
                validate_is_file('/some/directory')
            mock_isfile.assert_called_once_with('/some/directory')
    
    def test_is_not_file_nonexistent(self):
        with patch('src.errors.os.path.isfile') as mock_isfile, \
             patch('src.errors.os.path.exists') as mock_exists:
            mock_isfile.return_value = False
            mock_exists.return_value = False
            with pytest.raises(FileNotFoundError):
                validate_is_file('/nonexistent/path')

class TestValidateIsDirectory:
    def test_is_directory(self):
        with patch('src.errors.os.path.isdir') as mock_isdir:
            mock_isdir.return_value = True
            validate_is_directory('/some/directory')
            mock_isdir.assert_called_once_with('/some/directory')
    
    def test_is_not_directory_file(self):
        with patch('src.errors.os.path.isdir') as mock_isdir:
            mock_isdir.return_value = False
            with pytest.raises(NotADirectoryError):
                validate_is_directory('/some/file.txt')
            mock_isdir.assert_called_once_with('/some/file.txt')
    
    def test_is_not_directory_nonexistent(self):
        with patch('src.errors.os.path.isdir') as mock_isdir, \
             patch('src.errors.os.path.exists') as mock_exists:
            mock_isdir.return_value = False
            mock_exists.return_value = False
            with pytest.raises(FileNotFoundError):
                validate_is_directory('/nonexistent/path')

class TestValidateIntegration:
    def test_validate_file_complete(self):
        with patch('src.errors.os.path.exists') as mock_exists, \
             patch('src.errors.os.path.isfile') as mock_isfile:
            mock_exists.return_value = True
            mock_isfile.return_value = True
            validate_path_exists('/path/to/file')
            validate_is_file('/path/to/file')
            mock_exists.assert_called_with('/path/to/file')
            mock_isfile.assert_called_with('/path/to/file')
    
    def test_validate_directory_complete(self):
        with patch('src.errors.os.path.exists') as mock_exists, \
             patch('src.errors.os.path.isdir') as mock_isdir:
            mock_exists.return_value = True
            mock_isdir.return_value = True
            validate_path_exists('/path/to/dir')
            validate_is_directory('/path/to/dir')
            mock_exists.assert_called_with('/path/to/dir')
            mock_isdir.assert_called_with('/path/to/dir')
