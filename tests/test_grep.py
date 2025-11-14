import pytest
from unittest.mock import Mock, patch
from src.grep import grep


def test_nonexistent_path():
    """Несуществующий путь"""
    with pytest.raises(FileNotFoundError):
        grep('pattern', 'nonexistent.txt')


def test_pattern_match(tmp_path, capsys):
    """Поиск совпадения в файле"""
    test_file = tmp_path / "test.txt"
    test_file.write_text("first line\nmatch here\nlast line", encoding='utf-8')
    
    result = grep('match', str(test_file))
    
    assert result == 'Успешно'
    captured = capsys.readouterr()
    assert 'match here' in captured.out


def test_no_matches(tmp_path, capsys):
    """Отсутствие совпадений"""
    test_file = tmp_path / "test.txt"
    test_file.write_text("hello\nworld", encoding='utf-8')
    
    result = grep('nonexistent', str(test_file))
    
    assert result == 'Успешно'
    captured = capsys.readouterr()
    assert 'Совпадений не найдено' in captured.out


def test_recursive_search(tmp_path, capsys):
    """Рекурсивный поиск"""
    subdir = tmp_path / "subdir"
    subdir.mkdir()
    (tmp_path / "file1.txt").write_text("find me", encoding='utf-8')
    (subdir / "file2.txt").write_text("find me too", encoding='utf-8')
    
    result = grep('find', str(tmp_path), recursive=True)
    
    assert result == 'Успешно'
    captured = capsys.readouterr()
    assert 'find me' in captured.out
    assert 'find me too' in captured.out