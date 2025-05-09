import logging
from datetime import datetime

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.repositories.user_repository import UserRepository
from app.services.models.user_models import UserModel

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db=db)

    def get_all_users(self):
        logger.info("Fetching all users")
        users = self.repo.get_all()
        logger.debug(f"Fetched {len(users)} users")
        return users

    def get_user(self, user_id: int):
        logger.info(f"Fetching user with ID: {user_id}")
        user = self.repo.get_by_id(user_id)
        if not user:
            logger.warning(f"User with ID {user_id} not found")
        else:
            logger.debug(f"Found user: {user.email}")
        return user

    def update_user(self, user_id: int, data: UserModel):
        logger.info(f"Updating user with ID: {user_id}")
        user = self.repo.get_by_id(user_id)
        if not user:
            logger.warning(f"Cannot update: user {user_id} not found")
            return None
        for field, value in data.model_dump().items():
            setattr(user, field, value)
        user.updated_at = datetime.now()
        updated = self.repo.update(user)
        logger.debug(f"User {user_id} updated successfully")
        return updated

    def delete_user(self, user_id: int):
        logger.info(f"Deleting user with ID: {user_id}")
        deleted = self.repo.delete(user_id)
        if not deleted:
            logger.warning(f"User with ID {user_id} could not be deleted (not found)")
        else:
            logger.debug(f"User {user_id} deleted successfully")
        return deleted


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db=db)
