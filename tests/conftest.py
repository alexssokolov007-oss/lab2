import pytest

@pytest.fixture
def mock_print(mocker):
    return mocker.patch('builtins.print')

@pytest.fixture
def mock_input(mocker):
    return mocker.patch('builtins.input')

@pytest.fixture
def mock_path(mocker):
    return mocker.patch('pathlib.Path')

@pytest.fixture
def mock_os(mocker):
    return mocker.patch('os')

@pytest.fixture
def mock_open(mocker):
    return mocker.patch('builtins.open')

@pytest.fixture
def mock_shutil(mocker):
    return mocker.patch('shutil')