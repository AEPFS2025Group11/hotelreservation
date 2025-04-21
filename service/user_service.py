import logging
from datetime import datetime

from app.repository.user_repository import UserRepository
from app.service.models.user_models import UserModel


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.repo = user_repo
        self.logger = logging.getLogger(self.__class__.__name__)

    def get_all_users(self):
        self.logger.info("Fetching all users")
        users = self.repo.get_all()
        self.logger.debug(f"Fetched {len(users)} users")
        return users

    def get_user(self, user_id: int):
        self.logger.info(f"Fetching user with ID: {user_id}")
        user = self.repo.get_by_id(user_id)
        if not user:
            self.logger.warning(f"User with ID {user_id} not found")
        else:
            self.logger.debug(f"Found user: {user.email}")
        return user

    def update_user(self, user_id: int, data: UserModel):
        self.logger.info(f"Updating user with ID: {user_id}")
        user = self.repo.get_by_id(user_id)
        if not user:
            self.logger.warning(f"Cannot update: user {user_id} not found")
            return None
        for field, value in data.model_dump().items():
            setattr(user, field, value)
        user.updated_at = datetime.now()
        updated = self.repo.update(user)
        self.logger.debug(f"User {user_id} updated successfully")
        return updated

    def delete_user(self, user_id: int):
        self.logger.info(f"Deleting user with ID: {user_id}")
        deleted = self.repo.delete(user_id)
        if not deleted:
            self.logger.warning(f"User with ID {user_id} could not be deleted (not found)")
        else:
            self.logger.debug(f"User {user_id} deleted successfully")
        return deleted
