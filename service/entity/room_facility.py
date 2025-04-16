from sqlalchemy import Table, Column, ForeignKey

from app.util.base import Base

room_facility = Table(
    'room_facility',
    Base.metadata,
    Column('room_id', ForeignKey('room.room_id'), primary_key=True),
    Column('facility_id', ForeignKey('facility.facility_id'), primary_key=True)
)
