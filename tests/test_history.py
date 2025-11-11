import pytest
from unittest.mock import Mock, patch
from src.history_manager import show_history, undo_last

class TestHistoryManager:
    def test_display_history(self):
        with patch('src.history_manager.print') as mock_print, \
             patch('src.history_manager.history_manager') as mock_manager:
            mock_manager.history = [
                {'command': 'ls', 'timestamp': '2023-01-01 10:00:00'},
                {'command': 'cd /tmp', 'timestamp': '2023-01-01 10:01:00'}
            ]
            result = show_history()
            assert result == 'Успешно'
            assert mock_print.call_count == 2

    def test_undo_empty(self):
        with patch('src.history_manager.history_manager') as mock_manager:
            mock_manager.history = []
            result = undo_last()
            assert result is None
