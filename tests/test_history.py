import pytest
from unittest.mock import Mock, patch
from src.history_manager import HistoryManager, show_history, undo_last


class TestHistoryManager:
    def test_show_history_empty(self):
        """Пустая история"""
        mock_print = Mock()
        manager = HistoryManager()
        manager.history = []
        
        manager.show_history(print_func=mock_print)
        
        mock_print.assert_called_with('История пуста')

    def test_show_history_with_entries(self):
        """История с записями"""
        mock_print = Mock()
        manager = HistoryManager()
        manager.history = [
            {'timestamp': '2024-01-01 10:00:00', 'command': 'ls'},
            {'timestamp': '2024-01-01 10:01:00', 'command': 'cd /tmp'}
        ]
        
        manager.show_history(print_func=mock_print)
        
        assert mock_print.call_count == 3
        mock_print.assert_any_call('Последние 2 команд:')

    def test_undo_empty(self):
        """Отмена при пустой истории"""
        mock_print = Mock()
        manager = HistoryManager()
        manager.history = []
        
        result = manager.undo_last(print_func=mock_print)
        
        assert 'нет операций для отмены' in result
        mock_print.assert_called_with('Ошибка: нет операций для отмены')

    def test_add_command(self):
        """Добавление команды"""
        manager = HistoryManager()
        manager.history = []
        manager.history_file = Mock()
        
        manager.add_command('ls -l', 'ls')
        
        assert len(manager.history) == 1
        assert manager.history[0]['command'] == 'ls -l'
        manager.history_file.write_text.assert_called_once()

    def test_undo_cp_operation(self):
        """Отмена копирования"""
        mock_print = Mock()
        manager = HistoryManager()
        manager.history = [
            {'type': 'cp', 'source': 'src.txt', 'destination': 'dst.txt'}
        ]
        manager.shutil = Mock()

        with patch('src.history_manager.Path') as mock_path:
            mock_dst = Mock()
            mock_dst.exists.return_value = True
            mock_path.return_value = mock_dst

            with patch.object(manager, 'safe_remove') as mock_safe_remove:
                result = manager.undo_last(print_func=mock_print)

                assert result == 'Успешно'
                mock_safe_remove.assert_called_once()

    def test_safe_remove(self):
        """Безопасное удаление"""
        manager = HistoryManager()
        manager.shutil = Mock()

        with patch('src.history_manager.TRASH_DIR') as mock_trash_dir:
            mock_trash_path = Mock()
            mock_trash_path.exists.return_value = False
            mock_trash_dir.__truediv__.return_value = mock_trash_path

            manager.safe_remove('test.txt')
            
            manager.shutil.move.assert_called_once()


def test_show_history_function():
    with patch('src.history_manager.history_manager') as mock_manager:
        result = show_history()
        
        assert result == 'Успешно'
        mock_manager.show_history.assert_called_once_with(10)


def test_undo_last_function():
    with patch('src.history_manager.history_manager') as mock_manager:
        mock_manager.undo_last.return_value = 'Успешно'
        
        result = undo_last()
        
        assert result == 'Успешно'
        mock_manager.undo_last.assert_called_once()