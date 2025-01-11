import datetime

from pydantic import BaseModel, ConfigDict, Field


class BaseSerializer(BaseModel):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)


class CreateAuthorRequest(BaseSerializer):
    name: str
    age: int


class CreateBookRequest(BaseSerializer):
    title: str
    rating: int
    author_id: int = Field(alias="authorId")


class SerializedAuthor(CreateAuthorRequest):
    id: int

    time_created: datetime.datetime = Field(..., alias="timeCreated")
    time_updated: datetime.datetime | None = Field(None, alias="timeUpdated")


class SerializedBook(CreateBookRequest):
    id: int

    author: SerializedAuthor

    time_created: datetime.datetime = Field(..., alias="timeCreated")
    time_updated: datetime.datetime | None = Field(None, alias="timeUpdated")
