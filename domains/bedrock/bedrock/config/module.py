from types import MappingProxyType
from bedrock.di.module import Bind, module
import os


EnvConfig = MappingProxyType[str,str]



def create_default_env_config()->EnvConfig:
    return MappingProxyType(os.environ)

@module
def base_config_module(bind:Bind)->None:
    bind.singleton(create_default_env_config)