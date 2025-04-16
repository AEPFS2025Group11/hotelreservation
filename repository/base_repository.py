import logging
from fastapi import HTTPException

logger = logging.getLogger(__name__)


class BaseRepository:
    def __init__(self, db, model):
        self.db = db
        self.model = model

    def get_all(self):
        logger.info(f"Fetching all records from {self.model.__name__}")
        return self.db.query(self.model).all()

    def get_by_id(self, id_: int):
        logger.info(f"Fetching {self.model.__name__} by ID: {id_}")
        obj = self.db.query(self.model).get(id_)
        if obj is None:
            logger.warning(f"{self.model.__name__} with ID {id_} not found")
            raise HTTPException(status_code=404, detail=f"{self.model.__name__} not found")
        return obj

    def create(self, entity):
        logger.info(f"Creating new {self.model.__name__}: {entity}")
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        logger.info(f"{self.model.__name__} created with ID {entity.id}")
        return entity

    def update(self, entity):
        logger.info(f"Updating {self.model.__name__} with ID {entity.id}")
        entity = self.db.merge(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def delete(self, id_: int):
        logger.info(f"Deleting {self.model.__name__} with ID {id_}")
        obj = self.db.query(self.model).get(id_)
        if not obj:
            logger.warning(f"{self.model.__name__} with ID {id_} not found")
            raise HTTPException(status_code=404, detail=f"{self.model.__name__} not found")
        self.db.delete(obj)
        self.db.commit()
        return obj
