# all api centre

from fastapi import APIRouter
from Backend_py.api.routes import login

api_router = APIRouter()
api_router.include_router(login.router)