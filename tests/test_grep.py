import pytest
from unittest.mock import Mock, patch, MagicMock
from src.grep import grep

class TestGrep:
    def test_nonexistent_path(self):
        with patch('os.path.exists') as mock_exists:
            mock_exists.return_value = False
            with pytest.raises(FileNotFoundError):
                grep('pattern', 'nonexistent.txt')

    def test_pattern_match(self):
        with patch('os.path.exists') as mock_exists, \
             patch('os.path.isfile') as mock_isfile, \
             patch('builtins.open') as mock_open, \
             patch('builtins.print') as mock_print:
            
            mock_exists.return_value = True
            mock_isfile.return_value = True
            
            mock_file = MagicMock()
            mock_file.__enter__.return_value = mock_file
            mock_file.__iter__.return_value = ['first line\n', 'match here\n', 'last line\n']
            mock_open.return_value = mock_file
            
            result = grep('match', 'test.txt')
            
            assert result == 'Успешно'
            mock_print.assert_called()
            calls = [call[0][0] for call in mock_print.call_args_list]
            assert any('match here' in str(call) for call in calls)

    def test_no_matches(self):
        with patch('os.path.exists') as mock_exists, \
             patch('os.path.isfile') as mock_isfile, \
             patch('builtins.open') as mock_open, \
             patch('builtins.print') as mock_print:
            
            mock_exists.return_value = True
            mock_isfile.return_value = True
            
            mock_file = MagicMock()
            mock_file.__enter__.return_value = mock_file
            mock_file.__iter__.return_value = ['hello\n', 'world\n']
            mock_open.return_value = mock_file
            
            result = grep('nonexistent', 'test.txt')
            
            assert result == 'Успешно'
            mock_print.assert_called_once_with('Совпадений не найдено')

    def test_recursive_search(self):
        with patch('os.path.exists') as mock_exists, \
             patch('os.path.isdir') as mock_isdir, \
             patch('os.walk') as mock_walk, \
             patch('builtins.open') as mock_open, \
             patch('builtins.print') as mock_print:
            
            mock_exists.return_value = True
            mock_isdir.return_value = True
            mock_walk.return_value = [
                ('project', ['subdir'], ['file1.txt']),
                ('project/subdir', [], ['file2.txt'])
            ]
            
            mock_file = MagicMock()
            mock_file.__enter__.return_value = mock_file
            mock_file.__iter__.return_value = ['find me\n']
            mock_open.return_value = mock_file
            
            result = grep('find', 'project', recursive=True)
            
            assert result == 'Успешно'
            assert mock_print.call_count == 2

    def test_ignore_case(self):
        with patch('os.path.exists') as mock_exists, \
             patch('os.path.isfile') as mock_isfile, \
             patch('builtins.open') as mock_open, \
             patch('builtins.print') as mock_print:
            
            mock_exists.return_value = True
            mock_isfile.return_value = True
            
            mock_file = MagicMock()
            mock_file.__enter__.return_value = mock_file
            mock_file.__iter__.return_value = ['CaseSensitive\n']
            mock_open.return_value = mock_file
            
            result = grep('casesensitive', 'test.txt', ignore_case=True)
            
            assert result == 'Успешно'
            mock_print.assert_called_once()

    def test_multiple_matches(self):
        with patch('os.path.exists') as mock_exists, \
             patch('os.path.isfile') as mock_isfile, \
             patch('builtins.open') as mock_open, \
             patch('builtins.print') as mock_print:
            
            mock_exists.return_value = True
            mock_isfile.return_value = True
            
            mock_file = MagicMock()
            mock_file.__enter__.return_value = mock_file
            mock_file.__iter__.return_value = ['match first\n', 'no match\n', 'match second\n']
            mock_open.return_value = mock_file
            
            result = grep('match', 'test.txt')
            
            assert result == 'Успешно'
            assert mock_print.call_count == 2

    def test_regex_pattern(self):
        with patch('os.path.exists') as mock_exists, \
             patch('os.path.isfile') as mock_isfile, \
             patch('builtins.open') as mock_open, \
             patch('builtins.print') as mock_print:
            
            mock_exists.return_value = True
            mock_isfile.return_value = True
            
            mock_file = MagicMock()
            mock_file.__enter__.return_value = mock_file
            mock_file.__iter__.return_value = ['123-45-6789\n', 'phone: 555-2288\n']
            mock_open.return_value = mock_file
            
            grep(r'\d{3}-\d{2}-\d{4}', 'data.txt')
            
            mock_print.assert_called_once()
            call_args = mock_print.call_args[0][0]
            assert '123-45-6789' in call_args

    def test_multiple_files(self):
        with patch('os.path.exists') as mock_exists, \
             patch('os.path.isdir') as mock_isdir, \
             patch('os.walk') as mock_walk, \
             patch('builtins.open') as mock_open, \
             patch('builtins.print') as mock_print:
            
            mock_exists.return_value = True
            mock_isdir.return_value = True
            mock_walk.return_value = [
                ('.', [], ['file1.txt', 'file2.txt', 'file3.txt'])
            ]
            
            def open_side_effect(path, *args, **kwargs):
                mock_file = MagicMock()
                mock_file.__enter__.return_value = mock_file
                if 'file1' in str(path):
                    mock_file.__iter__.return_value = ['hello world\n']
                elif 'file2' in path:
                    mock_file.__iter__.return_value = ['hello there\n']
                else:
                    mock_file.__iter__.return_value = ['goodbye\n']
                return mock_file
            
            mock_open.side_effect = open_side_effect
            
            grep('hello', '.', recursive=True)
            
            assert mock_print.call_count == 2
