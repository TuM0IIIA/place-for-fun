from aiogram import  BaseMiddleware
from aiogram.types import TelegramObject
from typing import Callable, Dict, Any, Awaitable



class SomeMiddleware(BaseMiddleware): # наш класс дочерний к BaseMiddleware
    async def __call__(self, # метод __call__ принимает в себя параметры :
                       handler: Callable[[TelegramObject, Dict[str, Any]],  # сам обработчик
                       Awaitable[Any]],
                       event: TelegramObject,  # тип объекта
                       data: Dict[str, Any]) -> Any:  # дополнительная информация
        print('\nДействия ДО обработчика\n')  #

        # что будет делать бот ???????????????

        results = await handler(event, data)  # handler - обработчик , который выполняется
        print('\nДействия ПОСЛЕ обработчика\n')
        return results  # результат обработчика, который мы возвращаем


