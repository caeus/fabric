import asyncio
from bedrock.app.app_id import AppIDRouter
from bedrock.config.module import EnvConfig
from bedrock.health.router import HealthRouter
from bedrock.http.routers import Routers
import uvicorn
from fastapi import FastAPI
from ..di.module import Bind, module
from dataclasses import dataclass


@dataclass
class HttpConfig:
    port: int


class HttpEngine:
    server: uvicorn.Server
    port: int

    def __init__(self, server: uvicorn.Server, port: int):
        self.server = server
        self.port = port

@module
def base_http_module(bind: Bind):
    @bind.singleton
    def _(config:EnvConfig) -> HttpConfig:
        return HttpConfig(port=int(config["HTTP_PORT"]))

    @bind.singleton
    def _() -> FastAPI:
        return FastAPI()

    @bind.singleton
    def _(app: FastAPI,
          routers: Routers,
          app_id_router:AppIDRouter,
          health_router: HealthRouter,
          config: HttpConfig) -> uvicorn.Config:
        for router in routers:
            app.router.include_router(router)
        app.router.include_router(app_id_router)
        app.router.include_router(health_router)
        return uvicorn.Config(app, port=config.port)

    async def start_engine(server: uvicorn.Server)->HttpEngine:
        asyncio.create_task(server.serve(None))
        async def await_started():
            while server.started is not True:
                await asyncio.sleep(0.1)
        await asyncio.create_task(await_started())
        ## Ugly as fuck, but it works!
        return HttpEngine(server,server.servers[0].sockets[0].getsockname()[1])
        

    @bind.singleton
    def _(config: uvicorn.Config) -> HttpEngine:
        server = uvicorn.Server(config)
        return asyncio.run(start_engine(server))
