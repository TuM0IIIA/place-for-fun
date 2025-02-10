from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')  # создали БД
async_session=async_sessionmaker(engine)  # подключаемся к БД

#  создадим класс, который будет управлять всеми дочерними классами
class Base(AsyncAttrs,DeclarativeBase):  # создаем класс 'Base' который является дочерним к 'AsyncAttrs,DeclarativeBase'

    pass

class User(Base):  # все остальные будут дочерними к 'Base'
    __tablename__ = 'users'  # мн.число т.к. информация будет о множестве пользователей, а класс - один(модель одна)

    id: Mapped[int] = mapped_column(primary_key=True)  # идентификатор, который используем в своем боте
    tg_id = mapped_column(BigInteger)  # идентификатор - пользователя

class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25))  # 'String(25)' - ограничение символов

class Item(Base):
    __tablename__ = 'items'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25))
    description: Mapped[str] = mapped_column(String(120))
    price: Mapped[int] = mapped_column()
    category: Mapped[int] = mapped_column(ForeignKey('categories.id'))


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

