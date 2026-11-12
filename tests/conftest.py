import pytest

from src.api.json_placeholder_client import JsonPlaceholderClient
from src.models.test_data_model import PostTestParams, UserTestParams
from src.utils.test_manager import TestDataProvider


@pytest.fixture(scope="session")
def api_client():
    return JsonPlaceholderClient()

@pytest.fixture(scope="session")
def posts_data():
    return TestDataProvider.get_test_data(
        TestDataProvider.POSTS_DATA_FILE, dict[str, PostTestParams]
    )

@pytest.fixture(scope="session")
def users_data():
    return TestDataProvider.get_test_data(
        TestDataProvider.USERS_DATA_FILE, dict[str, UserTestParams]
    )