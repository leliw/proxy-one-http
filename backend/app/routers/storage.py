

from typing import Annotated
from fastapi import APIRouter, Depends

from app import model
from storage.directory_storage import DirectoryStorage


router = APIRouter(tags=["Sessions storage"])


def get_service():
    return DirectoryStorage(base_path="data/proxy")


ServiceDep = Annotated[DirectoryStorage, Depends(get_service)]

@router.get("")
async def get_keys(service: ServiceDep, path: str = None) -> list[str]:
    """Returns list of folders"""
    return service.keys(sub_path=path)


@router.get("/{key}")
async def get_key(service: ServiceDep, key: str, path: str = None) -> model.Request:
    """Returns file content"""
    return model.Request.parse_obj(service.get(key=key, sub_path=path, file_ext="json"))