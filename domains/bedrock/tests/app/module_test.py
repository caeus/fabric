
import aiohttp
import pytest
from bedrock.app.app_id import AppIDRouter
from bedrock.app.module import build_app, T, App
from injector import Injector
import uvicorn
import typing
from fastapi import FastAPI
from bedrock.config.module import EnvConfig
from bedrock.di.module import Bind, module
from bedrock.health.router import Healthchecks

from bedrock.http.module import HttpConfig, HttpEngine
from bedrock.http.routers import Routers
R = typing.TypeVar('R')


def assert_isinstance(app: App[R], type: typing.Type[T]) -> T:
    injectable = app.injector.get(type)
    assert isinstance(injectable, type)
    return injectable

@pytest.mark.asyncio
async def test_build_application():
    @module
    def _test_module(bind: Bind):
        @bind.singleton
        def _() -> EnvConfig:
            return EnvConfig({
                "APP_NAME":"test",
                "APP_ENV":"test",
                "APP_VERSION":"0.1-RC",
                "HTTP_PORT":"0"
            })
        @bind.singleton
        def _() -> Routers:
            return []
        @bind.singleton
        def _() -> Healthchecks:
            return []

    @build_app(_test_module)
    async def app(_: Injector) -> None:
        pass

    assert isinstance(app, App)
    assert_isinstance(app, HttpConfig)
    assert_isinstance(app, FastAPI)
    assert_isinstance(app, uvicorn.Config)
    assert_isinstance(app, AppIDRouter)
    engine = assert_isinstance(app, HttpEngine)
    assert engine.port is not 0
    #await asyncio.sleep(60)
    print("before making request")
    print(f"http://localhost:{engine.port}/asd")
    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://localhost:{engine.port}/version") as res:
            body = await res.json()
            pass
            print("after request")
            print("after bofdy")
            print(body)
            print(body)
            print(body)
            print(body)
    #print(await engine.portugly())
    await app.run_and_return()





   