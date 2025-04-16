from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from app.database.database import SessionLocal
from app.service.entity.room import Room
from app.service.entity.room_type import RoomType


class RoomRepository:
    def __init__(self):
        self.db = SessionLocal()

    def get_all(self) -> list[Room]:
        return self.db.query(Room).all()

    def get_by_id(self, room_id: int) -> Room:
        return self.db.query(Room).filter(Room.room_id == room_id).first()

    def get_filtered(self, hotel_id: int, capacity: int) -> list[Room]:
        query = self.db.query(Room).options(joinedload(Room.type)).filter(Room.hotel_id == hotel_id)
        if capacity is not None:
            query = query.join(Room.type).filter(RoomType.max_guests >= capacity)
        return query.all()

    def create(self, room_entity: Room) -> Room:
        self.db.add(room_entity)
        self.db.commit()
        self.db.refresh(room_entity)
        return room_entity

    def update(self, room_entity: Room) -> Room:
        self.db.commit()
        self.db.refresh(room_entity)
        return room_entity

    def delete(self, room_id: int):
        room = self.db.query(Room).filter(Room.room_id == room_id).first()
        if room is None:
            raise HTTPException(status_code=404, detail="Room not found")
        self.db.delete(room)
        self.db.commit()
        return room
