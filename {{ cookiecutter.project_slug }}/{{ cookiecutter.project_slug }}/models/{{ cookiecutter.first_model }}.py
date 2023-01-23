from typing import TYPE_CHECKING, Any

import datetime

from pydantic import root_validator
from sqlmodel import Field, Relationship, SQLModel

from {{ cookiecutter.project_slug }}.core.uuid import generate_uuid_from_url

from .common import TimestampModel

if TYPE_CHECKING:
    from .user import User  # pragma: no cover


class {{ cookiecutter.first_model|title }}Base(TimestampModel, SQLModel):
    id: str = Field(default=None, primary_key=True, nullable=False)
    uploader: str = Field(default=None)
    uploader_id: str = Field(default=None)
    title: str = Field(default=None)
    description: str = Field(default=None)
    duration: int = Field(default=None)
    thumbnail: str = Field(default=None)
    url: str = Field(default=None)
    # added_at: datetime.datetime = Field(default=None)
    owner_id: str = Field(foreign_key="user.id", nullable=False, default=None)
    # updated_at: datetime.datetime = Field(default=None)


class {{ cookiecutter.first_model }}({{ cookiecutter.first_model|title }}Base, table=True):
    owner: "User" = Relationship(back_populates="{{ cookiecutter.first_model }}s")


class {{ cookiecutter.first_model|title }}Create({{ cookiecutter.first_model|title }}Base):
    @root_validator(pre=True)
    @classmethod
    def set_pre_validation_defaults(cls, values: dict[str, Any]) -> dict[str, Any]:
        sanitized_url = values["url"]
        {{ cookiecutter.first_model }}_uuid = generate_uuid_from_url(url=sanitized_url)
        return {
            **values,
            "url": sanitized_url,
            "id": values.get("id", {{ cookiecutter.first_model }}_uuid),
            "updated_at": datetime.datetime.now(tz=datetime.timezone.utc),
        }


class {{ cookiecutter.first_model|title }}Update({{ cookiecutter.first_model|title }}Base):
    pass


class {{ cookiecutter.first_model|title }}Read({{ cookiecutter.first_model|title }}Base):
    pass
