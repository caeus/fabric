
from typing import Iterator, Protocol

from fastapi import APIRouter

class Routers(Protocol):
    def __iter__(self)->Iterator[APIRouter]:
        pass



