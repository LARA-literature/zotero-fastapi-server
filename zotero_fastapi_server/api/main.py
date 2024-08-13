

from fastapi import APIRouter, Response

from zotero_fastapi_server.api.routes import collections, items, schema #, login, users, utils

from zotero_fastapi_server.core.config import settings

api_router = APIRouter()
# api_router.include_router(login.router, tags=["login"])
# api_router.include_router(users.router, prefix="/users", tags=["users"])
# api_router.include_router(utils.router, prefix="/utils", tags=["utils"])

api_router.include_router(schema.router, prefix="", tags=["schema"])
api_router.include_router(collections.router, prefix=settings.API_V1_STR, tags=["collections"])
api_router.include_router(items.router, prefix=settings.API_V1_STR, tags=["items"])
