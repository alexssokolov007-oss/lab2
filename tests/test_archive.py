import pytest
from unittest.mock import Mock, patch, MagicMock
from src.archive import zip_folder, tar_folder, unzip_archive, untar_archive

class TestArchive:

    def test_zip_nonexistent(self):
        with patch('src.archive.os.path.exists') as mock_exists:
            mock_exists.return_value = False
            with pytest.raises(FileNotFoundError):
                zip_folder('nonexistent_folder')
    
    def test_zip_not_folder(self):
        with patch('src.archive.os.path.exists') as mock_exists, \
             patch('src.archive.os.path.isdir') as mock_isdir:
            mock_exists.return_value = True
            mock_isdir.return_value = False
            with pytest.raises(ValueError):
                zip_folder('test_file.txt')
    
    def test_zip_creation(self):
        with patch('src.archive.os.path.exists') as mock_exists, \
             patch('src.archive.os.path.isdir') as mock_isdir, \
             patch('src.archive.zipfile.ZipFile') as mock_zipfile, \
             patch('src.archive.os.walk') as mock_walk:
            mock_exists.return_value = True
            mock_isdir.return_value = True
            mock_walk.return_value = [
                ('source', ['subdir'], ['file1.txt', 'file2.txt']),
                ('source/subdir', [], ['file3.txt'])
            ]
            mock_zip_instance = MagicMock()
            mock_zipfile.return_value.__enter__.return_value = mock_zip_instance
            result = zip_folder('source', 'archive.zip')
            assert result == 'Успешно'
            mock_zipfile.assert_called_once_with('archive.zip', 'w')
            assert mock_zip_instance.write.call_count == 3
               
    def test_zip_default_name(self):
        with patch('src.archive.os.path.exists') as mock_exists, \
             patch('src.archive.os.path.isdir') as mock_isdir, \
             patch('src.archive.zipfile.ZipFile') as mock_zipfile, \
             patch('src.archive.os.walk') as mock_walk:
            mock_exists.return_value = True
            mock_isdir.return_value = True
            mock_walk.return_value = [('my_folder', [], ['file.txt'])]
            mock_zip_instance = MagicMock()
            mock_zipfile.return_value.__enter__.return_value = mock_zip_instance
            result = zip_folder('my_folder')
            assert result == 'Успешно'
            mock_zipfile.assert_called_once_with('my_folder.zip', 'w')
    
    def test_unzip_file(self):
        with patch('src.archive.os.path.exists') as mock_exists, \
             patch('src.archive.zipfile.ZipFile') as mock_zipfile:
            mock_exists.return_value = True
            mock_zip_instance = MagicMock()
            mock_zip_instance.namelist.return_value = ['file1.txt', 'file2.txt']
            mock_zipfile.return_value.__enter__.return_value = mock_zip_instance
            result = unzip_archive('archive.zip')
            assert result == 'Успешно'
            mock_zipfile.assert_called_once_with('archive.zip', 'r')
            mock_zip_instance.extractall.assert_called_once()
    
    def test_unzip_nonexistent(self):
        with patch('src.archive.os.path.exists') as mock_exists:
            mock_exists.return_value = False
            with pytest.raises(FileNotFoundError):
                unzip_archive('nonexistent.zip')
    
    def test_tar_creation(self):
        with patch('src.archive.os.path.exists') as mock_exists, \
             patch('src.archive.os.path.isdir') as mock_isdir, \
             patch('src.archive.tarfile.open') as mock_tarfile, \
             patch('src.archive.os.walk') as mock_walk:
            mock_exists.return_value = True
            mock_isdir.return_value = True
            mock_walk.return_value = [('data', [], ['info.txt'])]
            mock_tar_instance = MagicMock()
            mock_tarfile.return_value.__enter__.return_value = mock_tar_instance
            result = tar_folder('data', 'data.tar.gz')
            assert result == 'Успешно'
            mock_tarfile.assert_called_once_with('data.tar.gz', 'w:gz')
            mock_tar_instance.add.assert_called_once_with('data')
    
    def test_untar_file(self):
        with patch('src.archive.os.path.exists') as mock_exists, \
             patch('src.archive.tarfile.open') as mock_tarfile:
            mock_exists.return_value = True
            mock_tar_instance = MagicMock()
            mock_tarfile.return_value.__enter__.return_value = mock_tar_instance
            result = untar_archive('source.tar.gz')
            assert result == 'Успешно'
            mock_tarfile.assert_called_once_with('source.tar.gz', 'r:*')
            mock_tar_instance.extractall.assert_called_once()
    
    def test_untar_nonexistent(self):
        with patch('src.archive.os.path.exists') as mock_exists:
            mock_exists.return_value = False
            with pytest.raises(FileNotFoundError):
                untar_archive('nonexistent.tar.gz')
    
    def test_zip_with_subdirs(self):
        with patch('src.archive.os.path.exists') as mock_exists, \
             patch('src.archive.os.path.isdir') as mock_isdir, \
             patch('src.archive.zipfile.ZipFile') as mock_zipfile, \
             patch('src.archive.os.walk') as mock_walk:
            mock_exists.return_value = True
            mock_isdir.return_value = True
            mock_walk.return_value = [
                ('project', ['src', 'docs'], ['.gitignore']),
                ('project/src', [], ['main.py']),
                ('project/docs', [], ['readme.md'])
            ]
            mock_zip_instance = MagicMock()
            mock_zipfile.return_value.__enter__.return_value = mock_zip_instance
            result = zip_folder('project', 'project.zip')
            assert result == 'Успешно'
            mock_zipfile.assert_called_once_with('project.zip', 'w')
            assert mock_zip_instance.write.call_count == 3
    
    def test_tar_with_subdirs(self):
        with patch('src.archive.os.path.exists') as mock_exists, \
             patch('src.archive.os.path.isdir') as mock_isdir, \
             patch('src.archive.tarfile.open') as mock_tarfile, \
             patch('src.archive.os.walk') as mock_walk:
            mock_exists.return_value = True
            mock_isdir.return_value = True
            mock_walk.return_value = [
                ('app', ['static', 'templates'], ['main.py']),
                ('app/static', [], ['style.css']),
                ('app/templates', [], ['index.html'])
            ]
            mock_tar_instance = MagicMock()
            mock_tarfile.return_value.__enter__.return_value = mock_tar_instance
            result = tar_folder('app', 'app.tar.gz')
            assert result == 'Успешно'
            mock_tarfile.assert_called_once_with('app.tar.gz', 'w:gz')
            mock_tar_instance.add.assert_called_once_with('app')
