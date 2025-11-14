import pytest
from unittest.mock import Mock, patch
from src.archive import zip_folder, unzip_archive, tar_folder, untar_archive


class TestArchive:
    """Полные тесты для архивных функций с моками"""

    def test_zip_nonexistent_folder(self):
        """Тест: zip_folder с несуществующей папкой"""
        with patch('src.archive.validate_path_exists') as mock_validate:
            mock_validate.side_effect = FileNotFoundError("Не существует")
            with pytest.raises(FileNotFoundError):
                zip_folder('nonexistent_folder')

    def test_zip_file_instead_folder(self):
        """Тест: zip_folder с файлом вместо папки"""
        with patch('src.archive.Path') as mock_path:
            mock_instance = mock_path.return_value
            mock_instance.exists.return_value = True
            mock_instance.is_dir.return_value = False
            
            with pytest.raises(ValueError, match="не является папкой"):
                zip_folder('test_file.txt')

    def test_zip_folder_success(self):
        """Тест: успешное создание zip архива"""
        with patch('src.archive.validate_path_exists'):
            with patch('src.archive.Path') as mock_path:
                with patch('src.archive.zipfile') as mock_zipfile:
                    # Настраиваем моки
                    mock_folder = Mock()
                    mock_folder.exists.return_value = True
                    mock_folder.is_dir.return_value = True
                    mock_folder.name = 'source'
                    mock_folder.rglob.return_value = [
                        Mock(is_file=Mock(return_value=True), 
                             relative_to=Mock(return_value='file1.txt')),
                    ]
                    
                    mock_zip_instance = Mock()
                    mock_zipfile.ZipFile.return_value.__enter__.return_value = mock_zip_instance
                    
                    mock_path.return_value = mock_folder
                    
                    # Вызываем тестируемую функцию
                    result = zip_folder('source', 'archive.zip')
                    
                    # Проверяем результаты
                    assert result == 'Успешно'
                    mock_zipfile.ZipFile.assert_called_once()

    def test_zip_default_name(self):
        """Тест: создание zip с именем по умолчанию"""
        with patch('src.archive.validate_path_exists'):
            with patch('src.archive.Path') as mock_path:
                with patch('src.archive.zipfile') as mock_zipfile:
                    mock_folder = Mock()
                    mock_folder.exists.return_value = True
                    mock_folder.is_dir.return_value = True
                    mock_folder.name = 'my_folder'
                    mock_folder.rglob.return_value = []
                    
                    mock_zip_instance = Mock()
                    mock_zipfile.ZipFile.return_value.__enter__.return_value = mock_zip_instance
                    
                    mock_path.return_value = mock_folder
                    
                    result = zip_folder('my_folder')
                    
                    assert result == 'Успешно'
                    # Проверяем что имя архива сгенерировано правильно
                    mock_zipfile.ZipFile.assert_called_with('my_folder.zip', 'w', mock_zipfile.ZIP_DEFLATED)

    def test_unzip_nonexistent_archive(self):
        """Тест: распаковка несуществующего архива"""
        with patch('src.archive.validate_path_exists') as mock_validate:
            mock_validate.side_effect = FileNotFoundError("Не существует")
            with pytest.raises(FileNotFoundError):
                unzip_archive('nonexistent.zip')

    def test_unzip_success(self):
        """Тест: успешная распаковка zip архива"""
        with patch('src.archive.validate_path_exists'):
            with patch('src.archive.Path') as mock_path:
                with patch('src.archive.zipfile') as mock_zipfile:
                    mock_archive = Mock()
                    mock_archive.exists.return_value = True
                    
                    mock_zip_instance = Mock()
                    mock_zipfile.ZipFile.return_value.__enter__.return_value = mock_zip_instance
                    
                    mock_path.return_value = mock_archive
                    
                    result = unzip_archive('archive.zip')
                    
                    assert result == 'Успешно'
                    mock_zipfile.ZipFile.assert_called_once()

    def test_tar_folder_success(self):
        """Тест: успешное создание tar архива"""
        with patch('src.archive.validate_path_exists'):
            with patch('src.archive.Path') as mock_path:
                with patch('src.archive.tarfile') as mock_tarfile:
                    mock_folder = Mock()
                    mock_folder.exists.return_value = True
                    mock_folder.is_dir.return_value = True
                    
                    mock_tar_instance = Mock()
                    mock_tarfile.open.return_value.__enter__.return_value = mock_tar_instance
                    
                    mock_path.return_value = mock_folder
                    
                    result = tar_folder('data', 'data.tar.gz')
                    
                    assert result == 'Успешно'
                    mock_tarfile.open.assert_called_once_with('data.tar.gz', 'w:gz')

    def test_untar_success(self):
        """Тест: успешная распаковка tar архива"""
        with patch('src.archive.validate_path_exists'):
            with patch('src.archive.Path') as mock_path:
                with patch('src.archive.tarfile') as mock_tarfile:
                    mock_archive = Mock()
                    mock_archive.exists.return_value = True
                    
                    mock_tar_instance = Mock()
                    mock_tarfile.open.return_value.__enter__.return_value = mock_tar_instance
                    
                    mock_path.return_value = mock_archive
                    
                    result = untar_archive('source.tar.gz')
                    
                    assert result == 'Успешно'
                    mock_tarfile.open.assert_called_once()

    def test_untar_nonexistent(self):
        """Тест: распаковка несуществующего tar архива"""
        with patch('src.archive.validate_path_exists') as mock_validate:
            mock_validate.side_effect = FileNotFoundError("Не существует")
            with pytest.raises(FileNotFoundError):
                untar_archive('nonexistent.tar.gz')
