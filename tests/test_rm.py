import pytest
from unittest.mock import Mock, patch
from src.rm import rm


class TestRm:
    def test_nonexistent_file(self):
        with patch('src.rm.validate_path_exists') as mock_validate:
            mock_validate.side_effect = FileNotFoundError("Не существует")
            with pytest.raises(FileNotFoundError):
                rm('nonexistent.txt')

    def test_dir_without_recursive(self):
        with patch('src.rm.validate_path_exists'):
            with patch('src.rm.Path') as mock_path:
                mock_instance = Mock()
                mock_instance.exists.return_value = True
                mock_instance.is_dir.return_value = True
                mock_instance.resolve.return_value = Mock()
                
                mock_path.return_value.expanduser.return_value.resolve.return_value = mock_instance
                
                with pytest.raises(ValueError, match='Используйте -r для удаления директорий'):
                    rm('test_dir')

    def test_remove_file_simple(self):
        with patch('src.rm.validate_path_exists'):
            with patch('src.rm.Path') as mock_path:
                with patch('src.history_manager.safe_remove') as mock_safe_remove:
                    with patch('builtins.print') as mock_print:
                        mock_instance = Mock()
                        mock_instance.exists.return_value = True
                        mock_instance.is_dir.return_value = False
                        mock_instance.resolve.return_value = mock_instance
                        
                        mock_path.return_value.expanduser.return_value.resolve.return_value = mock_instance
                        
                        result = rm('test_file.txt')
                        
                        assert result == 'Успешно'
                        mock_print.assert_called_with('Успешно')

    def test_cancel_delete_simple(self):
        with patch('src.rm.validate_path_exists'):
            with patch('src.rm.Path') as mock_path:
                with patch('builtins.input') as mock_input:
                    with patch('builtins.print') as mock_print:
                        mock_instance = Mock()
                        mock_instance.exists.return_value = True
                        mock_instance.is_dir.return_value = True
                        mock_instance.resolve.return_value = mock_instance
                        
                        mock_path.return_value.expanduser.return_value.resolve.return_value = mock_instance
                        mock_input.return_value = 'n'
                        
                        result = rm('test_dir', recursive=True)
                        
                        assert result == 'Отменено'
                        mock_print.assert_called_with('Отменено')
