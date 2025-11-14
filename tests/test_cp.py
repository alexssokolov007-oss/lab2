import pytest
from unittest.mock import Mock, patch
from src.cp import cp


def test_nonexistent_source():
    """Попытка копирования несуществующего файла/директории"""
    with pytest.raises(FileNotFoundError):
        cp('nonexistent.txt', 'destination.txt')


def test_copy_file(tmp_path, capsys):
    """Успешное копирование обычного файла"""
    src_file = tmp_path / "source.txt"
    src_file.write_text("test content")
    dst_file = tmp_path / "dest.txt"
    
    result = cp(str(src_file), str(dst_file))
    
    assert result == 'Успешно'
    assert dst_file.exists()
    assert dst_file.read_text() == "test content"
    captured = capsys.readouterr()
    assert 'Успешно' in captured.out


def test_copy_dir_without_recursive(tmp_path):
    """Попытка копирования директории без флага -r"""
    src_dir = tmp_path / "source_dir"
    src_dir.mkdir()
    
    with pytest.raises(NotADirectoryError, match='Для копирования директорий используйте флаг -r'):
        cp(str(src_dir), str(tmp_path / "dest_dir"))


def test_copy_dir_with_recursive(tmp_path, capsys):
    """Успешное рекурсивное копирование директории с флагом -r"""
    src_dir = tmp_path / "source_dir"
    src_dir.mkdir()
    (src_dir / "file1.txt").write_text("content1")
    (src_dir / "file2.txt").write_text("content2")
    
    dst_dir = tmp_path / "dest_dir"
    
    result = cp(str(src_dir), str(dst_dir), recursive=True)
    
    assert result == 'Успешно'
    assert dst_dir.exists()
    assert (dst_dir / "file1.txt").exists()
    assert (dst_dir / "file2.txt").exists()
    captured = capsys.readouterr()
    assert 'Успешно' in captured.out


def test_self_copy(tmp_path):
    """Попытка копирования директории в саму себя"""
    src_dir = tmp_path / "source_dir"
    src_dir.mkdir()
    
    with pytest.raises(ValueError, match='Нельзя копировать директорию в саму себя'):
        cp(str(src_dir), str(src_dir / "subdir"), recursive=True)