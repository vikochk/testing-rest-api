from pydantic import BaseModel, Field


class GeoModel(BaseModel):
    lat: float
    lng: float


class AddressModel(BaseModel):
    street: str
    suite: str
    city: str
    zipcode: str
    geo: GeoModel 


class CompanyModel(BaseModel):
    name: str
    catch_phrase: str = Field(..., alias='catchPhrase')
    bs: str


class UserModel(BaseModel):
    id: int
    name: str
    username: str
    email: str
    address: AddressModel
    phone: str
    website: str
    company: CompanyModel