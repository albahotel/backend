from litestar import Controller, get
from litestar.di import Provide

from datetime import date, timedelta

from src.core.schemas.alert import AlertReadDTO
from src.core.providers import provide_alert_repository, provide_booking_repository
from src.core.repositories import BookingRepository, AlertRepository


class AnalyticsController(Controller):
    path = "/analytics"
    dependencies = {
        "booking_repository": Provide(provide_booking_repository),
        "alert_repository": Provide(provide_alert_repository),
    }
    tags = ["Analytics"]
    return_dto = AlertReadDTO

    @get(path="/occupied-rooms", sync_to_thread=False, exclude_from_auth=True)
    def get_rooms(
        self, start_date: date, end_date: date, booking_repository: BookingRepository
    ) -> dict:
        bookings = booking_repository.get_occupied_rooms(start_date, end_date)
        occupied_counts = {}
        for i in range(int((end_date - start_date).days) + 1):
            date = start_date + timedelta(i)
            if date not in occupied_counts:
                occupied_counts[date] = 0
        for booking in bookings:
            for n in range(int((booking.date_out - booking.date_in).days)):
                date = booking.date_in + timedelta(n)
                if date > end_date:
                    break
                if date < start_date:
                    continue
                occupied_counts[date] += 1
        labels = []
        dataset = []
        for date, count in occupied_counts.items():
            labels.append(date.isoformat())
            dataset.append(count)
            
        result = {
            "status": "success",
            "data": {
                "labels": labels,
                "dataset": dataset,
            },
        }

        return result

    @get(path="/alerts", sync_to_thread=False)
    def get_alerts(self, start_date: date, end_date: date, alert_repository: AlertRepository) -> dict:
        alerts = alert_repository.get_alerts(start_date, end_date)
        alerts_counts = {}
        for i in range(int((end_date - start_date).days) + 1):
            date = start_date + timedelta(i)
            if date not in alerts_counts:
                alerts_counts[date] = 0
        for alert in alerts:
            date = alert.created_at.date()
            alerts_counts[date] += 1

        labels = []
        dataset = []
        for date, count in alerts_counts.items():
            labels.append(date.isoformat())
            dataset.append(count)
            
        result = {
            "status": "success",
            "data": {
                "labels": labels,
                "dataset": dataset,
            },
        }
        
        return result