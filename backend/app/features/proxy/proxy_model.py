from typing import Optional
from pydantic import BaseModel


DEFAULT_TARGET_URL = "https://example.com"


class ProxySettings(BaseModel):
    """Proxy server setting"""

    port: int = 8999
    target_url: str = DEFAULT_TARGET_URL
    session_description: Optional[str] = None


class ProxyStatus(BaseModel):
    """Proxy server status"""

    status: str
    target_url: Optional[str] = None
    port: Optional[int] = None
