import os
from pathlib import Path

import pytest
import randname
import randname.database
import randname.error


@pytest.fixture
def database_path():
    _THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    return Path() / _THIS_FOLDER / "test_data"


@pytest.fixture
def database(database_path):
    return randname.database.Database(database_path)


def test_database_init(database_path):
    path_to_database = database_path
    database = randname.database.Database(path_to_database)
    assert database.path == path_to_database


def test_full_database_init():
    _THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    path_to_full_database = Path() / _THIS_FOLDER / "../full_database"
    full_database = randname.database.Database(path_to_full_database)
    assert full_database.path == path_to_full_database


def test_invalid_database_directory():
    non_existing_path_to_database = "./non_existing_directory"
    database = randname.database.Database(non_existing_path_to_database)
    with pytest.raises(randname.error.DirectoryDoesNotExist):
        database.validate()


def test_validate():
    ...
