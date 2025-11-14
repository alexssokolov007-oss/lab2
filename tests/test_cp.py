import pytest
from unittest.mock import Mock, patch
from src.cp import cp


class TestCp:
    def test_nonexistent_source(self):
        with patch('src.cp.validate_path_exists') as mock_validate:
            mock_validate.side_effect = FileNotFoundError("Не существует")
            with pytest.raises(FileNotFoundError):
                cp('nonexistent.txt', 'destination.txt')

    def test_copy_file(self):
        with patch('src.cp.validate_path_exists'):
            with patch('src.cp.Path') as mock_path:
                with patch('src.cp.shutil') as mock_shutil:
                    with patch('builtins.print') as mock_print:
                        src_mock = Mock()
                        src_mock.exists.return_value = True
                        src_mock.is_dir.return_value = False
                        
                        mock_path.side_effect = [src_mock, Mock()]
                        
                        result = cp('source.txt', 'dest.txt')
                        
                        assert result == 'Успешно'
                        mock_shutil.copy2.assert_called_once()
                        mock_print.assert_called_with('Успешно')

    def test_copy_dir_without_recursive(self):
        with patch('src.cp.validate_path_exists'):
            with patch('src.cp.Path') as mock_path:
                src_mock = Mock()
                src_mock.exists.return_value = True
                src_mock.is_dir.return_value = True
                
                mock_path.return_value = src_mock
                
                with pytest.raises(NotADirectoryError, match='Для копирования директорий используйте флаг -r'):
                    cp('source_dir', 'dest_dir')

    def test_copy_dir_with_recursive(self):
        with patch('src.cp.validate_path_exists'):
            with patch('src.cp.validate_not_self_copy'):
                with patch('src.cp.Path') as mock_path:
                    with patch('src.cp.shutil') as mock_shutil:
                        with patch('builtins.print') as mock_print:
                            src_mock = Mock()
                            src_mock.exists.return_value = True
                            src_mock.is_dir.return_value = True
                            
                            mock_path.side_effect = [src_mock, Mock()]
                            
                            result = cp('source_dir', 'dest_dir', recursive=True)
                            
                            assert result == 'Успешно'
                            mock_shutil.copytree.assert_called_once()
                            mock_print.assert_called_with('Успешно')
