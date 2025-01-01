from fastapi import FastAPI
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware

from Backend_py.core.config import settings
from Backend_py.api.main import api_router

def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"



# FASTAPI App initialization
app = FastAPI(
    title = settings.PROJECT_NAME,
    openapi_url= f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id
)

if settings.all_cors_origin:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origin,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)
# DB initialization
from Backend_py.database.db_init import init_db
init_db()
# if __name__ == "__main__":
    