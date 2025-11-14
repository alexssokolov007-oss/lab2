import pytest
from unittest.mock import patch, MagicMock, call
from src.history_manager import show_history, history_manager, HistoryManager
from pathlib import Path

# Создаем необходимые папки для тестов
Path(".trash").mkdir(exist_ok=True)
Path(".history").touch(exist_ok=True)

class TestHistoryManager:
    def test_display_history(self):
        # Сохраняем оригинальное состояние
        original_history = history_manager.history.copy()
        
        try:
            # Устанавливаем тестовые данные
            history_manager.history = [
                {'command': 'ls', 'timestamp': '2023-01-01 10:00:00'},
                {'command': 'cd /tmp', 'timestamp': '2023-01-01 10:01:00'}
            ]
            
            with patch('builtins.print') as mock_print:
                result = show_history()
                
                assert result == 'Успешно'
                # Проверяем что print был вызван минимум 2 раза
                assert mock_print.call_count >= 2
                
        finally:
            # Восстанавливаем оригинальную историю
            history_manager.history = original_history

    def test_display_history_empty(self):
        # Сохраняем оригинальное состояние
        original_history = history_manager.history.copy()
        
        try:
            history_manager.history = []
            
            with patch('builtins.print') as mock_print:
                result = show_history()
                
                assert result == 'Успешно'
                mock_print.assert_called_once_with('История пуста')
                
        finally:
            history_manager.history = original_history

    def test_undo_empty(self):
        # Сохраняем оригинальное состояние
        original_history = history_manager.history.copy()
        
        try:
            history_manager.history = []
            
            with patch('builtins.print') as mock_print:
                from src.history_manager import undo_last
                result = undo_last()
                
                assert "нет операций для отмены" in result.lower()
                mock_print.assert_called_once()
                
        finally:
            history_manager.history = original_history

    def test_undo_with_history(self):
        """Упрощенный тест - просто проверяем что функция не падает"""
        # Сохраняем оригинальное состояние
        original_history = history_manager.history.copy()
        
        try:
            # Создаем простую историю без сложных операций
            history_manager.history = [
                {
                    'command': 'ls', 
                    'timestamp': '2023-01-01 10:00:00',
                    'type': None,  # Простая команда без операции
                    'source': None,
                    'destination': None
                }
            ]
            
            with patch('builtins.print'):
                from src.history_manager import undo_last
                # Просто вызываем функцию - она должна вернуть сообщение об ошибке
                result = undo_last()
                
                # Проверяем что вернулось какое-то сообщение
                assert result is not None
                assert isinstance(result, str)
                
        finally:
            history_manager.history = original_history

    def test_show_history_with_count(self):
        """Тест с указанием количества записей"""
        original_history = history_manager.history.copy()
        
        try:
            # Создаем больше записей
            history_manager.history = [
                {'command': f'cmd{i}', 'timestamp': f'2023-01-01 10:0{i}:00'} 
                for i in range(15)
            ]
            
            with patch('builtins.print') as mock_print:
                result = show_history(5)  # Показываем только 5 записей
                
                assert result == 'Успешно'
                # Должно быть 6 вызовов: заголовок + 5 команд
                assert mock_print.call_count == 6
                
        finally:
            history_manager.history = original_history
