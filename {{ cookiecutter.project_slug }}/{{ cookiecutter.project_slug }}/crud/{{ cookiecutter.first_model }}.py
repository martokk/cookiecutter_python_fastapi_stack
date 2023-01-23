from sqlmodel import Session

from {{ cookiecutter.project_slug }} import models

from .base import BaseCRUD


class {{ cookiecutter.first_model|title }}CRUD(BaseCRUD[models.{{ cookiecutter.first_model }}, models.{{ cookiecutter.first_model|title }}Create, models.{{ cookiecutter.first_model|title }}Update]):
    async def create_with_owner_id(
        self, db: Session, *, in_obj: models.{{ cookiecutter.first_model|title }}Create, owner_id: str
    ) -> models.{{ cookiecutter.first_model }}:
        """
        Create a new {{ cookiecutter.first_model }} with an owner_id.

        Args:
            db (Session): The database session.
            in_obj (models.{{ cookiecutter.first_model|title }}Create): The {{ cookiecutter.first_model }} to create.
            owner_id (str): The owner_id to set on the {{ cookiecutter.first_model }}.

        Returns:
            models.{{ cookiecutter.first_model }}: The created {{ cookiecutter.first_model }}.
        """
        in_obj.owner_id = owner_id
        return await self.create(db, in_obj=in_obj)

    async def get_multi_by_owner_id(
        self, db: Session, *, owner_id: str, skip: int = 0, limit: int = 100
    ) -> list[models.{{ cookiecutter.first_model }}]:
        """
        Retrieve multiple {{ cookiecutter.first_model }}s by owner_id.

        Args:
            db (Session): The database session.
            owner_id (str): The owner_id to filter by.
            skip (int): The number of rows to skip. Defaults to 0.
            limit (int): The maximum number of rows to return. Defaults to 100.

        Returns:
            list[models.{{ cookiecutter.first_model }}]: A list of {{ cookiecutter.first_model }}s that match the given criteria.
        """
        return await self.get_multi(db=db, owner_id=owner_id, skip=skip, limit=limit)


{{ cookiecutter.first_model }} = {{ cookiecutter.first_model|title }}CRUD(models.{{ cookiecutter.first_model }})
