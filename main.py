from fastapi import Depends, FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.auth.oauth import auth_backend, fastapi_users
from app.auth.schema import UserRead, UserCreate, UserUpdate
from app.auth.models import User
from app.auth.oauth import current_user
from app.projects.routers import router as project_router


app = FastAPI(
    title='Test API',
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],

)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["Users"],
)

app.include_router(
    fastapi_users.get_reset_password_router(),
    tags=["Auth"],
)

app.include_router(
    project_router
)

origins = [
    "http://localhost:8000",
]

app.mount("/static/", StaticFiles(directory="static"), name="static")


@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_user)):
    return {"message": f"Hello {user.email}!"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie",
                   "Access-Control-Allow-Headers",
                   "Access-Control-Allow-Origin", "Authorization"],
)
