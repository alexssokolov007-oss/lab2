import pytest
from unittest.mock import Mock, patch
from src.mv import mv


class TestMvSimple:
    """Упрощенные тесты для mv команды"""

    def test_nonexistent_source(self):
        """Тест: перемещение несуществующего файла"""
        with patch('src.mv.validate_path_exists') as mock_validate:
            mock_validate.side_effect = FileNotFoundError("Не существует")
            with pytest.raises(FileNotFoundError):
                mv('nonexistent.txt', 'destination.txt')

    def test_rename_file_basic(self):
        """Тест: базовое переименование файла"""
        with patch('src.mv.validate_path_exists'):
            with patch('src.mv.Path') as mock_path:
                with patch('src.mv.shutil') as mock_shutil:
                    with patch('builtins.print') as mock_print:
                        # Создаем простые моки
                        src_mock = Mock()
                        src_mock.exists.return_value = True
                        src_mock.is_dir.return_value = False
                        
                        dst_mock = Mock()
                        dst_mock.exists.return_value = False
                        dst_mock.is_dir.return_value = False
                        
                        mock_path.side_effect = [src_mock, dst_mock]
                        
                        result = mv('old_name.txt', 'new_name.txt')
                        
                        assert result == 'Успешно'
                        # Проверяем что move был вызван (не проверяем конкретные аргументы)
                        mock_shutil.move.assert_called_once()
                        mock_print.assert_called_with('Успешно')

    def test_move_dir_basic(self):
        """Тест: базовое перемещение директории"""
        with patch('src.mv.validate_path_exists'):
            with patch('src.mv.validate_not_self_copy'):
                with patch('src.mv.Path') as mock_path:
                    with patch('src.mv.shutil') as mock_shutil:
                        with patch('builtins.print') as mock_print:
                            src_mock = Mock()
                            src_mock.exists.return_value = True
                            src_mock.is_dir.return_value = True
                            
                            dst_mock = Mock()
                            dst_mock.exists.return_value = False
                            dst_mock.is_dir.return_value = False
                            
                            mock_path.side_effect = [src_mock, dst_mock]
                            
                            result = mv('old_dir', 'new_dir')
                            
                            assert result == 'Успешно'
                            mock_shutil.move.assert_called_once()

    def test_overwrite_file_basic(self):
        """Тест: базовая перезапись файла"""
        with patch('src.mv.validate_path_exists'):
            with patch('src.mv.Path') as mock_path:
                with patch('src.mv.shutil') as mock_shutil:
                    with patch('builtins.print') as mock_print:
                        src_mock = Mock()
                        src_mock.exists.return_value = True
                        src_mock.is_dir.return_value = False
                        
                        dst_mock = Mock()
                        dst_mock.exists.return_value = True
                        dst_mock.is_dir.return_value = False
                        
                        mock_path.side_effect = [src_mock, dst_mock]
                        
                        result = mv('new.txt', 'old.txt')
                        
                        assert result == 'Успешно'
                        mock_shutil.move.assert_called_once()
