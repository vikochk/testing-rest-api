from pydantic import BaseModel
from typing import Optional

from src.models.user_model import UserModel


class PostTestParams(BaseModel):
    status_code: int
    id: Optional[int] = None
    expected_user_id: Optional[int] = None


class UserTestParams(BaseModel):
    status_code: int
    expected_user_id: int
    expected_data: Optional[UserModel] = None