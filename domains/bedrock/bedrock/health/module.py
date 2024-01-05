

from bedrock.di.module import Bind, module
from bedrock.health.router import create_health_router


@module
def base_health_module(bind:Bind):
    bind.singleton(create_health_router)