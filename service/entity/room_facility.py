from sqlalchemy import Table, Column, ForeignKey
from app.util.base import Base

room_facility = Table(
    'room_facility',
    Base.metadata,
    Column('room_id', ForeignKey('room.id'), primary_key=True),
    Column('facility_id', ForeignKey('facility.id'), primary_key=True)
)