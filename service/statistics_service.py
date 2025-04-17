import logging
from collections import defaultdict
from datetime import date

from app.repository.booking_repository import BookingRepository
from app.repository.guest_repository import GuestRepository
from app.repository.statistics_repository import StatisticsRepository

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class StatisticsService:
    def __init__(
            self,
            statistics_repo: StatisticsRepository,
            guest_repo: GuestRepository,
            booking_repo: BookingRepository
    ):
        self.repo = statistics_repo
        self.guest_repo = guest_repo
        self.booking_repo = booking_repo

    def get_occupancy_by_room_type(self):
        raw_data = self.repo.get_booking_count_by_room_type()
        logger.info(f"Occupancy stats by room type: {raw_data}")
        return [{"room_type": rt, "bookings": count} for rt, count in raw_data]

    def get_demographics(self):
        guests = self.guest_repo.get_all()
        stats = defaultdict(int)
        now = date.today()

        for guest in guests:
            if guest.birth_date:
                age = now.year - guest.birth_date.year - (
                        (now.month, now.day) < (guest.birth_date.month, guest.birth_date.day)
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

            if guest.nationality:
                stats[f"country:{guest.nationality}"] += 1

            bookings = self.booking_repo.get_by_guest_id(guest.id)
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
