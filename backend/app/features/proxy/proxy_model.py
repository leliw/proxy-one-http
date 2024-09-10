from pydantic import BaseModel


DEFAULT_TARGET_URL = "https://example.com"


class Settings(BaseModel):
    """Proxy server setting"""

    port: int = 8999
    target_url: str = DEFAULT_TARGET_URL


class Status(Settings):
    """Proxy server status"""

    status: str
