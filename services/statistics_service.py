import logging
from collections import defaultdict
from datetime import date

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.repositories.booking_repository import BookingRepository
from app.repositories.user_repository import UserRepository
from app.repositories.statistics_repository import StatisticsRepository

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class StatisticsService:
    def __init__(
            self,
            db: Session
    ):
        self.repo = StatisticsRepository(db)
        self.user_repo = UserRepository(db)
        self.booking_repo = BookingRepository(db)

    def get_occupancy_by_room_type(self):
        raw_data = self.repo.get_booking_count_by_room_type()
        logger.info(f"Occupancy stats by room type: {raw_data}")
        return [{"room_type": rt, "bookings": count} for rt, count in raw_data]

    def get_demographics(self):
        users = self.user_repo.get_all()
        stats = defaultdict(int)
        now = date.today()

        for user in users:
            if user.birth_date:
                age = now.year - user.birth_date.year - (
                        (now.month, now.day) < (user.birth_date.month, user.birth_date.day)
                )
                if age < 18:
                    stats["<18"] += 1
                elif age < 25:
                    stats["18-24"] += 1
                elif age < 35:
                    stats["25-34"] += 1
                elif age < 50:
                    stats["35-49"] += 1
                elif age < 65:
                    stats["50-64"] += 1
                else:
                    stats["65+"] += 1

            if user.nationality:
                stats[f"country:{user.nationality}"] += 1

            bookings = self.booking_repo.get_by_user_id(user.id)
            if len(bookings) > 1:
                stats["wiederkehrend"] += 1
            else:
                stats["einmalig"] += 1

        return {
            "age_distribution": {
                k: v for k, v in stats.items()
                if k in ["<18", "18-24", "25-34", "35-49", "50-64", "65+"]
            },
            "country_distribution": {
                k.replace("country:", ""): v for k, v in stats.items()
                if k.startswith("country:")
            },
            "returning_guests": {
                "wiederkehrend": stats["wiederkehrend"],
                "einmalig": stats["einmalig"]
            }
        }


def get_statistics_service(db: Session = Depends(get_db)) -> StatisticsService:
    return StatisticsService(db=db)
