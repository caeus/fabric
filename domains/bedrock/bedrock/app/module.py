from injector import Injector
from dataclasses import dataclass
from typing import Callable, TypeVar, Generic, Awaitable
import asyncio
from bedrock.app.app_id import create_app_id, create_app_id_router
from bedrock.config.module import base_config_module
import nest_asyncio
from bedrock.di.module import Bind, FModule, module
from bedrock.health.module import base_health_module

from ..http.module import base_http_module
import sys

T = TypeVar('T')



@dataclass
class App(Generic[T]):
    use: Callable[[Injector], Awaitable[T]]
    injector: Injector
    async def run_and_return(self):
        return await self.use(self.injector)
    async def run_forever_or_exit(self):
        try:
            await self.run_and_return()
            await asyncio.Future() # Wait forever
        except:
            sys.exit(1)


@module
def base_app_module(bind:Bind)->None:
    bind.singleton(create_app_id_router)
    bind.singleton(create_app_id)


def build_app(module: FModule | None) -> Callable[[Callable[[Injector], Awaitable[T]]], App[T]]:
    nest_asyncio.apply()
    def decorated(use: Callable[[Injector], Awaitable[T]]) -> App[T]:
        modules = [
            base_http_module,
            base_config_module,
            base_app_module,
            base_health_module,
        ]
        if module is not None:
            modules= [*modules,module]
        return App(use=use, injector=Injector(modules))
    return decorated
