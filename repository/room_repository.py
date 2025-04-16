from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from app.database.database import SessionLocal
from app.service.entity.room import Room


class RoomRepository:
    def __init__(self):
        self.db = SessionLocal()

    def get_all(self) -> list[Room]:
        return self.db.query(Room).all()

    def get_by_id(self, room_id: int) -> Room:
        return self.db.query(Room).filter(Room.room_id == room_id).first()

    def get_by_hotel_id(self, hotel_id: int) -> list[Room]:
        return self.db.query(Room).filter(hotel_id == Room.hotel_id).options(joinedload(Room.type)).all()

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
        room = self.db.get_by_id(room_id)
        if room is None:
            raise HTTPException(status_code=404, detail="Room not found")
        self.db.delete(room)
        self.db.commit()
        return room
