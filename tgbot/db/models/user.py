from loguru import logger
from sqlalchemy import (Column, String, sql, DateTime, func, select, BigInteger)

from tgbot.db.alchemy import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True)
    username = Column(String(64), nullable=True)
    create_date = Column(DateTime, server_default=func.now())

    # required in order to access columns with server defaults
    # or SQL expression defaults, subsequent to a flush, without
    # triggering an expired load
    __mapper_args__ = {"eager_defaults": True}

    @classmethod
    async def get_or_create(cls, session, user):
        stmt = select(cls).where(cls.id == user.id)
        if result := (await session.execute(stmt)).scalars().first():
            return result
        else:
            session.add(User(id=user.id, username=user.username))
            result = (await session.execute(stmt)).scalars().first()
            return result

    @classmethod
    async def count(cls, session) -> int:
        stmt = func.count(select(cls.id))
        result = (await session.execute(stmt)).scalar()
        return result
