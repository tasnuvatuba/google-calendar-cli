from dateutil.parser import isoparse
from typing import List, Optional


class Event:
    def __init__(self, title, start_time, end_time, description=None, location=None,
                 daylong=False, attendees: Optional[List[str]] = None, event_id=None):
        self.title = title
        self.start_time = start_time
        self.end_time = end_time
        self.description = description
        self.location = location
        self.daylong = daylong
        self.attendees = attendees if attendees else []
        self.event_id = event_id

    @classmethod
    def from_json(cls, json_data):
        event_id = json_data.get('id')
        title = json_data.get("summary")
        start = json_data.get("start", {})
        end = json_data.get("end", {})
        description = json_data.get("description", None)
        location = json_data.get("location", None)
        daylong = False

        start_time = end_time = None
        if start:
            start_datetime = start.get("dateTime")
            start_date = start.get("date")
            if start_datetime:
                start_time = isoparse(start_datetime)
            elif start_date:
                start_time = isoparse(start_date)
                daylong = True

        if end:
            end_datetime = end.get("dateTime")
            end_date = end.get("date")
            if end_datetime:
                end_time = isoparse(end_datetime)
            elif end_date:
                end_time = isoparse(end_date)
                daylong = True

        attendees = [attendee["email"] for attendee in json_data.get("attendees", [])]
        return cls(title, start_time, end_time, description, location, daylong, attendees, event_id)

    def to_json(self):
        event = {
            "summary": self.title,
            "description": self.description,
            "location": self.location,
            "start": {
                "dateTime": self.start_time.isoformat() if not self.daylong else None,
                "date": self.start_time.date().isoformat() if self.daylong else None,
                "timeZone": "UTC"
            },
            "end": {
                "dateTime": self.end_time.isoformat() if not self.daylong else None,
                "date": self.end_time.date().isoformat() if self.daylong else None,
                "timeZone": "UTC"
            },
            "attendees": [{"email": attendee} for attendee in self.attendees]
        }

        if self.daylong:
            del event["start"]["dateTime"]
            del event["end"]["dateTime"]
        else:
            del event["start"]["date"]
            del event["end"]["date"]

        return event

    def __str__(self):
        event_details = (f"Event ID: {self.event_id}\n"
                         f"Event: {self.title}\n"
                         f"Description: {self.description}\n"
                         f"Location: {self.location}\n"
                         f"Attendees: {', '.join(self.attendees)}\n")

        event_details += (f"Start: {self.start_time}\n"
                          f"End: {self.end_time}\n")
        if self.daylong:
            event_details += "This is a day-long event\n"
        return event_details
