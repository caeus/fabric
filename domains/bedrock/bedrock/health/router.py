


import asyncio
from dataclasses import dataclass
from typing import Iterator, List, Protocol, Union
from fastapi import APIRouter

from bedrock.http.response import Response



@dataclass
class Ok:
    name:str
    ok = True

@dataclass
class Error:
    name:str
    ok = False
    message:str

Result = Union[Error,Ok]
    
class Healthcheck:
    async def run(self)->Result:
        raise BaseException("")
        pass


class Healthchecks(Protocol):
    def __iter__(self)->Iterator[Healthcheck]:
        pass




class HealthRouter(APIRouter):
    pass

def create_health_router(healthchecks:Healthchecks)->HealthRouter:
    router = HealthRouter()
    @router.get("/healthcheck")
    async def _():
        return Response[List[Result]](await asyncio.gather(
            *[hc.run() for hc in healthchecks]
        ))

    return router