from dataclasses import dataclass

from fastapi import APIRouter

from bedrock.config.module import EnvConfig


@dataclass
class AppID:
    name: str
    env: str
    version: str


def create_app_id(config: EnvConfig) -> AppID:
    return AppID(
        name=config["APP_NAME"],
        env=config["APP_ENV"],
        version=config["APP_VERSION"]
    )


class AppIDRouter(APIRouter):
    pass


def create_app_id_router(id: AppID) -> AppIDRouter:
    router = AppIDRouter()

    @router.get("/version")
    def _():
        return id
    return router
