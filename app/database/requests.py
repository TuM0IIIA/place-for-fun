from app.database.models import async_session
from app.database.models import User, Category, Item
from sqlalchemy import select

async def set_user(tg_id):  # def set_use(tg_id: int) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))   # ищем юзера в таблице 'User'
        # '.scalar' полноценный объект, который имеет свои поля( понятно, что вернет объект)

        if not user:  # если пользователь не найден
            session.add(User(tg_id=tg_id))  # добавляем пользователя в таблицу
            await session.commit()
            # если функция возвращает что-то, то она используется с 'await'
            # если нет , то НЕ используется
            # например '.add' НЕ используется с await:
            # def add(self,instance: object,_warn: bool = True) -> None
            # а '.commit' - используется :  (async def commit(self) -> Coroutine[Any, Any, None])


async def get_categories():
    async with async_session() as session:
        return await session.scalars(select(Category))


async def get_category_item(category_id):
    async with async_session() as session:
        return await session.scalars(select(Item).where(Item.category == category_id))
        # выбираем все Item, где item.category = category_id


async def get_item(item_id):
    async with async_session() as session:
        return await session.scalar(select(Item).where(Item.id == item_id))
        # выбираем все Item, где item.id = item_id