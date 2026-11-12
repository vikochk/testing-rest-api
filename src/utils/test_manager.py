from pathlib import Path
from typing import TypeVar, Any
from pydantic import ValidationError, TypeAdapter

from src.utils.logger import Logger

T = TypeVar('T')


class TestDataProvider:
    __test__ = False

    POSTS_DATA_FILE = "posts_data.json"
    USERS_DATA_FILE = "users_data.json"

    @staticmethod
    def get_test_data(file_name: str, data_type: Any) -> T:
        project_root = Path('tests/resources')
        file_path = project_root / file_name

        if not file_path.is_file():
            Logger.error_and_throw(
                f'Файл с тестовыми данными не был найден по пути "{file_path}"', 
                FileNotFoundError
            )
        
        try:
            raw_json = file_path.read_text(encoding='utf-8')
            adapter = TypeAdapter(data_type)
            return adapter.validate_json(raw_json)
        except (ValidationError, ValueError) as e:
            Logger.error_and_throw(
                f'Неверная структура файла с тестовыми данными: {e}', ValueError
            )