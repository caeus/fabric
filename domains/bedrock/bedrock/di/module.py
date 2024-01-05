from typing import Callable
import injector

import typing_extensions
import typing


T = typing.TypeVar('T')


class Bind:
    binder: injector.Binder
    def __init__(self, binder: injector.Binder):
        self.binder = binder
    def singleton(self, callable: Callable[..., T]) -> None:
        annotations = typing_extensions.get_type_hints(callable)
        self.binder.bind(
            annotations["return"],
            injector.CallableProvider(injector.inject(callable)),
            injector.SingletonScope
        )
FModule = Callable[[injector.Binder], None]

def module(configure: Callable[[Bind], None]) -> FModule:
    def decorated(binder: injector.Binder) -> None:
        configure(Bind(binder))
    return decorated
