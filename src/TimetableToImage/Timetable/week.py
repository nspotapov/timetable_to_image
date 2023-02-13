import datetime
from src.TimetableToImage import Timetable


class Week:
    DAYS_NAME = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]

    def __init__(self):
        self.begin = None
        self.end = None
        self.days = None
        self.group = None
        self.number = None
        self.timetable_bells = None

    def set_period(self, begin: datetime.date, end: datetime.date):
        self.begin = begin
        self.end = end
        if self.days:
            for i, day in enumerate(self.days):
                day: Timetable.Day
                day.date = self.begin + datetime.timedelta(days=i)
