import pytest
from unittest.mock import Mock, patch
from src.rm import rm


class TestRm:
    def test_nonexistent_file(self):
        """Попытка удаления несуществующего файла/папки"""
        with pytest.raises(FileNotFoundError):
            rm('nonexistent.txt')

    def test_dir_without_recursive(self, tmp_path):
        """Попытка удаления директории без флага -r"""
        test_dir = tmp_path / "test_dir"
        test_dir.mkdir()
        
        with pytest.raises(ValueError, match='Используйте -r для удаления директорий'):
            rm(str(test_dir))

    def test_remove_file_simple(self, tmp_path, capsys):
        """Успешное удаление обычного файла"""
        test_file = tmp_path / "test_file.txt"
        test_file.write_text("content")
        
        # Мокаем safe_remove чтобы избежать реального удаления
        with patch('src.rm.safe_remove') as mock_safe_remove:
            result = rm(str(test_file))
            
            assert result == 'Успешно'
            mock_safe_remove.assert_called_once()
            captured = capsys.readouterr()
            assert 'Успешно' in captured.out

    def test_cancel_delete_simple(self, tmp_path, capsys):
        """Отмена удаления директории при ответе 'n' на запрос подтверждения"""
        test_dir = tmp_path / "test_dir"
        test_dir.mkdir()
        
        def mock_input(prompt):
            print(prompt, end='')  #проверка
            return 'n'
        
        with patch('src.rm.safe_remove') as mock_safe_remove:
            with patch('src.rm.input', mock_input):
                result = rm(str(test_dir), recursive=True, input_func=mock_input)
                
                assert result == 'Отменено'
                mock_safe_remove.assert_not_called()
                captured = capsys.readouterr()
                assert 'Отменено' in captured.out
                assert 'Удалить директорию' in captured.out

    def test_confirm_delete_simple(self, tmp_path, capsys):
        """Подтверждение удаления директории при ответе 'y'"""
        test_dir = tmp_path / "test_dir"
        test_dir.mkdir()
        
        # monkeypatch подменяет input
        def mock_input(prompt):
            print(prompt, end='')  # проверка
            return 'y'

        with patch('src.rm.safe_remove') as mock_safe_remove:
            with patch('src.rm.input', mock_input):
                result = rm(str(test_dir), recursive=True, input_func=mock_input)
                
                assert result == 'Успешно'
                mock_safe_remove.assert_called_once()
                captured = capsys.readouterr()
                assert 'Успешно' in captured.out
                assert 'Удалить директорию' in captured.out

    def test_remove_file_without_confirmation(self, tmp_path, capsys):
        """Удаление файла без подтверждения"""
        test_file = tmp_path / "test_file.txt"
        test_file.write_text("content")
        
        with patch('src.rm.safe_remove') as mock_safe_remove:
            result = rm(str(test_file))
            
            assert result == 'Успешно'
            mock_safe_remove.assert_called_once()
            captured = capsys.readouterr()
            assert 'Успешно' in captured.out