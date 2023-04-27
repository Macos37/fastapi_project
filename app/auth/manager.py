from typing import Optional

from fastapi import Depends, Request
from fastapi_users import (BaseUserManager, IntegerIDMixin, exceptions, models,
                           schemas)

from app.auth.models import User
from app.auth.utils import get_user_db
from config import SECRET

from logs.logger import Logger

logger = Logger(__name__)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        logger.logger.info(f"User ID {user.id} has registered.")

    async def create(
        self,
        user_create: schemas.UC,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> models.UP:
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user
    
    async def on_after_login(self, user: User, request: Optional[Request] = None):
        logger.logger.info(f"User ID {user.id} has logged in.")
        
    async def on_after_delete(self, user: User, request: Optional[Request] = None):
        logger.logger.info(f"User ID {user.id} has deleted.")
    
    async def on_after_update(self, user: User, request: Optional[Request] = None):
        logger.logger.info(f"User ID {user.id} has updated.")


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)