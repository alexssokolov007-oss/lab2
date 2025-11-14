import pytest
from unittest.mock import Mock, patch
from src.cd import cd


class TestCd:
    def test_nonexistent_dir(self):
        """Переход в несуществующую директорию"""
        with patch('src.cd.validate_path_exists') as mock_validate:
            mock_validate.side_effect = FileNotFoundError("Не существует")
            with pytest.raises(FileNotFoundError):
                cd('nonexistent_dir')

    def test_file_instead_dir(self):
        """Попытка перейти в файл вместо директории"""
        with patch('src.cd.validate_path_exists'):
            with patch('src.cd.validate_is_directory') as mock_validate_dir:
                mock_validate_dir.side_effect = NotADirectoryError("Не директория")
                with pytest.raises(NotADirectoryError):
                    cd('test_file.txt')

    def test_absolute_path(self):
        """Переход по абсолютному пути"""
        with patch('src.cd.os') as mock_os:
            with patch('src.cd.Path') as mock_path:
                mock_new_path = Mock()
                mock_new_path.__str__ = Mock(return_value='/test/dir')
                mock_path_instance = Mock()
                mock_path_instance.expanduser.return_value.resolve.return_value = mock_new_path
                mock_path.return_value = mock_path_instance
                
                with patch('src.cd.validate_path_exists'):
                    with patch('src.cd.validate_is_directory'):
                        result = cd('/test/dir', os_module=mock_os)
                        
                        assert result == 'Успешно'
                        mock_os.chdir.assert_called_once_with(mock_new_path)

    def test_home_dir(self):
        """Переход в домашнюю директорию (~)"""
        with patch('src.cd.os') as mock_os:
            with patch('src.cd.Path') as mock_path:
                mock_home = Mock()
                mock_home.__str__ = Mock(return_value='/home/user')
                mock_path.home.return_value = mock_home
                
                result = cd('~', os_module=mock_os)
                
                assert result == 'Успешно'
                mock_os.chdir.assert_called_once_with(mock_home)