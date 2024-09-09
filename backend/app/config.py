from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class ServerConfig(BaseSettings):
    model_config = SettingsConfigDict(env_nested_delimiter="__")

    version: str = "1.1.0"
    target_url: str = "http://example.com"
    port: int = 8999


class ClientConfig(BaseModel):
    version: str
    target_url: str
    port: int
