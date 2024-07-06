import pytest
import pytest_asyncio
import asyncio
from typing import Generator, AsyncGenerator

from async_asgi_testclient import TestClient

from main import app


# DATABASE_URL = str(settings.DATABASE_URL)
# engine = create_engine(DATABASE_URL)
# Session = sessionmaker(bind=engine)


# @pytest.fixture(autouse=True)
# def setup_db_table():
#     Base.metadata.create_all(engine)
#     yield
#     Base.metadata.drop_all(engine)


# @pytest.fixture(autouse=False)
# async def setup_db(setup_db_table):
#     with Session() as session:
#         with session.begin():
#             admin = User(
#                 telegram_id=0,
#                 username="admin",
#                 inviter_id=0,
#             )

#             session.add(admin)
#             session.commit()


@pytest.fixture(autouse=True, scope="session")
def run_migrations() -> None:
    import os

    print("running migrations..")
    os.system("alembic upgrade head")
    yield
    os.system("alembic downgrade base")


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def client() -> AsyncGenerator[TestClient, None]:
    host, port = "127.0.0.1", "9000"
    scope = {"client": (host, port)}

    async with TestClient(app, scope=scope) as client:
        yield client
