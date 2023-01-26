from unittest.mock import MagicMock, patch

import pytest
from sqlmodel import Session

from {{ cookiecutter.project_slug }} import crud, models


async def test_create_item(db_with_user: Session) -> None:
    """
    Test creating a new item with an owner.
    """
    owner = await crud.user.get(db=db_with_user, username="test_user")
    {{ cookiecutter.first_model }}_create = models.{{ cookiecutter.first_model | title }}Create(
        id="12345678",
        uploader="test",
        uploader_id="test_uploader_id",
        title="Example {{ cookiecutter.first_model | title }} AAA",
        description="This is example {{ cookiecutter.first_model }} AAA.",
        duration=417,
        thumbnail="https://sp.rmbl.ws/s8d/R/0_FRh.oq1b.jpg",
        url="https://rumble.com/AAA/test.html",
    )
    {{ cookiecutter.first_model }} = await crud.{{ cookiecutter.first_model }}.create_with_owner_id(
        db=db_with_user, in_obj={{ cookiecutter.first_model }}_create, owner_id=owner.id
    )
    assert {{ cookiecutter.first_model }}.title == "Example {{ cookiecutter.first_model | title }} AAA"
    assert {{ cookiecutter.first_model }}.description == "This is example {{ cookiecutter.first_model }} AAA."
    assert {{ cookiecutter.first_model }}.owner_id == owner.id


async def test_get_item(db_with_{{ cookiecutter.first_model }}s: Session) -> None:
    """
    Test getting an item by id.
    """
    db_{{ cookiecutter.first_model }} = await crud.{{ cookiecutter.first_model }}.get(db=db_with_{{ cookiecutter.first_model }}s, id="00000000")
    assert db_{{ cookiecutter.first_model }}
    assert db_{{ cookiecutter.first_model }}.id == "00000000"
    assert db_{{ cookiecutter.first_model }}.title == "Example {{ cookiecutter.first_model | title }} 0"
    assert db_{{ cookiecutter.first_model }}.description == "This is example {{ cookiecutter.first_model }} 0."
    assert db_{{ cookiecutter.first_model }}.owner_id == "ZbFPeSXW"


async def test_update_item(db_with_{{ cookiecutter.first_model }}s: Session) -> None:
    """
    Test updating an item.
    """
    db_{{ cookiecutter.first_model }} = await crud.{{ cookiecutter.first_model }}.get(db=db_with_{{ cookiecutter.first_model }}s, id="00000000")
    db_{{ cookiecutter.first_model }}_update = models.{{ cookiecutter.first_model | title }}Update(description="New Description")
    updated_{{ cookiecutter.first_model }} = await crud.{{ cookiecutter.first_model }}.update(
        db=db_with_{{ cookiecutter.first_model }}s, id="00000000", in_obj=db_{{ cookiecutter.first_model }}_update
    )
    assert db_{{ cookiecutter.first_model }}.id == updated_{{ cookiecutter.first_model }}.id
    assert db_{{ cookiecutter.first_model }}.title == updated_{{ cookiecutter.first_model }}.title
    assert updated_{{ cookiecutter.first_model }}.description == "New Description"
    assert db_{{ cookiecutter.first_model }}.owner_id == updated_{{ cookiecutter.first_model }}.owner_id


async def test_update_item_without_filter(db_with_{{ cookiecutter.first_model }}s: Session) -> None:
    """
    Test updating an item without a filter.
    """
    await crud.{{ cookiecutter.first_model }}.get(db=db_with_{{ cookiecutter.first_model }}s, id="00000000")
    db_{{ cookiecutter.first_model }}_update = models.{{ cookiecutter.first_model | title }}Update(description="New Description")
    with pytest.raises(ValueError):
        await crud.{{ cookiecutter.first_model }}.update(db=db_with_{{ cookiecutter.first_model }}s, in_obj=db_{{ cookiecutter.first_model }}_update)


async def test_delete_item(db_with_{{ cookiecutter.first_model }}s: Session) -> None:
    """
    Test deleting an item.
    """
    await crud.{{ cookiecutter.first_model }}.remove(db=db_with_{{ cookiecutter.first_model }}s, id="00000000")
    with pytest.raises(crud.RecordNotFoundError):
        await crud.{{ cookiecutter.first_model }}.get(db=db_with_{{ cookiecutter.first_model }}s, id="00000000")


async def test_delete_item_delete_error(db_with_{{ cookiecutter.first_model }}s: Session, mocker: MagicMock) -> None:
    """
    Test deleting an item with a delete error.
    """
    mocker.patch("{{ cookiecutter.project_slug }}.crud.{{ cookiecutter.first_model }}.get", return_value=None)
    with pytest.raises(crud.DeleteError):
        await crud.{{ cookiecutter.first_model }}.remove(db=db_with_{{ cookiecutter.first_model }}s, id="00000001")
