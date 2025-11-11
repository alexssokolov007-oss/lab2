import pytest
from pathlib import Path
from unittest.mock import Mock, patch


@pytest.fixture
def mock_cwd():
    """Фикстура для мока текущей директории"""
    return Path("/test/cwd")


@pytest.fixture
def mock_env():
    """Фикстура для мока окружения"""
    return {}


@pytest.fixture
def ls_instance():
    """Фикстура для экземпляра команды ls"""
    from src.commands.builtin_ls import Ls
    return Ls()
