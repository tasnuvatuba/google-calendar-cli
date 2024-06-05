from typing import List, Optional
from model.event import Event

from datetime import datetime
from typing import List, Optional


class RecurrenceRule:
    def __init__(self, freq, interval=1, count=None, until=None, by_day=None, by_month=None, by_year_day=None,
                 by_hour=None):
        self.freq = freq
        self.interval = interval
        self.count = count
        self.until = until
        self.by_day = by_day
        self.by_month = by_month
        self.by_year_day = by_year_day
        self.by_hour = by_hour

    def to_rrule(self):
        rrule = f"FREQ={self.freq.upper()}"
        if self.interval:
            rrule += f";INTERVAL={self.interval}"
        if self.count:
            rrule += f";COUNT={self.count}"
        if self.until:
            rrule += f";UNTIL={self.until.strftime('%Y%m%dT%H%M%SZ')}"
        if self.by_day:
            rrule += f";BYDAY={','.join(self.by_day).upper()}"
        if self.by_month:
            rrule += f";BYMONTH={','.join(map(str, self.by_month))}"
        if self.by_year_day:
            rrule += f";BYYEARDAY={','.join(map(str, self.by_year_day))}"
        if self.by_hour:
            rrule += f";BYHOUR={','.join(map(str, self.by_hour))}"
        return rrule


class RecurringEvent(Event):
    def __init__(self, title, start_time, end_time, recurrence: RecurrenceRule, description=None, location=None,
                 daylong=False, attendees: Optional[List[str]] = None):
        super().__init__(title, start_time, end_time, description, location, daylong, attendees)
        self.recurrence = recurrence

    def to_json(self):
        event = super().to_json()
        event['recurrence'] = self.recurrence.to_rrule()
        return event

    def __str__(self):
        base_str = super().__str__()
        return f"{base_str}\nRecurrence: {self.recurrence}"
