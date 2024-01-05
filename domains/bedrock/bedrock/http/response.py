

from dataclasses import dataclass
from typing import Generic, TypeVar


T = TypeVar('T')

@dataclass
class Response(Generic[T]):
    data: T


@dataclass
class Error:
    code:str
    message:str
    tags:dict[str,str]