from typing import Any

import datetime
import sqlite3
from collections.abc import AsyncGenerator, Generator

import pytest
import sqlalchemy as sa
from fastapi import Request
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, SQLModel, create_engine

from {{ cookiecutter.project_slug }} import crud, models, settings
from {{ cookiecutter.project_slug }}.api.deps import get_db
from {{ cookiecutter.project_slug }}.core import security
from {{ cookiecutter.project_slug }}.core.app import app
from {{ cookiecutter.project_slug }}.db.init_db import init_initial_data

# Set up the databsase
db_url = "sqlite:///:memory:"
engine = create_engine(
    db_url,
    echo=False,
    connect_args={"check_same_thread": False},
    pool_pre_ping=True,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=Session)
SQLModel.metadata.drop_all(bind=engine)
SQLModel.metadata.create_all(bind=engine)


# These two event listeners are only needed for sqlite for proper
# SAVEPOINT / nested transaction support. Other databases like postgres
# don't need them.
# From: https://docs.sqlalchemy.org/en/14/dialects/sqlite.html#serializable-isolation-savepoints-transactional-ddl
@sa.event.listens_for(engine, "connect")  # type: ignore
def do_connect(dbapi_connection: Any, connection_record: Any) -> None:
    # disable pysqlite's emitting of the BEGIN statement entirely.
    # also stops it from emitting COMMIT before any DDL.
    dbapi_connection.isolation_level = None


@sa.event.listens_for(engine, "begin")  # type: ignore
def do_begin(conn: Any) -> None:
    # emit our own BEGIN
    conn.exec_driver_sql("BEGIN")


@pytest.fixture(name="db")
async def fixture_db() -> AsyncGenerator[Session, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    # Begin a nested transaction (using SAVEPOINT).
    nested = connection.begin_nested()
    await init_initial_data(db=session)

    # If the application code calls session.commit, it will end the nested
    # transaction. Need to start a new one when that happens.
    @sa.event.listens_for(session, "after_transaction_end")  # type: ignore
    def end_savepoint(session: Any, transaction: Any) -> None:  # type: ignore
        nonlocal nested
        if not nested.is_active:
            nested = connection.begin_nested()

    yield session

    # Rollback the overall transaction, restoring the state before the test ran.
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(name="client")
async def fixture_client(db: Session) -> AsyncGenerator[TestClient, None]:
    """
    Fixture that creates a test client with the database session override.

    Args:
        db (Session): database session.

    Yields:
        TestClient: test client with database session override.
    """

    def override_get_db() -> Generator[Session, None, None]:
        yield db

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    del app.dependency_overrides[get_db]


@pytest.fixture(name="db_with_user")
async def fixture_db_with_user(db: Session) -> Session:
    """
    Fixture that creates an example user in the test database.

    Args:
        db (Session): database session.

    Returns:
        Session: database session with example user.
    """
    user_hashed_password = security.get_password_hash("test_password")
    user_create = models.UserCreate(
        username="test_user", email="test@example.com", hashed_password=user_hashed_password
    )
    await crud.user.create(in_obj=user_create, db=db)
    return db


@pytest.fixture(name="db_with_{{ cookiecutter.first_model }}s")
async def fixture_db_with_{{ cookiecutter.first_model }}s(db_with_user: Session) -> Session:
    """
    Fixture that creates example {{ cookiecutter.first_model }}s for the example source in the test database.

    Args:
        db_with_user (Session): database session.

    Returns:
        Session: database session with example {{ cookiecutter.first_model }}s.

    Returns the following {{ cookiecutter.first_model }}_ids:
        - 5kwf8hFn
        - R6iBBN3J
        - fEpPZMry
    """
    owner = await crud.user.get(db=db_with_user, username="test_user")
    {{ cookiecutter.first_model }}s = []
    for i in range(3):
        {{ cookiecutter.first_model }}_create = models.{{ cookiecutter.first_model|title }}Create(
            id=f"{i}{i}{i}{i}{i}{i}{i}{i}",
            uploader="test",
            uploader_id="test_uploader_id",
            title=f"Example {{ cookiecutter.first_model }} {i}",
            description=f"This is example {{ cookiecutter.first_model }} {i}.",
            duration=417,
            thumbnail="https://sp.rmbl.ws/s8d/R/0_FRh.oq1b.jpg",
            url=f"https://rumble.com/{i}{i}{i}{i}/test.html",
            added_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
        )
        {{ cookiecutter.first_model }} = await crud.{{ cookiecutter.first_model }}.create_with_owner_id(
            in_obj={{ cookiecutter.first_model }}_create, db=db_with_user, owner_id=owner.id
        )
        {{ cookiecutter.first_model }}s.append({{ cookiecutter.first_model }})
    return db_with_user


@pytest.fixture(name="superuser_token_headers")
def superuser_token_headers(db_with_user: Session, client: TestClient) -> dict[str, str]:
    """
    Fixture that returns the headers for a superuser.

    Args:
        db_with_user (Session): database session.
        client (TestClient): test client.

    Returns:
        dict[str, str]: headers for a superuser.
    """
    login_data = {
        "username": settings.FIRST_SUPERUSER_USERNAME,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = client.post(f"{settings.API_V1_PREFIX}/login/access-token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers


@pytest.fixture(name="normal_user_token_headers")
def normal_user_token_headers(client: TestClient) -> dict[str, str]:
    """
    Fixture that returns the headers for a normal user.

    Args:
        client (TestClient): test client.

    Returns:
        dict[str, str]: headers for a normal user.
    """
    login_data = {
        "username": "test_user",
        "password": "test_password",
    }
    r = client.post(f"{settings.API_V1_PREFIX}/login/access-token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers


@pytest.fixture(name="test_request")
def fixture_request() -> Request:
    """
    Fixture that returns a request object.

    Returns:
        Request: request object.
    """
    return Request(scope={"type": "http", "method": "GET", "path": "/"})