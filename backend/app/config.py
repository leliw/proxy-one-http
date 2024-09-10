from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

from ampf.base.ampf_base_factory import AmpfBaseFactory


class ServerConfig(BaseSettings):
    model_config = SettingsConfigDict(env_nested_delimiter="__")

    version: str = "1.1.0"
    data_dir: str = "data"


class ClientConfig(BaseModel):
    version: str


class UserConfig(BaseModel):
    target_url: str = "http://example.com"
    port: int = 8999


class UserConfigService:
    def __init__(self, factory: AmpfBaseFactory):
        self.storage = factory.create_compact_storage("user_config", UserConfig, key_name="config")

    def get(self) -> UserConfig:
        return self.storage.get("config")

    def put(self, config: UserConfig):
        self.storage.put("config", config)
