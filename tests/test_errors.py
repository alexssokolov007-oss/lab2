import pytest
from unittest.mock import Mock, patch
from src.errors import validate_path_exists, validate_is_file, validate_is_directory


class TestValidatePathExists:
    def test_path_exists(self, tmp_path):
        """Путь существует"""
        # временный файл
        real_file = tmp_path / "test_file.txt"
        real_file.write_text("test")
        
        validate_path_exists(str(real_file))

    def test_path_not_exists(self):
        """Путь не существует"""
        with pytest.raises(FileNotFoundError, match="не существует"):
            validate_path_exists('/nonexistent/path')


class TestValidateIsFile:
    def test_is_file(self, tmp_path):
        """Путь является файлом"""
        real_file = tmp_path / "test_file.txt"
        real_file.write_text("test")
        
        validate_is_file(str(real_file))

    def test_is_not_file(self, tmp_path):
        """Путь не является файлом"""
        real_dir = tmp_path / "test_dir"
        real_dir.mkdir()
        
        with pytest.raises(IsADirectoryError, match="не является файлом"):
            validate_is_file(str(real_dir))


class TestValidateIsDirectory:
    def test_is_directory(self, tmp_path):
        """Путь является директорией"""
        real_dir = tmp_path / "test_dir"
        real_dir.mkdir()
        
        validate_is_directory(str(real_dir))

    def test_is_not_directory(self, tmp_path):
        """Путь не является директорией"""
        real_file = tmp_path / "test_file.txt"
        real_file.write_text("test")
        
        with pytest.raises(NotADirectoryError, match="не является директорией"):
            validate_is_directory(str(real_file))