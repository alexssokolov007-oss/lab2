import pytest
from unittest.mock import Mock, patch
from src.mv import mv


class TestMvSimple:
    def test_nonexistent_source(self):
        """Перемещение несуществующего файла"""
        with pytest.raises(FileNotFoundError):
            mv('nonexistent.txt', 'destination.txt')

    def test_rename_file_basic(self, tmp_path, capsys):
        """Переименование файла"""
        old_file = tmp_path / "old_name.txt"
        old_file.write_text("content")
        new_file = tmp_path / "new_name.txt"
        
        result = mv(str(old_file), str(new_file))
        
        assert result == 'Успешно'
        assert not old_file.exists()
        assert new_file.exists()
        assert new_file.read_text() == "content"
        captured = capsys.readouterr()
        assert 'Успешно' in captured.out

    def test_move_dir_basic(self, tmp_path, capsys):
        """Перемещение директории"""
        old_dir = tmp_path / "old_dir"
        old_dir.mkdir()
        (old_dir / "file.txt").write_text("content")
        
        new_dir = tmp_path / "new_dir"
        
        result = mv(str(old_dir), str(new_dir))
        
        assert result == 'Успешно'
        assert not old_dir.exists()
        assert new_dir.exists()
        assert (new_dir / "file.txt").exists()
        captured = capsys.readouterr()
        assert 'Успешно' in captured.out

    def test_overwrite_file_basic(self, tmp_path, capsys):
        """Перезапись файла"""
        new_file = tmp_path / "new.txt"
        new_file.write_text("new content")
        
        old_file = tmp_path / "old.txt" 
        old_file.write_text("old content")
        
        result = mv(str(new_file), str(old_file))
        
        assert result == 'Успешно'
        assert not new_file.exists()
        assert old_file.exists()
        assert old_file.read_text() == "new content"
        captured = capsys.readouterr()
        assert 'Успешно' in captured.out