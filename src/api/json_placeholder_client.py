from requests import Response as RequestsResponse
from pydantic import TypeAdapter
from typing import Generic, TypeVar, Any

from src.api.api_client import APIClient
from src.models.post_model import PostModel
from src.models.user_model import UserModel

T = TypeVar('T')


class Response(Generic[T]):
    def __init__(self, raw_response: RequestsResponse, model_type: Any = None):
        self.raw = raw_response
        self.status_code = raw_response.status_code
        self.text = raw_response.text
        self._model_type = model_type
        self._data = None

    @property
    def data(self) -> T:
        if self._data is None and self._model_type is not None:
            if self.text and self.text != '{}':
                adapter = TypeAdapter(self._model_type)
                self._data = adapter.validate_json(self.text)
        return self._data

    def json(self):
        return self.raw.json()


class JsonPlaceholderClient(APIClient):
    BASE_URL = 'https://jsonplaceholder.typicode.com'

    __POSTS_ENDPOINT = '/posts'
    __USERS_ENDPOINT = '/users'

    def __init__(self):
        super().__init__(self.BASE_URL)

    def get_all_posts(self) -> Response[list[PostModel]]:
        raw_response = self.get_request(self.__POSTS_ENDPOINT)
        return Response(raw_response, model_type=list[PostModel])

    def get_post_by_id(self, post_id: int) -> Response[PostModel]:
        raw_response = self.get_request(f"{self.__POSTS_ENDPOINT}/{post_id}")
        return Response(raw_response, model_type=PostModel)

    def create_post(self, post_data: dict) -> Response[PostModel]:
        raw_response = self.post_request(self.__POSTS_ENDPOINT, new_data_json=post_data)
        return Response(raw_response, model_type=PostModel)

    def get_all_users(self) -> Response[list[UserModel]]:
        raw_response = self.get_request(self.__USERS_ENDPOINT)
        return Response(raw_response, model_type=list[UserModel])

    def get_user_by_id(self, user_id: int) -> Response[UserModel]:
        raw_response = self.get_request(f"{self.__USERS_ENDPOINT}/{user_id}")
        return Response(raw_response, model_type=UserModel)