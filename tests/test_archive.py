import pytest
from unittest.mock import Mock, patch
from src.archive import zip_folder, unzip_archive, tar_folder, untar_archive


class TestArchive:
    def test_zip_nonexistent_folder(self):
        """zip_folder с несуществующей папкой"""
        with pytest.raises(FileNotFoundError):
            zip_folder('nonexistent_folder')

    def test_zip_file_instead_folder(self, tmp_path):
        """zip_folder с файлом вместо папки"""
        real_file = tmp_path / "test_file.txt"
        real_file.write_text("test")
        
        with pytest.raises(ValueError, match="не является папкой"):
            zip_folder(str(real_file))

    def test_zip_folder_success(self, tmp_path):
        """Успешное создание zip архива"""
        test_dir = tmp_path / "source"
        test_dir.mkdir()
        (test_dir / "file1.txt").write_text("content1")
        (test_dir / "file2.txt").write_text("content2")
        
        archive_path = tmp_path / "archive.zip"
        
        result = zip_folder(str(test_dir), str(archive_path))
        
        assert result == 'Успешно'
        assert archive_path.exists()

    def test_unzip_nonexistent_archive(self):
        """Распаковка несуществующего архива"""
        with pytest.raises(FileNotFoundError):
            unzip_archive('nonexistent.zip')

    def test_tar_folder_success(self, tmp_path):
        """Успешное создание tar архива"""
        test_dir = tmp_path / "data"
        test_dir.mkdir()
        (test_dir / "file.txt").write_text("content")
        
        archive_path = tmp_path / "data.tar.gz"
        
        result = tar_folder(str(test_dir), str(archive_path))
        
        assert result == 'Успешно'
        assert archive_path.exists()

    def test_untar_nonexistent(self):
        """Распаковка несуществующего tar архива"""
        with pytest.raises(FileNotFoundError):
            untar_archive('nonexistent.tar.gz')