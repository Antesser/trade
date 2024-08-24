from conftest import async_session_maker, client
from sqlalchemy import insert, select

from auth.models import role


async def test_add_role():
    async with async_session_maker() as session:
        stmt = insert(role).values(id=1, name="admin", permissions=None)
        await session.execute(stmt)
        await session.commit()

        query = select(role)
        result = await session.execute(query)
        assert result.all() == [(1, 'admin', None)]

def test_register():
    response = client.post("/auth/register", json={
        "email": "3user@example.com",
        "password": "password",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "username": "string",
        "role_id": 1
    })

    assert response.status_code == 201
