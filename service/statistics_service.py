from app.repository.statistics_repository import StatisticsRepository


class StatisticsService:
    def __init__(self, repo: StatisticsRepository):
        self.repo = repo

    def get_occupancy_by_room_type(self):
        raw_data = self.repo.get_booking_count_by_room_type()
        return [{"room_type": rt, "bookings": count} for rt, count in raw_data]
